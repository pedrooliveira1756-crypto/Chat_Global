"""Run the frontend and API locally as separate development servers."""

import argparse
import ipaddress
import os
from pathlib import Path
import socket
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parent
BACKEND = ROOT / 'back-end'


def local_addresses():
    addresses = set()
    try:
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True, check=False)
        addresses.update(result.stdout.split())
    except OSError:
        pass
    try:
        addresses.update(item[4][0] for item in socket.getaddrinfo(socket.gethostname(), None, family=socket.AF_INET))
    except OSError:
        pass
    result = []
    for candidate in addresses:
        try:
            address = ipaddress.ip_address(candidate)
        except ValueError:
            continue
        if address.version == 4 and address.is_private and not address.is_loopback:
            result.append(candidate)
    return sorted(result)


def main():
    parser = argparse.ArgumentParser(description='Inicia frontend e API em servidores separados.')
    parser.add_argument('--ip', help='IP local do computador, caso a detecção automática falhe.')
    args = parser.parse_args()
    backend_environment = os.environ.copy()
    backend_environment['CHAT_LAN_DEV'] = '1'
    migration = subprocess.run(
        [sys.executable, 'manage.py', 'migrate', '--noinput'],
        cwd=BACKEND,
        env=backend_environment,
        check=False,
    )
    if migration.returncode:
        return migration.returncode
    processes = []
    try:
        processes.append(subprocess.Popen(
            [sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000', '--noreload'],
            cwd=BACKEND,
            env=backend_environment,
        ))
        processes.append(subprocess.Popen(
            [sys.executable, '-m', 'http.server', '5500', '--bind', '0.0.0.0', '--directory', str(ROOT / 'front-end')],
            cwd=ROOT,
        ))
        time.sleep(0.8)
        if any(process.poll() is not None for process in processes):
            print('Um servidor não iniciou. Verifique se as portas 5500 e 8000 estão livres.', file=sys.stderr)
            return 1

        print('\nNo PC: http://127.0.0.1:5500', flush=True)
        for address in ([args.ip] if args.ip else local_addresses()):
            print(f'Na rede local: http://{address}:5500', flush=True)
        print('Deixe este terminal aberto. Pressione Ctrl+C para parar.\n', flush=True)
        while all(process.poll() is None for process in processes):
            time.sleep(0.3)
        return 1
    except KeyboardInterrupt:
        return 0
    finally:
        for process in processes:
            if process.poll() is None:
                process.terminate()
        for process in processes:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


if __name__ == '__main__':
    raise SystemExit(main())

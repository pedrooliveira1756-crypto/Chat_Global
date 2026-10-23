import { copyFile, mkdir, rm, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = dirname(fileURLToPath(import.meta.url));
const output = join(root, 'dist');
const configuredUrl = process.env.CHAT_API_URL?.trim();

if (!configuredUrl) {
  throw new Error('Defina CHAT_API_URL na Vercel com a URL HTTPS da API no Render.');
}

let apiUrl;
try {
  apiUrl = new URL(configuredUrl);
} catch {
  throw new Error('CHAT_API_URL precisa ser uma URL absoluta, como https://sua-api.onrender.com.');
}

if (apiUrl.protocol !== 'https:' || apiUrl.username || apiUrl.password) {
  throw new Error('CHAT_API_URL precisa usar HTTPS e não pode conter credenciais.');
}

const apiBase = new URL('/chat/', apiUrl).toString();
await rm(output, { recursive: true, force: true });
await mkdir(output, { recursive: true });
await Promise.all(['index.html', 'style.css', 'app.js'].map((file) => copyFile(join(root, file), join(output, file))));
await writeFile(join(output, 'config.js'), `window.CHAT_API_URL = ${JSON.stringify(apiBase)};\n`);
console.log(`Frontend pronto. API: ${apiBase}`);

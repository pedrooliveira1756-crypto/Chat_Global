import { copyFile, mkdir, rm } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = dirname(fileURLToPath(import.meta.url));
const output = join(root, 'dist');
await rm(output, { recursive: true, force: true });
await mkdir(output, { recursive: true });
await Promise.all(['index.html', 'style.css', 'app.js', 'config.js'].map((file) => copyFile(join(root, file), join(output, file))));
console.log('Frontend pronto para a Vercel.');

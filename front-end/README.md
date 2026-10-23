# Frontend

Este site usa apenas HTML, CSS e JavaScript. No deploy, a Vercel executa `build.mjs`, que copia os arquivos para `dist/`. `config.js` já aponta para a API publicada no Render.

## Vercel

- Importe o repositório e selecione `front-end` como **Root Directory**.
- Escolha **Other** como Framework Preset.
- O `vercel.json` já define o comando de build e a pasta de saída. Faça o deploy.
- A URL `https://chatglobal-front-end.vercel.app` já está autorizada pelo backend. Para outro domínio, adicione a nova origem em `FRONTEND_ORIGINS` no Render.

Para testar o build sem Vercel:

```bash
node build.mjs
```

Confira que `dist/config.js` aponta para `https://chat-realtime-api-1nul.onrender.com/chat/`. A URL da API é pública; nenhum segredo deve entrar nesse arquivo.

## No PC e na rede local

Na raiz do projeto, execute `.venv/bin/python run_chat.py`. No PC, abra `http://127.0.0.1:5500`. O frontend local usa automaticamente a API na porta `8000` do mesmo computador. Em outro dispositivo na mesma rede, use um dos endereços que o comando mostrar. Se a detecção do IP falhar, execute `.venv/bin/python run_chat.py --ip SEU-IP`.

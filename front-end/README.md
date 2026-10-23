# Frontend

Este site usa apenas HTML, CSS e JavaScript. No deploy, a Vercel executa `build.mjs`, que copia os arquivos para `dist/`. `config.js` chama `/chat/` na própria Vercel, e `vercel.json` encaminha as requisições ao Render.

## Vercel

- Importe o repositório e selecione `front-end` como **Root Directory**. Se o projeto estiver configurado com a raiz do repositório, o `vercel.json` da raiz também está preparado.
- Escolha **Other** como Framework Preset.
- O `vercel.json` já define o comando de build e a pasta de saída. Faça o deploy.
- Depois do deploy, abra `https://chatglobal-front-end.vercel.app/chat/health/`: deve aparecer `{"status":"ok"}`.

Para testar o build sem Vercel:

```bash
node build.mjs
```

Confira que `dist/config.js` usa `/chat/` fora da porta local `5500`. A URL do Render fica na regra de encaminhamento do `vercel.json`.

## No PC e na rede local

Na raiz do projeto, execute `.venv/bin/python run_chat.py`. No PC, abra `http://127.0.0.1:5500`. O frontend local usa automaticamente a API na porta `8000` do mesmo computador. Em outro dispositivo na mesma rede, use um dos endereços que o comando mostrar. Se a detecção do IP falhar, execute `.venv/bin/python run_chat.py --ip SEU-IP`.

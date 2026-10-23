# Frontend

Este site usa apenas HTML, CSS e JavaScript. No deploy, a Vercel executa `build.mjs`, que copia os arquivos para `dist/`. Em produção, `config.js` aponta diretamente para a API no Render.

## Vercel

- Importe o repositório e selecione `front-end` como **Root Directory**. Se o projeto estiver configurado com a raiz do repositório, o `vercel.json` da raiz também está preparado.
- Escolha **Other** como Framework Preset.
- O `vercel.json` já define o comando de build e a pasta de saída. Faça o deploy.
- Confira `https://chat-realtime-api-1nul.onrender.com/chat/health/`: deve aparecer `{"status":"ok"}`. Depois abra o site na Vercel e crie um usuário.

Para testar o build sem Vercel:

```bash
node build.mjs
```

Confira que `dist/config.js` aponta para a URL do Render fora da porta local `5500`. Se a URL da API mudar, atualize `config.js` e publique o frontend novamente.

## No PC e na rede local

Na raiz do projeto, execute `.venv/bin/python run_chat.py`. No PC, abra `http://127.0.0.1:5500`. O frontend local usa automaticamente a API na porta `8000` do mesmo computador. Em outro dispositivo na mesma rede, use um dos endereços que o comando mostrar. Se a detecção do IP falhar, execute `.venv/bin/python run_chat.py --ip SEU-IP`.

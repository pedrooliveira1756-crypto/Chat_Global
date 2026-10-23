# Chat RealTime

O projeto tem duas aplicações separadas:

- `back-end/`: API Django, pronta para Render.
- `front-end/`: HTML, CSS e JavaScript estáticos, prontos para Vercel.

As mensagens são atualizadas a cada 3 segundos. A API ainda não usa WebSocket.

## Deploy: Render primeiro, Vercel depois

1. Envie este projeto para um repositório Git acessível pelas duas plataformas.
2. No Render, crie um **Blueprint** a partir do repositório. O arquivo `render.yaml` cria o serviço Python com raiz `back-end` e um PostgreSQL. Espere o deploy terminar e copie a URL HTTPS da API, por exemplo `https://chat-realtime-api.onrender.com`. Confira `https://SUA-API.onrender.com/chat/health/`: a resposta deve ser `{"status":"ok"}`.
3. Na Vercel, importe o mesmo repositório como outro projeto e escolha **Framework Preset** `Other`. Pode usar **Root Directory** `front-end` (recomendado) ou a raiz do repositório; há um `vercel.json` preparado nos dois lugares. Faça um novo deploy ao mudar essa opção.
4. O frontend chama `https://chat-realtime-api-1nul.onrender.com/chat/` diretamente. Se a URL do Render mudar, atualize `front-end/config.js`.
5. Confira `https://chat-realtime-api-1nul.onrender.com/chat/health/`. A resposta deve ser `{"status":"ok"}`. Depois teste o cadastro, a leitura e o envio de mensagens no site da Vercel.

O backend permite requisições do domínio `https://chatglobal-front-end.vercel.app` via CORS. Se usar outro domínio para o frontend, adicione-o em `FRONTEND_ORIGINS` no Render.

**Sobre o plano gratuito do Render:** o PostgreSQL Free expira depois de 30 dias e não tem backup gerenciado. O `render.yaml` usa esse plano para facilitar testes; escolha um plano persistente antes de guardar conversas importantes. O banco local `back-end/db.sqlite3` não vai para o Render automaticamente.

## Desenvolvimento local

Com a `.venv` existente, na raiz do projeto:

```bash
.venv/bin/python run_chat.py
```

O comando aplica as migrações e inicia dois servidores separados. No PC, abra `http://127.0.0.1:5500`. Veja mais em `front-end/README.md`.

# Chat RealTime

O projeto tem duas aplicações separadas:

- `back-end/`: API Django, pronta para Render.
- `front-end/`: HTML, CSS e JavaScript estáticos, prontos para Vercel.

As mensagens são atualizadas a cada 3 segundos. A API ainda não usa WebSocket.

## Deploy: Render primeiro, Vercel depois

1. Envie este projeto para um repositório Git acessível pelas duas plataformas.
2. No Render, crie um **Blueprint** a partir do repositório. O arquivo `render.yaml` cria o serviço Python com raiz `back-end` e um PostgreSQL. Espere o deploy terminar e copie a URL HTTPS da API, por exemplo `https://chat-realtime-api.onrender.com`. Confira `https://SUA-API.onrender.com/chat/health/`: a resposta deve ser `{"status":"ok"}`.
3. Na Vercel, importe o mesmo repositório como outro projeto. Defina **Root Directory** como `front-end` e **Framework Preset** como `Other`. Crie a variável de ambiente `CHAT_API_URL` com a URL HTTPS da API do Render, sem precisar adicionar `/chat/`. O `vercel.json` executa o build e publica `dist/`.
4. Quando a Vercel fornecer a URL do site, volte ao serviço da API no Render e crie `FRONTEND_ORIGINS` com a origem exata, por exemplo `https://meu-chat.vercel.app` (sem barra final). Salve e faça um novo deploy do backend.
5. Abra a URL da Vercel e teste o cadastro, a leitura e o envio de mensagens.

Se usar domínio próprio ou um endereço de preview diferente, adicione essa origem em `FRONTEND_ORIGINS`, separando múltiplas origens por vírgulas. Se mudar `CHAT_API_URL` na Vercel, faça um novo deploy do frontend: o valor entra no arquivo estático durante o build.

**Sobre o plano gratuito do Render:** o PostgreSQL Free expira depois de 30 dias e não tem backup gerenciado. O `render.yaml` usa esse plano para facilitar testes; escolha um plano persistente antes de guardar conversas importantes. O banco local `back-end/db.sqlite3` não vai para o Render automaticamente.

## Desenvolvimento local

Com a `.venv` existente, na raiz do projeto:

```bash
.venv/bin/python run_chat.py
```

O comando aplica as migrações e inicia dois servidores separados. No PC, abra `http://127.0.0.1:5500`. Veja mais em `front-end/README.md`.

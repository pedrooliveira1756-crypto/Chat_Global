# API Django no Render

As rotas `/`, `/chat/health/`, `/chat/create_user/` e `/chat/messages/` respondem JSON. O serviço Render usa esta pasta como **Root Directory**, instala `requirements.txt`, aplica migrações no início e executa Gunicorn. O banco PostgreSQL vem de `DATABASE_URL`.

Variáveis de produção:

| Variável | Uso |
| --- | --- |
| `DJANGO_DEBUG` | `false` em produção. |
| `DJANGO_SECRET_KEY` | Chave gerada pelo Render Blueprint. |
| `DATABASE_URL` | URL interna do PostgreSQL, ligada pelo Blueprint. |
| `FRONTEND_ORIGINS` | Origens extras, caso use outro domínio. `https://chatglobal-front-end.vercel.app` já está permitido. |
| `DJANGO_ALLOWED_HOSTS` | Opcional no Render: `RENDER_EXTERNAL_HOSTNAME` é adicionado automaticamente. Necessário para outros domínios se configurados. |

O frontend precisa receber um token ao criar usuário e enviá-lo junto com `user_id` e `content` ao postar mensagens. O token fica salvo no navegador. O chat continua público: não há contas com senha nem moderação.

Para testar localmente usando o SQLite existente, execute `../.venv/bin/python manage.py test conversas` nesta pasta. A variável `DATABASE_URL` é obrigatória quando `DJANGO_DEBUG=false`; o SQLite é usado apenas no desenvolvimento local.

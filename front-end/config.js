// No desenvolvimento local, usa a API no mesmo computador.
// Na Vercel, o navegador acessa diretamente a API no Render.
window.CHAT_API_URL = window.location.port === '5500'
  ? `${window.location.protocol}//${window.location.hostname}:8000/chat/`
  : 'https://chat-realtime-api-1nul.onrender.com/chat/';

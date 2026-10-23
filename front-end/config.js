// No desenvolvimento local, usa a API no mesmo computador.
// Na Vercel, /chat/ é encaminhado ao Render pelo vercel.json.
window.CHAT_API_URL = window.location.port === '5500'
  ? `${window.location.protocol}//${window.location.hostname}:8000/chat/`
  : '/chat/';

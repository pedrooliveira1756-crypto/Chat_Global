// Usa o mesmo endereço pelo qual o frontend foi aberto (PC ou celular).
// Altere esta URL se a API estiver em outro host ou porta.
window.CHAT_API_URL = window.location.port === '5500'
  ? `${window.location.protocol}//${window.location.hostname}:8000/chat/`
  : '/chat/';

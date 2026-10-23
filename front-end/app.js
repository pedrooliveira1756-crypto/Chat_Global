const apiBase = window.CHAT_API_URL.replace(/\/+$/, '') + '/';
const $ = (selector) => document.querySelector(selector);
const elements = {
  overlay: $('#overlay'), joinForm: $('#join-form'), username: $('#username'),
  joinButton: $('#join-button'), joinError: $('#join-error'),
  identity: $('#identity'), identityName: $('#identity-name'), identityAvatar: $('#identity-avatar'),
  switchUser: $('#switch-user'), conversation: $('#conversation'), messages: $('#messages'),
  status: $('#status'), statusText: $('#status-text'), feedback: $('#feedback'),
  messageForm: $('#message-form'), messageInput: $('#message-input'), sendButton: $('#send-button'),
};

let currentUser = null;
let loadingMessages = false;
let loadedOnce = false;
const displayedIds = new Set();

try {
  const saved = JSON.parse(localStorage.getItem('chat-user'));
  if (Number.isInteger(saved?.id) && typeof saved?.username === 'string' && typeof saved?.token === 'string') currentUser = saved;
} catch (_) { /* Acesso sem armazenamento local continua funcionando. */ }

function saveUser(user) {
  currentUser = user;
  try { localStorage.setItem('chat-user', JSON.stringify(user)); } catch (_) { /* Opcional. */ }
}

function clearUser() {
  currentUser = null;
  try { localStorage.removeItem('chat-user'); } catch (_) { /* Opcional. */ }
}

function updateIdentity() {
  const hasUser = Boolean(currentUser);
  elements.overlay.hidden = hasUser;
  elements.identity.hidden = !hasUser;
  elements.messageInput.disabled = !hasUser;
  elements.sendButton.disabled = !hasUser;
  if (hasUser) {
    elements.identityName.textContent = currentUser.username;
    elements.identityAvatar.textContent = currentUser.username.trim().charAt(0).toUpperCase() || '?';
    elements.messageInput.focus();
  } else {
    elements.username.focus();
  }
  for (const row of elements.messages.children) {
    const author = row.querySelector('.message-author');
    author.querySelector('.you-tag')?.remove();
    if (currentUser && Number(row.dataset.userId) === currentUser.id) {
      const you = document.createElement('span');
      you.className = 'you-tag';
      you.textContent = 'você';
      author.append(you);
    }
  }
}

function setConnection(online) {
  elements.status.classList.toggle('online', online);
  elements.status.classList.toggle('offline', !online);
  elements.statusText.textContent = online ? 'Conectado' : 'Sem conexão';
}

async function api(path, options = {}) {
  let response;
  try {
    response = await fetch(apiBase + path, {
      ...options,
      headers: options.body ? { 'Content-Type': 'application/json' } : undefined,
    });
  } catch (_) {
    throw new Error(`Não foi possível acessar a API em ${apiBase}. Confira a conexão entre este site e o Render.`);
  }

  let data;
  try { data = await response.json(); } catch (_) { throw new Error('A API retornou uma resposta inválida.'); }
  if (!response.ok) throw new Error(data.error || `Erro ${response.status} na API.`);
  return data;
}

function avatarTone(name) {
  let value = 0;
  for (const character of name) value = (value + character.charCodeAt(0)) % 5;
  return String(value);
}

function appendMessage(message) {
  if (displayedIds.has(message.id)) return;
  displayedIds.add(message.id);

  const row = document.createElement('article');
  row.className = 'message';
  row.dataset.userId = message.user_id;
  const avatar = document.createElement('span');
  avatar.className = 'avatar';
  avatar.dataset.tone = avatarTone(message.username);
  avatar.setAttribute('aria-hidden', 'true');
  avatar.textContent = message.username.trim().charAt(0).toUpperCase() || '?';

  const body = document.createElement('div');
  body.className = 'message-body';
  const author = document.createElement('div');
  author.className = 'message-author';
  const name = document.createElement('strong');
  name.textContent = message.username;
  author.append(name);
  if (currentUser && message.user_id === currentUser.id) {
    const you = document.createElement('span');
    you.className = 'you-tag';
    you.textContent = 'você';
    author.append(you);
  }
  const content = document.createElement('p');
  content.className = 'message-content';
  content.textContent = message.content;
  body.append(author, content);
  row.append(avatar, body);
  elements.messages.append(row);
}

async function loadMessages() {
  if (loadingMessages) return;
  loadingMessages = true;
  try {
    const messages = await api('messages/');
    if (!Array.isArray(messages)) throw new Error('A API retornou mensagens em formato inválido.');
    const nearBottom = elements.conversation.scrollHeight - elements.conversation.scrollTop - elements.conversation.clientHeight < 110;
    for (const message of messages) appendMessage(message);
    if (nearBottom || !loadedOnce) elements.conversation.scrollTop = elements.conversation.scrollHeight;
    loadedOnce = true;
    setConnection(true);
  } catch (error) {
    setConnection(false);
    elements.feedback.textContent = error.message;
  } finally {
    loadingMessages = false;
  }
}

elements.joinForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const username = elements.username.value.trim();
  if (!username) { elements.joinError.textContent = 'Digite um nome para continuar.'; return; }
  elements.joinError.textContent = '';
  elements.joinButton.disabled = true;
  try {
    const user = await api('create_user/', { method: 'POST', body: JSON.stringify({ username }) });
    saveUser(user);
    updateIdentity();
    setConnection(true);
    elements.feedback.textContent = '';
    await loadMessages();
  } catch (error) {
    elements.joinError.textContent = error.message;
    setConnection(false);
  } finally {
    elements.joinButton.disabled = false;
  }
});

elements.switchUser.addEventListener('click', () => {
  clearUser();
  updateIdentity();
});

elements.messageForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const content = elements.messageInput.value.trim();
  if (!currentUser || !content) return;
  elements.sendButton.disabled = true;
  elements.feedback.textContent = '';
  try {
    const message = await api('messages/', { method: 'POST', body: JSON.stringify({ user_id: currentUser.id, token: currentUser.token, content }) });
    appendMessage(message);
    elements.messageInput.value = '';
    elements.messageInput.style.height = '';
    elements.conversation.scrollTop = elements.conversation.scrollHeight;
    setConnection(true);
  } catch (error) {
    elements.feedback.textContent = error.message;
    setConnection(false);
  } finally {
    elements.sendButton.disabled = !currentUser;
    elements.messageInput.focus();
  }
});

elements.messageInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
    event.preventDefault();
    elements.messageForm.requestSubmit();
  }
});
elements.messageInput.addEventListener('input', () => {
  elements.messageInput.style.height = 'auto';
  elements.messageInput.style.height = `${Math.min(elements.messageInput.scrollHeight, 140)}px`;
});

updateIdentity();
loadMessages();
setInterval(loadMessages, 3000);

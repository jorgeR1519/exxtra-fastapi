const SESSION_KEY = "exxtra-clientes-session";

export function isClientSession(session) {
  return session?.user?.tipo?.toLowerCase() === "cliente";
}

export function getSession() {
  const rawValue = window.localStorage.getItem(SESSION_KEY);
  return rawValue ? JSON.parse(rawValue) : null;
}

export function setSession(session) {
  window.localStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

export function clearSession() {
  window.localStorage.removeItem(SESSION_KEY);
}

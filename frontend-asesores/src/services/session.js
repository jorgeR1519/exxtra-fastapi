const SESSION_KEY = "exxtra-asesores-session";

export function isAdvisorSession(session) {
  const role = session?.user?.tipo?.toLowerCase();
  return role === "asesor" || role === "intermediario";
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

import { reactive } from "vue";

const TOKEN_KEY = "credistep.token";
const THEME_KEY = "credistep.theme";

function safeGet(key) {
  try { return localStorage.getItem(key); } catch { return null; }
}
function safeSet(key, value) {
  try { value == null ? localStorage.removeItem(key) : localStorage.setItem(key, value); } catch { /* sin storage */ }
}

export const store = reactive({
  token: safeGet(TOKEN_KEY),
  user: null,
  theme: safeGet(THEME_KEY) || "light",
  toasts: [],
  sidebarOpen: false,

  setSession(token, user) {
    this.token = token;
    this.user = user;
    safeSet(TOKEN_KEY, token);
  },
  logout() {
    this.token = null;
    this.user = null;
    safeSet(TOKEN_KEY, null);
  },
  toggleTheme() {
    this.theme = this.theme === "dark" ? "light" : "dark";
    safeSet(THEME_KEY, this.theme);
    applyTheme();
  },
  toast(message, opts = {}) {
    const id = Math.random().toString(36).slice(2);
    this.toasts.push({ id, message, type: opts.type || "ok", xp: opts.xp || 0, icon: opts.icon || "✨" });
    setTimeout(() => { this.toasts = this.toasts.filter((t) => t.id !== id); }, opts.duration || 3600);
  },
});

export function applyTheme() {
  document.documentElement.setAttribute("data-theme", store.theme);
}

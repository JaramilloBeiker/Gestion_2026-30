import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import { refreshUser } from "./api.js";
import { applyTheme, store } from "./store.js";
import { Bar, Icon, Loading, Modal, PremiumLock, ProgressRing, Toasts } from "./components/ui.js";
import AppShell from "./components/AppShell.js";
import Landing from "./views/Landing.js";
import Auth from "./views/Auth.js";
import Diagnostic from "./views/Diagnostic.js";
import DiagnosticResult from "./views/DiagnosticResult.js";
import Dashboard from "./views/Dashboard.js";
import Plan from "./views/Plan.js";
import Learn from "./views/Learn.js";
import Lesson from "./views/Lesson.js";
import Simulators from "./views/Simulators.js";
import Goals from "./views/Goals.js";
import Reminders from "./views/Reminders.js";
import Glossary from "./views/Glossary.js";
import Premium from "./views/Premium.js";
import Profile from "./views/Profile.js";
import Admin from "./views/Admin.js";

applyTheme();

const routes = [
  { path: "/", component: Landing, meta: { public: true } },
  { path: "/ingresar", component: Auth, props: { mode: "login" }, meta: { guest: true } },
  { path: "/registro", component: Auth, props: { mode: "register" }, meta: { guest: true } },
  { path: "/diagnostico", component: Diagnostic, meta: { auth: true, skipOnboarding: true } },
  {
    path: "/",
    component: AppShell,
    meta: { auth: true },
    children: [
      { path: "inicio", component: Dashboard, meta: { title: "Inicio" } },
      { path: "diagnostico/resultado", component: DiagnosticResult, meta: { title: "Mi diagnóstico" } },
      { path: "mi-plan", component: Plan, meta: { title: "Mi ruta" } },
      { path: "aprende", component: Learn, meta: { title: "Aprende" } },
      { path: "aprende/:slug", component: Lesson, props: true, meta: { title: "Lección" } },
      { path: "simuladores", component: Simulators, meta: { title: "Simuladores" } },
      { path: "metas", component: Goals, meta: { title: "Metas" } },
      { path: "recordatorios", component: Reminders, meta: { title: "Recordatorios" } },
      { path: "glosario", component: Glossary, meta: { title: "Glosario" } },
      { path: "plus", component: Premium, meta: { title: "CrediStep Plus" } },
      { path: "perfil", component: Profile, meta: { title: "Perfil", skipOnboarding: true } },
      { path: "institucion", component: Admin, meta: { title: "Panel institucional", admin: true } },
    ],
  },
  { path: "/:pathMatch(.*)*", redirect: "/" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
});

router.beforeEach(async (to) => {
  if (store.token && !store.user) {
    try { await refreshUser(); } catch { store.logout(); }
  }
  const user = store.user;
  const needsAuth = to.matched.some((r) => r.meta.auth);
  if (needsAuth && !user) return { path: "/ingresar", query: { next: to.fullPath } };
  if (to.meta.guest && user) return user.role === "admin" ? "/institucion" : "/inicio";
  if (user && needsAuth) {
    if (user.role === "admin" && !to.meta.admin && to.path !== "/perfil") return "/institucion";
    if (user.role !== "admin" && to.meta.admin) return "/inicio";
    if (user.role !== "admin" && !user.onboarded && !to.meta.skipOnboarding) return "/diagnostico";
  }
  store.sidebarOpen = false;
  document.title = to.meta.title ? `${to.meta.title} · CrediStep` : "CrediStep · Tu GPS financiero";
  return true;
});

const app = createApp({
  components: { Toasts },
  template: `<router-view/><Toasts/>`,
});
app.component("Icon", Icon);
app.component("ProgressRing", ProgressRing);
app.component("Bar", Bar);
app.component("Modal", Modal);
app.component("PremiumLock", PremiumLock);
app.component("Loading", Loading);
app.use(router);
app.mount("#app");

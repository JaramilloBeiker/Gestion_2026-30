import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { store } from "../store.js";
import { initials } from "../utils.js";
import StepAssistant from "./StepAssistant.js";

export default {
  components: { StepAssistant },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const isAdmin = computed(() => store.user?.role === "admin");
    const studentNav = [
      { to: "/inicio", icon: "home", label: "Inicio" },
      { to: "/mi-plan", icon: "map", label: "Mi ruta" },
      { to: "/aprende", icon: "book", label: "Aprende" },
      { to: "/simuladores", icon: "calc", label: "Simuladores" },
      { to: "/metas", icon: "target", label: "Metas" },
      { to: "/recordatorios", icon: "bell", label: "Recordatorios" },
    ];
    const moreNav = [
      { to: "/glosario", icon: "search", label: "Glosario" },
      { to: "/diagnostico/resultado", icon: "compass", label: "Mi diagnóstico" },
      { to: "/perfil", icon: "user", label: "Perfil" },
    ];
    const title = computed(() => route.meta.title || "CrediStep");
    function logout() {
      store.logout();
      router.push("/");
    }
    return { store, isAdmin, studentNav, moreNav, title, logout, initials };
  },
  template: `
  <div class="shell">
    <aside class="sidebar" :class="{ open: store.sidebarOpen }" @click="store.sidebarOpen = false">
      <router-link to="/" class="brand"><img src="/assets/img/logo.svg" alt=""/><div>CrediStep<small>Tu GPS financiero</small></div></router-link>
      <template v-if="isAdmin">
        <div class="nav-section">Institución</div>
        <router-link to="/institucion" class="nav-link"><Icon name="building"/> Panel institucional</router-link>
        <router-link to="/perfil" class="nav-link"><Icon name="user"/> Perfil</router-link>
      </template>
      <template v-else>
        <div class="nav-section">Tu camino</div>
        <router-link v-for="n in studentNav" :key="n.to" :to="n.to" class="nav-link"><Icon :name="n.icon"/> {{ n.label }}</router-link>
        <div class="nav-section">Más</div>
        <router-link v-for="n in moreNav" :key="n.to" :to="n.to" class="nav-link"><Icon :name="n.icon"/> {{ n.label }}</router-link>
        <router-link to="/plus" class="nav-link"><Icon name="crown"/> CrediStep Plus <span v-if="!store.user?.is_premium" class="pill">PRO</span></router-link>
      </template>
      <div class="sidebar-card" v-if="!isAdmin && !store.user?.is_premium">
        <h4>👑 Pásate a Plus</h4>
        <p>Simulador de puntaje, lecciones avanzadas y metas ilimitadas.</p>
        <router-link to="/plus" class="btn btn-lime btn-sm btn-block">$20.000 / mes</router-link>
      </div>
      <div class="sidebar-card" v-else-if="store.user?.institution">
        <h4>🎓 {{ store.user.institution }}</h4>
        <p style="margin-bottom:0">{{ isAdmin ? 'Administrador de licencia' : 'Plus incluido por tu institución' }}</p>
      </div>
      <button class="nav-link" style="border:0;background:none;width:100%;margin-top:10px" @click="logout"><Icon name="logout"/> Cerrar sesión</button>
    </aside>
    <div class="overlay" :class="{ show: store.sidebarOpen }" @click="store.sidebarOpen = false"></div>

    <div class="main">
      <header class="topbar">
        <button class="icon-btn menu-btn" @click="store.sidebarOpen = true" aria-label="Menú"><Icon name="menu"/></button>
        <h1>{{ title }}</h1>
        <div class="spacer"></div>
        <span v-if="!isAdmin" class="chip-stat hide-sm" title="Experiencia">⭐ {{ store.user?.xp ?? 0 }} XP</span>
        <button class="icon-btn" @click="store.toggleTheme()" :aria-label="store.theme === 'dark' ? 'Modo claro' : 'Modo oscuro'">
          <Icon :name="store.theme === 'dark' ? 'sun' : 'moon'"/>
        </button>
        <router-link to="/perfil" class="avatar" :title="store.user?.name">{{ initials(store.user?.name) }}</router-link>
      </header>
      <main class="content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in"><component :is="Component"/></transition>
        </router-view>
      </main>
    </div>
    <StepAssistant v-if="!isAdmin"/>
  </div>`,
};

import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { api } from "../api.js";
import { store } from "../store.js";
import { fmtDate, initials, GOALS_LABELS, SEGMENTS } from "../utils.js";

export default {
  setup() {
    const router = useRouter();
    const form = reactive({ name: store.user?.name || "", age: store.user?.age || "", city: store.user?.city || "" });
    const busy = ref(false);
    async function save() {
      busy.value = true;
      try {
        store.user = await api.patch("/auth/me", { name: form.name, age: form.age ? Number(form.age) : null, city: form.city || null });
        store.toast("Perfil actualizado", { icon: "💾" });
      } catch (e) { store.toast(e.message, { type: "error" }); }
      finally { busy.value = false; }
    }
    function logout() { store.logout(); router.push("/"); }
    return { store, form, busy, save, logout, initials, fmtDate, GOALS_LABELS, SEGMENTS };
  },
  template: `
  <div class="grid-2 appear" style="align-items:start">
    <div class="card center" style="padding:32px">
      <div class="avatar" style="width:96px;height:96px;border-radius:30px;font-size:34px;margin:0 auto">{{ initials(store.user?.name) }}</div>
      <h2 class="mt-2" style="font-size:24px;font-weight:800">{{ store.user?.name }}</h2>
      <p class="muted">{{ store.user?.email }}</p>
      <div class="row wrap mt-2" style="justify-content:center">
        <span class="badge" v-if="store.user?.role === 'admin'">🏛️ Administrador institucional</span>
        <span class="badge badge-lime" v-else-if="store.user?.is_premium">👑 Plus</span>
        <span class="badge badge-muted" v-else>Plan gratis</span>
        <span class="badge" v-if="store.user?.segment">{{ SEGMENTS[store.user.segment] }}</span>
        <span class="badge" v-if="store.user?.institution">🎓 {{ store.user.institution }}</span>
      </div>
      <div class="grid-2 mt-3" style="gap:12px" v-if="store.user?.role !== 'admin'">
        <div class="kpi"><div class="label">Experiencia</div><div class="value">⭐ {{ store.user?.xp }} XP</div></div>
        <div class="kpi"><div class="label">Meta principal</div><div class="value" style="font-size:16px">{{ GOALS_LABELS[store.user?.main_goal] || '—' }}</div></div>
      </div>
      <p class="xs muted mt-3">Miembro desde el {{ fmtDate(store.user?.created_at, { day: 'numeric', month: 'long', year: 'numeric' }) }}</p>
    </div>

    <div class="stack-lg">
      <form class="card form-grid" @submit.prevent="save">
        <div class="card-title">✏️ Tus datos</div>
        <div class="field"><label>Nombre</label><input class="input" v-model="form.name" required minlength="2"/></div>
        <div class="form-row">
          <div class="field"><label>Edad</label><input class="input" type="number" min="14" max="99" v-model="form.age"/></div>
          <div class="field"><label>Ciudad</label><input class="input" v-model="form.city"/></div>
        </div>
        <button class="btn btn-primary" :disabled="busy" style="justify-self:start">Guardar cambios</button>
      </form>
      <div class="card stack">
        <div class="card-title">⚙️ Preferencias</div>
        <div class="row-between"><span>Modo oscuro</span><button class="btn btn-outline btn-sm" @click="store.toggleTheme()">{{ store.theme === 'dark' ? '🌙 Activado' : '☀️ Desactivado' }}</button></div>
        <div class="row-between" v-if="store.user?.role !== 'admin'"><span>Diagnóstico financiero</span><router-link to="/diagnostico" class="btn btn-outline btn-sm">Repetir</router-link></div>
        <div class="row-between"><span>Sesión</span><button class="btn btn-danger btn-sm" @click="logout">Cerrar sesión</button></div>
      </div>
      <p class="xs muted">🔒 Tus datos se tratan conforme a la Ley 1581 de 2012 (protección de datos personales). Las instituciones aliadas solo ven métricas agregadas, nunca tu información individual.</p>
    </div>
  </div>`,
};

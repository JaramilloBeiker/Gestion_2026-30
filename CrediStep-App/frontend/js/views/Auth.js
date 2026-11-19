import { reactive, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { api } from "../api.js";
import { store } from "../store.js";

export default {
  props: { mode: String },
  setup(props) {
    const router = useRouter();
    const route = useRoute();
    const form = reactive({ name: "", email: "", password: "", age: "", institution_code: "" });
    const error = ref("");
    const busy = ref(false);
    const institution = ref(null);
    const showCode = ref(false);

    let timer;
    watch(() => form.institution_code, (code) => {
      clearTimeout(timer);
      institution.value = null;
      if (code.trim().length < 4) return;
      timer = setTimeout(async () => {
        try { institution.value = (await api.get(`/auth/institution/${encodeURIComponent(code.trim())}`)).name; }
        catch { institution.value = false; }
      }, 400);
    });

    async function submit() {
      error.value = "";
      busy.value = true;
      try {
        const payload = props.mode === "login"
          ? { email: form.email, password: form.password }
          : { name: form.name, email: form.email, password: form.password, age: form.age ? Number(form.age) : null, institution_code: form.institution_code || null };
        const res = await api.post(props.mode === "login" ? "/auth/login" : "/auth/register", payload);
        store.setSession(res.token, res.user);
        if (props.mode === "register") store.toast("¡Bienvenido a CrediStep!", { xp: 10, icon: "🌱" });
        const next = route.query.next;
        if (res.user.role === "admin") router.push("/institucion");
        else if (!res.user.onboarded) router.push("/diagnostico");
        else router.push(typeof next === "string" ? next : "/inicio");
      } catch (e) {
        error.value = e.message;
      } finally {
        busy.value = false;
      }
    }
    function fillDemo(kind) {
      form.email = kind === "admin" ? "admin@javeriana.edu.co" : "demo@credistep.co";
      form.password = "CrediStep2026";
    }
    return { form, error, busy, submit, fillDemo, institution, showCode };
  },
  template: `
  <div class="auth">
    <aside class="auth-side">
      <div class="grid-lines"></div>
      <router-link to="/" class="brand" style="position:relative"><img src="/assets/img/logo.svg" alt=""/><div>CrediStep</div></router-link>
      <div style="position:relative">
        <h2>Aprende, planifica y construye tu futuro.</h2>
        <p class="mt-2" style="color:rgba(232,255,243,.8);font-size:17px;max-width:440px">Construye tu historial crediticio paso a paso, con una ruta hecha para ti.</p>
        <div class="stack mt-4" style="max-width:380px">
          <div class="card" style="background:rgba(255,255,255,.07);border-color:rgba(255,255,255,.12);color:#fff">
            <div class="row"><span style="font-size:28px">🧭</span><div><strong>Diagnóstico en 2 minutos</strong><div class="small" style="opacity:.75">Descubre dónde estás hoy</div></div></div>
          </div>
          <div class="card" style="background:rgba(255,255,255,.07);border-color:rgba(255,255,255,.12);color:#fff;margin-left:30px">
            <div class="row"><span style="font-size:28px">📈</span><div><strong>Índice de preparación</strong><div class="small" style="opacity:.75">Mira tu progreso semana a semana</div></div></div>
          </div>
        </div>
      </div>
      <p class="small" style="position:relative;opacity:.6">Contenido educativo y neutral. No vendemos productos financieros.</p>
    </aside>

    <main class="auth-main">
      <div class="auth-card appear">
        <router-link to="/" class="muted small row" style="gap:4px;margin-bottom:24px"><Icon name="chevronLeft" :size="16"/> Volver al inicio</router-link>
        <h1>{{ mode === 'login' ? '¡Hola de nuevo! 👋' : 'Crea tu cuenta' }}</h1>
        <p class="muted mt-1">{{ mode === 'login' ? 'Ingresa para seguir con tu ruta.' : 'Empieza gratis y arma tu ruta personalizada.' }}</p>

        <form class="form-grid mt-3" @submit.prevent="submit">
          <div v-if="error" class="error-box">{{ error }}</div>
          <template v-if="mode === 'register'">
            <div class="field"><label for="name">Nombre</label><input id="name" class="input" v-model="form.name" required minlength="2" placeholder="¿Cómo te llamas?" autocomplete="name"/></div>
          </template>
          <div class="field"><label for="email">Correo electrónico</label><input id="email" class="input" type="email" v-model="form.email" required placeholder="tucorreo@ejemplo.com" autocomplete="email"/></div>
          <div class="field"><label for="pw">Contraseña</label><input id="pw" class="input" type="password" v-model="form.password" required :minlength="mode === 'register' ? 8 : 1" :placeholder="mode === 'register' ? 'Mínimo 8 caracteres' : 'Tu contraseña'" :autocomplete="mode === 'login' ? 'current-password' : 'new-password'"/></div>
          <template v-if="mode === 'register'">
            <div class="field"><label for="age">Edad <span class="muted">(opcional)</span></label><input id="age" class="input" type="number" min="14" max="99" v-model="form.age" placeholder="Ej. 20"/></div>
            <button v-if="!showCode" type="button" class="btn btn-ghost btn-sm" style="justify-self:start;padding-left:0" @click="showCode = true">🎓 ¿Tu universidad tiene licencia? Ingresa el código</button>
            <div v-else class="field">
              <label for="code">Código institucional</label>
              <input id="code" class="input" v-model="form.institution_code" placeholder="Ej. JAVERIANA2026" style="text-transform:uppercase"/>
              <span v-if="institution" class="hint" style="color:var(--primary)">✓ {{ institution }} — tendrás Plus incluido</span>
              <span v-else-if="institution === false" class="hint" style="color:var(--danger)">Código no encontrado</span>
            </div>
          </template>
          <button class="btn btn-primary btn-lg btn-block mt-1" :disabled="busy">{{ busy ? 'Un momento…' : (mode === 'login' ? 'Ingresar' : 'Crear cuenta y empezar') }}</button>
        </form>

        <p class="center small mt-3 muted">
          <template v-if="mode === 'login'">¿No tienes cuenta? <router-link to="/registro" class="bold">Regístrate</router-link></template>
          <template v-else>¿Ya tienes cuenta? <router-link to="/ingresar" class="bold">Ingresa</router-link></template>
        </p>

        <div v-if="mode === 'login'" class="demo-box mt-3">
          <strong>Cuentas de demostración</strong> · contraseña <code>CrediStep2026</code>
          <div class="row wrap mt-1">
            <button type="button" class="btn btn-soft btn-sm" @click="fillDemo('student')">👩‍🎓 Estudiante</button>
            <button type="button" class="btn btn-soft btn-sm" @click="fillDemo('admin')">🏛️ Universidad</button>
          </div>
        </div>
      </div>
    </main>
  </div>`,
};

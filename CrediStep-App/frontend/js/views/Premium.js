import { onMounted, ref } from "vue";
import { api, refreshUser } from "../api.js";
import { store } from "../store.js";
import { cop, fmtDate } from "../utils.js";

export default {
  setup() {
    const info = ref(null);
    const confirmPlan = ref(null);
    const busy = ref(false);
    onMounted(async () => { info.value = await api.get("/premium/plans"); });

    async function activate() {
      busy.value = true;
      try {
        await api.post("/premium/activate", { plan: confirmPlan.value.id });
        await refreshUser();
        store.toast("¡Bienvenido a CrediStep Plus!", { xp: 20, icon: "👑" });
        confirmPlan.value = null;
      } catch (e) { store.toast(e.message, { type: "error" }); }
      finally { busy.value = false; }
    }
    async function cancel() {
      if (!window.confirm("¿Seguro que quieres cancelar Plus?")) return;
      await api.post("/premium/cancel");
      await refreshUser();
      store.toast("Tu suscripción fue cancelada", { icon: "👋" });
    }
    const cell = (v) => (v === true ? "✅" : v === false ? "—" : v);
    return { info, store, confirmPlan, activate, cancel, busy, cop, fmtDate, cell };
  },
  template: `
  <div>
    <div class="card card-dark" style="padding:36px;margin-bottom:24px">
      <div class="grid-lines"></div>
      <div style="position:relative;max-width:640px">
        <span class="badge badge-lime">👑 CrediStep Plus</span>
        <h2 style="font-size:34px;font-weight:800;color:#fff;margin-top:14px">Seguimiento avanzado para llegar más rápido a tu meta</h2>
        <p class="muted mt-2" style="font-size:16px">Una app que quieres abrir, no un trámite del banco. Plus te da herramientas para entender a fondo tu progreso.</p>
        <div v-if="store.user?.is_premium" class="next-task mt-3" style="background:rgba(255,255,255,.08);border-color:rgba(190,242,100,.4);color:#fff">
          <div class="ico">✨</div>
          <div><div class="bold">Ya tienes Plus activo</div>
            <div class="small" style="opacity:.8">{{ store.user.premium_plan === 'institucional' ? 'Incluido por ' + store.user.institution : 'Plan ' + store.user.premium_plan + ' · vigente hasta el ' + fmtDate(store.user.premium_until, { day: 'numeric', month: 'long', year: 'numeric' }) }}</div></div>
        </div>
      </div>
    </div>

    <Loading v-if="!info" :height="300"/>
    <div v-else class="stack-lg appear">
      <div class="grid-3">
        <div class="card plan-card">
          <h3 style="font-size:19px;font-weight:800">Gratis</h3>
          <div class="price mt-1">$0</div>
          <p class="muted small">Lo esencial para empezar tu ruta.</p>
          <button class="btn btn-outline btn-block mt-3" disabled>{{ store.user?.is_premium ? 'Plan base' : 'Tu plan actual' }}</button>
        </div>
        <div v-for="p in info.plans" :key="p.id" class="card plan-card" :class="{ featured: p.id === 'mensual' }">
          <span v-if="p.badge" class="badge badge-lime" style="position:absolute;top:18px;right:18px">{{ p.badge }}</span>
          <h3 style="font-size:19px;font-weight:800">{{ p.name }}</h3>
          <div class="price mt-1">{{ cop(p.price) }}<span class="small muted" style="font-weight:600"> /{{ p.period }}</span></div>
          <p class="muted small">{{ p.id === 'anual' ? 'Equivale a ' + cop(p.price / 12) + ' al mes.' : 'Cancela cuando quieras.' }}</p>
          <button class="btn btn-block mt-3" :class="p.id === 'mensual' ? 'btn-primary' : 'btn-outline'"
            :disabled="store.user?.is_premium" @click="confirmPlan = p">{{ store.user?.premium_plan === p.id ? 'Plan activo' : 'Elegir ' + p.name }}</button>
        </div>
      </div>

      <div class="card">
        <div class="card-title" style="margin-bottom:10px">Compara los planes</div>
        <div style="overflow-x:auto">
          <table class="feature-table">
            <thead><tr><th>Función</th><th>Gratis</th><th>Plus</th></tr></thead>
            <tbody><tr v-for="f in info.features" :key="f.feature"><td>{{ f.feature }}</td><td>{{ cell(f.free) }}</td><td class="bold" style="color:var(--primary)">{{ cell(f.plus) }}</td></tr></tbody>
          </table>
        </div>
      </div>

      <div class="card row wrap" style="gap:20px">
        <span style="font-size:40px">🎓</span>
        <div style="flex:1;min-width:240px"><h3 style="font-size:18px;font-weight:800">¿Tu universidad tiene licencia CrediStep?</h3>
          <p class="muted small">Con el código institucional obtienes Plus sin costo. Empezamos con la Pontificia Universidad Javeriana.</p></div>
        <button v-if="store.user?.is_premium && store.user.premium_plan !== 'institucional'" class="btn btn-danger btn-sm" @click="cancel">Cancelar suscripción</button>
      </div>
    </div>

    <Modal v-if="confirmPlan" title="Activar CrediStep Plus" @close="confirmPlan = null">
      <div class="stack">
        <div class="next-task"><div class="ico">👑</div><div><div class="bold">{{ confirmPlan.name }}</div><div class="small muted">{{ cop(confirmPlan.price) }} / {{ confirmPlan.period }}</div></div></div>
        <div class="demo-box">🧪 <strong>Versión inicial de demostración:</strong> no se realiza ningún cobro ni se solicitan datos de pago. La pasarela de pagos se integrará en una siguiente versión.</div>
        <button class="btn btn-primary btn-block" :disabled="busy" @click="activate">{{ busy ? 'Activando…' : 'Activar Plus (demo)' }}</button>
      </div>
    </Modal>
  </div>`,
};

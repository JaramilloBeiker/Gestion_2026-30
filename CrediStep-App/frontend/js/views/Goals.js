import { computed, onMounted, reactive, ref } from "vue";
import { api, refreshUser } from "../api.js";
import { store } from "../store.js";
import { cop, fmtDate, GOAL_CATEGORIES } from "../utils.js";

const empty = () => ({ title: "", category: "emergencia", target_amount: null, current_amount: 0, deadline: "" });

export default {
  setup() {
    const data = ref(null);
    const showForm = ref(false);
    const editing = ref(null);
    const form = reactive(empty());
    const contributeGoal = ref(null);
    const amount = ref(null);
    const error = ref("");

    async function load() { data.value = await api.get("/goals"); }
    onMounted(load);

    const totals = computed(() => {
      const g = data.value?.goals || [];
      return { saved: g.reduce((a, x) => a + x.current_amount, 0), target: g.reduce((a, x) => a + x.target_amount, 0) };
    });
    const atLimit = computed(() => data.value?.limit !== null && data.value?.goals.length >= data.value?.limit);

    function openNew() {
      Object.assign(form, empty());
      editing.value = null;
      error.value = "";
      showForm.value = true;
    }
    function openEdit(g) {
      Object.assign(form, { title: g.title, category: g.category, target_amount: g.target_amount, current_amount: g.current_amount, deadline: g.deadline || "" });
      editing.value = g.id;
      error.value = "";
      showForm.value = true;
    }
    async function save() {
      error.value = "";
      try {
        const body = { ...form, deadline: form.deadline || null };
        if (editing.value) await api.put(`/goals/${editing.value}`, body);
        else { await api.post("/goals", body); store.toast("¡Nueva meta creada!", { xp: 15, icon: "🎯" }); }
        showForm.value = false;
        await load();
        refreshUser();
      } catch (e) { error.value = e.message; }
    }
    async function contribute() {
      try {
        const g = await api.post(`/goals/${contributeGoal.value.id}/contribute`, { amount: Number(amount.value) });
        store.toast(g.pct >= 100 ? `¡Cumpliste tu meta ${g.title}! 🏆` : `Aporte de ${cop(amount.value)} registrado`, { xp: g.pct >= 100 ? 110 : 10, icon: "🐷" });
        contributeGoal.value = null;
        amount.value = null;
        await load();
        refreshUser();
      } catch (e) { store.toast(e.message, { type: "error" }); }
    }
    async function remove(g) {
      if (!window.confirm(`¿Eliminar la meta "${g.title}"?`)) return;
      await api.del(`/goals/${g.id}`);
      await load();
    }
    function monthly(g) {
      if (!g.deadline || g.remaining <= 0) return null;
      const months = Math.max(1, Math.ceil((new Date(g.deadline) - new Date()) / (30 * 864e5)));
      return g.remaining / months;
    }
    return { data, showForm, editing, form, save, openNew, openEdit, contributeGoal, amount, contribute, remove, totals, atLimit, error, cop, fmtDate, monthly, GOAL_CATEGORIES };
  },
  template: `
  <div>
    <div class="page-head">
      <div><h2>Mis metas</h2><p>Ahorra con propósito: fondo de emergencia, viajes, independencia o estudios.</p></div>
      <button class="btn btn-primary" @click="atLimit ? $router.push('/plus') : openNew()"><Icon name="plus" :size="18"/> Nueva meta</button>
    </div>
    <Loading v-if="!data" :count="2" :height="160"/>
    <div v-else class="stack-lg appear">
      <div class="grid-3">
        <div class="card"><div class="xs bold muted">AHORRADO EN TOTAL</div><div class="big-number" style="color:var(--primary)">{{ cop(totals.saved) }}</div></div>
        <div class="card"><div class="xs bold muted">META TOTAL</div><div class="big-number">{{ cop(totals.target) }}</div></div>
        <div class="card"><div class="xs bold muted">METAS ACTIVAS</div><div class="big-number">{{ data.goals.length }}<span v-if="data.limit" class="muted" style="font-size:20px"> / {{ data.limit }}</span></div>
          <router-link v-if="data.limit" to="/plus" class="xs bold">Metas ilimitadas con Plus →</router-link></div>
      </div>

      <div v-if="!data.goals.length" class="card empty">
        <div class="e-ico">🎯</div><h3>Aún no tienes metas</h3>
        <p class="mt-1">Te recomendamos empezar con un fondo de emergencia de un mes de gastos.</p>
        <button class="btn btn-primary mt-3" @click="openNew">Crear mi primera meta</button>
      </div>

      <div class="grid-2">
        <div v-for="g in data.goals" :key="g.id" class="card goal-card card-hover">
          <div class="row">
            <div class="g-ico">{{ GOAL_CATEGORIES[g.category].icon }}</div>
            <div style="flex:1;min-width:0"><h3 style="font-size:18px;font-weight:800">{{ g.title }}</h3>
              <div class="xs muted">{{ GOAL_CATEGORIES[g.category].label }}<span v-if="g.deadline"> · Para el {{ fmtDate(g.deadline, { day: 'numeric', month: 'short', year: 'numeric' }) }}</span></div></div>
            <button class="icon-btn" @click="openEdit(g)" aria-label="Editar"><Icon name="edit" :size="18"/></button>
            <button class="icon-btn" @click="remove(g)" aria-label="Eliminar"><Icon name="trash" :size="18"/></button>
          </div>
          <div class="row-between mt-3"><span class="bold" style="font-size:22px">{{ cop(g.current_amount) }}</span><span class="muted small">de {{ cop(g.target_amount) }}</span></div>
          <Bar :value="g.pct" class="mt-1"/>
          <div class="row-between mt-2 small">
            <span :class="g.pct >= 100 ? 'bold' : 'muted'" :style="g.pct >= 100 ? 'color:var(--primary)' : ''">{{ g.pct >= 100 ? '🏆 ¡Meta cumplida!' : g.pct + '% · faltan ' + cop(g.remaining) }}</span>
            <span v-if="monthly(g)" class="muted">≈ {{ cop(monthly(g)) }}/mes</span>
          </div>
          <button v-if="g.pct < 100" class="btn btn-soft btn-block mt-3" @click="contributeGoal = g">🐷 Registrar aporte</button>
        </div>
      </div>
    </div>

    <Modal v-if="showForm" :title="editing ? 'Editar meta' : 'Nueva meta'" @close="showForm = false">
      <form class="form-grid" @submit.prevent="save">
        <div v-if="error" class="error-box">{{ error }}</div>
        <div class="field"><label>Tipo de meta</label>
          <div class="row wrap" style="gap:8px">
            <button v-for="(c, k) in GOAL_CATEGORIES" :key="k" type="button" class="btn btn-sm" :class="form.category === k ? 'btn-primary' : 'btn-outline'" @click="form.category = k">{{ c.icon }} {{ c.label }}</button>
          </div></div>
        <div class="field"><label>Nombre</label><input class="input" v-model="form.title" required minlength="2" placeholder="Ej. Viaje a Santa Marta"/></div>
        <div class="form-row">
          <div class="field"><label>¿Cuánto necesitas?</label><div class="input-prefix"><span>$</span><input class="input" type="number" min="1" v-model.number="form.target_amount" required/></div></div>
          <div class="field"><label>Ya tengo</label><div class="input-prefix"><span>$</span><input class="input" type="number" min="0" v-model.number="form.current_amount"/></div></div>
        </div>
        <div class="field"><label>Fecha objetivo <span class="muted">(opcional)</span></label><input class="input" type="date" v-model="form.deadline"/></div>
        <button class="btn btn-primary btn-block">{{ editing ? 'Guardar cambios' : 'Crear meta' }}</button>
      </form>
    </Modal>

    <Modal v-if="contributeGoal" :title="'Aporte a ' + contributeGoal.title" @close="contributeGoal = null">
      <form class="form-grid" @submit.prevent="contribute">
        <div class="field"><label>¿Cuánto vas a aportar?</label><div class="input-prefix"><span>$</span><input class="input" type="number" min="1" v-model.number="amount" required autofocus/></div></div>
        <div class="row wrap" style="gap:8px"><button v-for="v in [10000, 20000, 50000, 100000]" :key="v" type="button" class="btn btn-outline btn-sm" @click="amount = v">{{ cop(v) }}</button></div>
        <button class="btn btn-primary btn-block">Registrar aporte</button>
      </form>
    </Modal>
  </div>`,
};

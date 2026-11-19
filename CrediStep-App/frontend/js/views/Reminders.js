import { computed, onMounted, reactive, ref } from "vue";
import { api, refreshUser } from "../api.js";
import { store } from "../store.js";
import { cop, fmtDate, relDays, todayISO, REMINDER_KINDS } from "../utils.js";

const empty = () => ({ title: "", kind: "pago", due_date: todayISO(3), recurrence: "monthly", amount: null });

export default {
  setup() {
    const items = ref(null);
    const filter = ref("pending");
    const showForm = ref(false);
    const editing = ref(null);
    const form = reactive(empty());
    const error = ref("");

    async function load() { items.value = await api.get("/reminders"); }
    onMounted(load);

    const shown = computed(() => (items.value || []).filter((r) => (filter.value === "pending" ? !r.done : r.done)));
    const counts = computed(() => {
      const list = items.value || [];
      return {
        overdue: list.filter((r) => r.status === "overdue").length,
        soon: list.filter((r) => r.status === "soon").length,
        done: list.filter((r) => r.done).length,
      };
    });

    function openNew() { Object.assign(form, empty()); editing.value = null; error.value = ""; showForm.value = true; }
    function openEdit(r) {
      Object.assign(form, { title: r.title, kind: r.kind, due_date: r.due_date, recurrence: r.recurrence, amount: r.amount });
      editing.value = r.id; error.value = ""; showForm.value = true;
    }
    async function save() {
      error.value = "";
      try {
        const body = { ...form, amount: form.amount || null };
        if (editing.value) await api.put(`/reminders/${editing.value}`, body);
        else { await api.post("/reminders", body); store.toast("Recordatorio creado", { xp: 5, icon: "🔔" }); }
        showForm.value = false;
        await load();
        refreshUser();
      } catch (e) { error.value = e.message; }
    }
    async function toggle(r) {
      const res = await api.post(`/reminders/${r.id}/toggle`);
      if (res.reminder.done) {
        const onTime = r.status !== "overdue";
        store.toast(onTime ? "¡Cumplido a tiempo! 👏" : "Marcado como cumplido", { xp: onTime ? 15 : 5, icon: "✅" });
        if (res.next) setTimeout(() => store.toast(`Próximo: ${fmtDate(res.next.due_date)}`, { icon: "🔁" }), 400);
      }
      await load();
      refreshUser();
    }
    async function remove(r) {
      if (!window.confirm(`¿Eliminar "${r.title}"?`)) return;
      await api.del(`/reminders/${r.id}`);
      await load();
    }
    const recLabel = { none: "Una vez", weekly: "Semanal", monthly: "Mensual" };
    return { items, filter, shown, counts, showForm, editing, form, save, openNew, openEdit, toggle, remove, error, cop, fmtDate, relDays, REMINDER_KINDS, recLabel };
  },
  template: `
  <div>
    <div class="page-head">
      <div><h2>Recordatorios</h2><p>Pagar a tiempo es lo que más pesa en tu historial. Nunca más una fecha límite olvidada.</p></div>
      <button class="btn btn-primary" @click="openNew"><Icon name="plus" :size="18"/> Nuevo recordatorio</button>
    </div>
    <Loading v-if="!items" :height="300"/>
    <div v-else class="stack-lg appear">
      <div class="grid-3">
        <div class="card row"><span style="font-size:30px">🚨</span><div><div class="big-number" style="font-size:30px;color:var(--danger)">{{ counts.overdue }}</div><div class="small muted">Vencidos</div></div></div>
        <div class="card row"><span style="font-size:30px">⏳</span><div><div class="big-number" style="font-size:30px;color:var(--warning)">{{ counts.soon }}</div><div class="small muted">En los próximos 3 días</div></div></div>
        <div class="card row"><span style="font-size:30px">✅</span><div><div class="big-number" style="font-size:30px;color:var(--primary)">{{ counts.done }}</div><div class="small muted">Cumplidos</div></div></div>
      </div>

      <div class="card">
        <div class="card-head">
          <div class="tabs"><button class="tab" :class="{ active: filter === 'pending' }" @click="filter = 'pending'">Pendientes</button><button class="tab" :class="{ active: filter === 'done' }" @click="filter = 'done'">Cumplidos</button></div>
        </div>
        <div v-if="!shown.length" class="empty"><div class="e-ico">🔔</div><p>{{ filter === 'pending' ? 'No tienes recordatorios pendientes.' : 'Aún no has cumplido recordatorios.' }}</p></div>
        <div class="list">
          <div v-for="r in shown" :key="r.id" class="list-item" style="gap:14px">
            <button class="checkbox" :class="{ on: r.done }" @click="toggle(r)" :aria-label="'Marcar ' + r.title"><Icon name="check" :size="15" :stroke="3"/></button>
            <div style="font-size:24px">{{ REMINDER_KINDS[r.kind].icon }}</div>
            <div style="flex:1;min-width:0">
              <div class="bold" :style="r.done ? 'text-decoration:line-through;color:var(--muted)' : ''">{{ r.title }}</div>
              <div class="xs muted">{{ fmtDate(r.due_date, { weekday: 'short', day: 'numeric', month: 'short' }) }} · {{ recLabel[r.recurrence] }}<span v-if="r.amount"> · {{ cop(r.amount) }}</span></div>
            </div>
            <span v-if="!r.done" class="badge" :class="{ 'badge-danger': r.status === 'overdue', 'badge-warning': r.status === 'soon', 'badge-muted': r.status === 'upcoming' }">{{ relDays(r.days_left) }}</span>
            <button class="icon-btn" @click="openEdit(r)" aria-label="Editar"><Icon name="edit" :size="18"/></button>
            <button class="icon-btn" @click="remove(r)" aria-label="Eliminar"><Icon name="trash" :size="18"/></button>
          </div>
        </div>
      </div>
    </div>

    <Modal v-if="showForm" :title="editing ? 'Editar recordatorio' : 'Nuevo recordatorio'" @close="showForm = false">
      <form class="form-grid" @submit.prevent="save">
        <div v-if="error" class="error-box">{{ error }}</div>
        <div class="field"><label>Tipo</label>
          <div class="row wrap" style="gap:8px"><button v-for="(k, key) in REMINDER_KINDS" :key="key" type="button" class="btn btn-sm" :class="form.kind === key ? 'btn-primary' : 'btn-outline'" @click="form.kind = key">{{ k.icon }} {{ k.label }}</button></div></div>
        <div class="field"><label>Descripción</label><input class="input" v-model="form.title" required minlength="2" placeholder="Ej. Pagar tarjeta antes de la fecha límite"/></div>
        <div class="form-row">
          <div class="field"><label>Fecha</label><input class="input" type="date" v-model="form.due_date" required/></div>
          <div class="field"><label>Se repite</label><select class="select" v-model="form.recurrence"><option value="none">Una vez</option><option value="weekly">Cada semana</option><option value="monthly">Cada mes</option></select></div>
        </div>
        <div class="field"><label>Monto <span class="muted">(opcional)</span></label><div class="input-prefix"><span>$</span><input class="input" type="number" min="0" v-model.number="form.amount"/></div></div>
        <button class="btn btn-primary btn-block">{{ editing ? 'Guardar' : 'Crear recordatorio' }}</button>
      </form>
    </Modal>
  </div>`,
};

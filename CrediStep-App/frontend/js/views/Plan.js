import { onMounted, ref } from "vue";
import { api, refreshUser } from "../api.js";
import { store } from "../store.js";

export default {
  setup() {
    const plan = ref(null);
    const busyId = ref(null);
    onMounted(async () => { plan.value = await api.get("/plan"); });

    async function toggle(task) {
      if (task.lesson_slug || busyId.value) return;
      busyId.value = task.id;
      try {
        const method = task.done ? "del" : "post";
        plan.value = await api[method](`/plan/tasks/${task.id}/complete`);
        if (!task.done) store.toast(`¡Completaste: ${task.title}!`, { xp: task.xp, icon: "✅" });
        refreshUser();
      } catch (e) {
        store.toast(e.message, { type: "error" });
      } finally {
        busyId.value = null;
      }
    }
    return { plan, toggle, busyId };
  },
  template: `
  <div>
    <div class="page-head">
      <div><h2>Mi ruta · ¡Vamos paso a paso!</h2><p>Pequeños pasos que construyen un gran historial. Tu ruta se adapta a tu diagnóstico.</p></div>
      <router-link to="/diagnostico" class="btn btn-outline btn-sm"><Icon name="refresh" :size="16"/> Actualizar diagnóstico</router-link>
    </div>
    <Loading v-if="!plan" :count="3" :height="140"/>
    <div v-else class="stack-lg appear">
      <div class="card row wrap" style="gap:24px">
        <ProgressRing :value="plan.pct" :size="110" :stroke="11"/>
        <div style="flex:1;min-width:220px">
          <div class="xs bold muted">PROGRESO DE TU RUTA</div>
          <div class="bold" style="font-size:20px">{{ plan.completed }} de {{ plan.total }} pasos completados</div>
          <Bar :value="plan.pct" class="mt-2"/>
        </div>
        <div class="next-task" style="flex:1;min-width:260px" v-if="plan.next_task">
          <div class="ico">➡️</div>
          <div><div class="xs bold muted">PRÓXIMO OBJETIVO</div><div class="bold">{{ plan.next_task.title }}</div></div>
        </div>
      </div>

      <div class="gps">
        <div v-for="s in plan.steps" :key="s.id" class="gps-step" :class="s.status">
          <div class="gps-node">{{ s.status === 'done' ? '✅' : s.icon }}</div>
          <div class="card">
            <div class="row-between wrap">
              <div>
                <div class="xs bold muted">PASO {{ s.order }}</div>
                <h3 style="font-size:19px;font-weight:800">{{ s.title }}</h3>
                <p class="muted small mt-1">{{ s.description }}</p>
              </div>
              <span class="badge" :class="{ 'badge-lime': s.status === 'done', 'badge-muted': s.status === 'pending' }">
                {{ s.status === 'done' ? '¡Completado!' : s.status === 'active' ? 'En curso' : 'Pendiente' }} · {{ s.completed }}/{{ s.total }}
              </span>
            </div>
            <div class="mt-3">
              <div v-for="t in s.tasks" :key="t.id" class="task" :class="{ done: t.done }">
                <button class="checkbox" :class="{ on: t.done }" :disabled="!!t.lesson_slug || busyId === t.id" @click="toggle(t)"
                  :title="t.lesson_slug ? 'Se completa al aprobar la lección' : (t.done ? 'Desmarcar' : 'Marcar como hecho')" :aria-label="t.title">
                  <Icon name="check" :size="15" :stroke="3"/>
                </button>
                <div style="flex:1;min-width:0">
                  <div class="task-title">{{ t.title }}</div>
                  <div class="small muted">{{ t.description }}<span v-if="t.auto && t.done"> · completado automáticamente</span></div>
                </div>
                <span class="badge badge-muted hide-sm">+{{ t.xp }} XP</span>
                <router-link v-if="t.lesson_slug && !t.done" :to="'/aprende/' + t.lesson_slug" class="btn btn-soft btn-sm">Ver lección</router-link>
                <router-link v-else-if="t.action_route && !t.done" :to="t.action_route" class="btn btn-soft btn-sm">Ir</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>`,
};

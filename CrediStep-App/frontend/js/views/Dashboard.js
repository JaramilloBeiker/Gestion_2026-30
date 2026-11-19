import { computed, onMounted, ref } from "vue";
import { api, refreshUser } from "../api.js";
import { store } from "../store.js";
import { cop, relDays, timeAgo, REMINDER_KINDS } from "../utils.js";

export default {
  setup() {
    const d = ref(null);
    onMounted(async () => {
      d.value = await api.get("/dashboard");
      refreshUser();
    });
    const greeting = computed(() => {
      const h = new Date().getHours();
      return h < 12 ? "Buenos días" : h < 19 ? "Buenas tardes" : "Buenas noches";
    });
    const maxWeek = computed(() => Math.max(10, ...(d.value?.week.map((w) => w.xp) || [0])));
    const firstName = computed(() => (store.user?.name || "").split(" ")[0]);
    return { d, store, greeting, maxWeek, firstName, cop, relDays, timeAgo, REMINDER_KINDS };
  },
  template: `
  <div>
    <div class="page-head">
      <div><h2>{{ greeting }}, {{ firstName }} 👋</h2><p>Este es tu progreso hacia tu próximo gran paso financiero.</p></div>
      <div class="row" v-if="d">
        <span class="chip-stat flame">🔥 {{ d.streak }} {{ d.streak === 1 ? 'día' : 'días' }} de racha</span>
        <span class="chip-stat">🌱 Nivel {{ d.level.level }} · {{ d.level.name }}</span>
      </div>
    </div>

    <Loading v-if="!d" :count="2"/>
    <div v-else class="stack-lg appear">
      <div class="grid-2 grid-7-5">
        <div class="card card-dark hero-card">
          <div class="blob"></div>
          <ProgressRing :value="d.readiness.index" :size="190" :stroke="16" sub="preparación"/>
          <div style="position:relative">
            <span class="badge badge-lime">Índice de preparación crediticia</span>
            <h3 class="mt-2">{{ d.readiness.label }}</h3>
            <p class="muted mt-1 small">Combina tu situación financiera, tu ruta, lo que has aprendido y tus hábitos.</p>
            <div class="components">
              <div v-for="c in d.readiness.components" :key="c.key">
                <div class="row-between xs" style="margin-bottom:5px"><span>{{ c.label }}</span><strong>{{ c.value }}%</strong></div>
                <Bar :value="c.value" small/>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-head"><div class="card-title">🗺️ Mi ruta</div><router-link to="/mi-plan" class="btn btn-soft btn-sm">Ver todo</router-link></div>
          <div class="row-between"><span class="big-number">{{ d.plan.pct }}%</span><span class="muted small">{{ d.plan.completed }} de {{ d.plan.total }} pasos</span></div>
          <div class="mini-steps"><div v-for="s in d.plan.steps" :key="s.title" :class="s.status" :title="s.title"></div></div>
          <div class="next-task mt-3" v-if="d.plan.next_task">
            <div class="ico">🎯</div>
            <div style="min-width:0">
              <div class="xs muted bold">PRÓXIMO OBJETIVO · {{ d.plan.next_task.step_title }}</div>
              <div class="bold">{{ d.plan.next_task.title }}</div>
            </div>
          </div>
          <div class="next-task mt-3" v-else><div class="ico">🏆</div><div class="bold">¡Completaste toda tu ruta!</div></div>
          <router-link v-if="d.plan.next_task" :to="d.plan.next_task.lesson_slug ? '/aprende/' + d.plan.next_task.lesson_slug : (d.plan.next_task.action_route || '/mi-plan')" class="btn btn-primary btn-block mt-3">Continuar <Icon name="arrowRight" :size="18"/></router-link>
        </div>
      </div>

      <div class="grid-3">
        <div class="card">
          <div class="card-head"><div class="card-title">💡 Acción recomendada</div></div>
          <h3 style="font-size:19px;font-weight:800">{{ d.recommended.product || d.recommended.title }}</h3>
          <p class="text-2 small mt-1">{{ d.recommended.text }}</p>
          <div v-if="d.recommended.checklist.length" class="mt-2"><div class="xs bold muted">ANTES DE HACERLO:</div>
            <ul class="check-list small"><li v-for="c in d.recommended.checklist" :key="c">{{ c }}</li></ul>
          </div>
          <router-link :to="d.recommended.route" class="btn btn-soft btn-sm mt-3">Aprende cómo hacerlo →</router-link>
        </div>

        <div class="card">
          <div class="card-head"><div class="card-title">📅 Próximos recordatorios</div><router-link to="/recordatorios" class="icon-btn" aria-label="Recordatorios"><Icon name="plus"/></router-link></div>
          <div class="list" v-if="d.reminders.length">
            <div v-for="r in d.reminders" :key="r.id" class="list-item">
              <span class="dot" :class="r.status"></span>
              <div style="flex:1;min-width:0"><div class="bold small">{{ REMINDER_KINDS[r.kind].icon }} {{ r.title }}</div><div class="xs muted">{{ relDays(r.days_left) }}<span v-if="r.amount"> · {{ cop(r.amount) }}</span></div></div>
            </div>
          </div>
          <div v-else class="empty" style="padding:20px"><div class="small">Sin recordatorios pendientes</div><router-link to="/recordatorios" class="btn btn-soft btn-sm mt-2">Crear uno</router-link></div>
        </div>

        <div class="card">
          <div class="card-head"><div class="card-title">⚡ Actividad semanal</div><span class="badge">{{ d.week.reduce((a, w) => a + w.xp, 0) }} XP</span></div>
          <div class="week">
            <div v-for="w in d.week" :key="w.date" class="col">
              <div class="b" :class="{ zero: !w.xp }" :style="{ height: Math.max(4, (w.xp / maxWeek) * 90) + 'px' }" :title="w.xp + ' XP'"></div>
              <span class="xs muted bold">{{ w.label }}</span>
            </div>
          </div>
          <div class="mt-3">
            <div class="row-between xs"><span class="bold">{{ d.level.name }}</span><span class="muted" v-if="d.level.next_xp">{{ d.level.xp }} / {{ d.level.next_xp }} XP → {{ d.level.next_name }}</span></div>
            <Bar :value="d.level.pct" small class="mt-1"/>
          </div>
        </div>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="card-head"><div class="card-title">📚 Educación aplicada</div><router-link to="/aprende" class="btn btn-soft btn-sm">Ir a Aprende</router-link></div>
          <div class="row" style="gap:20px">
            <ProgressRing :value="d.learning.pct" :size="100" :stroke="10"/>
            <div><div class="bold" style="font-size:18px">{{ d.learning.completed }} de {{ d.learning.total }} lecciones</div>
              <p class="muted small mt-1">Cada lección dura menos de 6 minutos e incluye un quiz para ganar XP.</p></div>
          </div>
        </div>
        <div class="card">
          <div class="card-head"><div class="card-title">🕒 Actividad reciente</div></div>
          <div class="list">
            <div v-for="(a, i) in d.activity" :key="i" class="list-item">
              <span class="dot"></span><div style="flex:1" class="small">{{ a.description }}</div>
              <span class="xs muted">{{ timeAgo(a.created_at) }}</span><span v-if="a.xp" class="badge">+{{ a.xp }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>`,
};

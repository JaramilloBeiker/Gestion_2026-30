import { computed, onMounted, ref } from "vue";
import { api } from "../api.js";
import { GOALS_LABELS, SEGMENTS } from "../utils.js";

const LEVEL_COLORS = ["#ef4444", "#f59e0b", "#22c55e", "#047857"];

export default {
  setup() {
    const o = ref(null);
    onMounted(async () => { o.value = await api.get("/admin/overview"); });
    const maxNeed = computed(() => Math.max(1, ...(o.value?.top_needs.map((n) => n.count) || [1])));
    const maxSignup = computed(() => Math.max(1, ...(o.value?.signups.map((n) => n.count) || [1])));
    const levelTotal = computed(() => o.value?.levels.reduce((a, l) => a + l.count, 0) || 1);
    const donut = computed(() => {
      if (!o.value) return [];
      let acc = 0;
      const C = 2 * Math.PI * 60;
      return o.value.levels.map((l, i) => {
        const frac = l.count / levelTotal.value;
        const seg = { ...l, color: LEVEL_COLORS[i], dash: `${frac * C} ${C}`, offset: -acc * C, pct: Math.round(frac * 100) };
        acc += frac;
        return seg;
      });
    });
    return { o, maxNeed, maxSignup, donut, GOALS_LABELS, SEGMENTS };
  },
  template: `
  <div>
    <Loading v-if="!o" :count="2"/>
    <div v-else class="stack-lg appear">
      <div class="page-head">
        <div><h2>{{ o.institution.name }}</h2><p>Licencia institucional · código <strong>{{ o.institution.code }}</strong> · Métricas agregadas y anónimas de tus estudiantes.</p></div>
        <span class="badge badge-lime" style="font-size:13px;padding:6px 14px">🎓 Piloto activo</span>
      </div>

      <div class="grid-4">
        <div class="card"><div class="xs bold muted">ESTUDIANTES ACTIVADOS</div><div class="big-number">{{ o.students }}</div>
          <Bar :value="o.students / o.institution.seats * 100" small class="mt-2"/><div class="xs muted mt-1">{{ o.students }} de {{ o.institution.seats }} licencias</div></div>
        <div class="card"><div class="xs bold muted">ACTIVOS ESTA SEMANA</div><div class="big-number">{{ o.active_week }}</div>
          <div class="xs muted mt-1">{{ o.students ? Math.round(o.active_week / o.students * 100) : 0 }}% de los estudiantes</div></div>
        <div class="card"><div class="xs bold muted">PREPARACIÓN PROMEDIO</div><div class="big-number" style="color:var(--primary)">{{ o.avg_readiness }}%</div>
          <div class="xs muted mt-1">Índice de preparación crediticia</div></div>
        <div class="card"><div class="xs bold muted">DIAGNÓSTICO PROMEDIO</div><div class="big-number">{{ o.avg_diagnostic }}<span class="muted" style="font-size:18px">/100</span></div>
          <div class="xs muted mt-1">Situación financiera inicial</div></div>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="card-title" style="margin-bottom:16px">🧭 Nivel de los estudiantes</div>
          <div class="row wrap" style="gap:28px">
            <svg width="160" height="160" viewBox="0 0 160 160" style="transform:rotate(-90deg)">
              <circle cx="80" cy="80" r="60" fill="none" stroke="var(--border)" stroke-width="22"/>
              <circle v-for="s in donut" :key="s.label" cx="80" cy="80" r="60" fill="none" :stroke="s.color" stroke-width="22" :stroke-dasharray="s.dash" :stroke-dashoffset="s.offset"/>
            </svg>
            <div class="donut-legend">
              <div v-for="s in donut" :key="s.label"><span class="sw" :style="{ background: s.color }"></span>{{ s.label }} · <strong>{{ s.count }}</strong> <span class="muted">({{ s.pct }}%)</span></div>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="card-title" style="margin-bottom:16px">🎯 Principales necesidades detectadas</div>
          <div v-for="n in o.top_needs" :key="n.label" class="hbar">
            <span class="small" style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap" :title="n.label">{{ n.label }}</span>
            <Bar :value="n.count / maxNeed * 100"/><strong class="small">{{ n.count }}</strong>
          </div>
          <p class="xs muted mt-2">Úsalo para planear talleres de Bienestar Universitario.</p>
        </div>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="card-title" style="margin-bottom:16px">📚 Avance por módulo</div>
          <div v-for="m in o.modules" :key="m.title" class="hbar" style="grid-template-columns: 1fr 120px 44px">
            <span class="small">{{ m.icon }} {{ m.title }}</span><Bar :value="m.pct"/><strong class="small">{{ m.pct }}%</strong>
          </div>
        </div>
        <div class="card">
          <div class="card-title">📈 Nuevos registros por semana</div>
          <div class="vbars">
            <div v-for="w in o.signups" :key="w.label" class="col">
              <strong style="color:var(--text)">{{ w.count }}</strong>
              <div class="b" :style="{ height: Math.max(3, w.count / maxSignup * 110) + 'px' }"></div>
              <span>{{ w.label }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="card-title" style="margin-bottom:12px">👥 Segmentos</div>
          <div class="list"><div v-for="s in o.segments" :key="s.label" class="list-item"><span class="dot"></span><span style="flex:1">{{ SEGMENTS[s.label] || s.label }}</span><strong>{{ s.count }}</strong></div></div>
        </div>
        <div class="card">
          <div class="card-title" style="margin-bottom:12px">🚀 Metas principales</div>
          <div class="list"><div v-for="g in o.goals" :key="g.label" class="list-item"><span class="dot"></span><span style="flex:1">{{ GOALS_LABELS[g.label] || g.label }}</span><strong>{{ g.count }}</strong></div></div>
        </div>
      </div>
      <p class="xs muted">🔒 Por privacidad (Ley 1581 de 2012), este panel muestra solo información agregada. Ningún dato individual de los estudiantes es visible para la institución.</p>
    </div>
  </div>`,
};

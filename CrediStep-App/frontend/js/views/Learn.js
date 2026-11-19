import { computed, onMounted, ref } from "vue";
import { api } from "../api.js";

export default {
  setup() {
    const modules = ref(null);
    onMounted(async () => { modules.value = await api.get("/learning/modules"); });
    const totals = computed(() => {
      if (!modules.value) return { done: 0, total: 0 };
      return modules.value.reduce((a, m) => ({ done: a.done + m.completed, total: a.total + m.total }), { done: 0, total: 0 });
    });
    return { modules, totals };
  },
  template: `
  <div>
    <div class="page-head">
      <div><h2>Educación aplicada</h2><p>No solo “¿qué es una tarjeta de crédito?”, sino “¿qué significa para ti y cómo deberías usarla?”.</p></div>
      <span class="chip-stat" v-if="modules">📚 {{ totals.done }}/{{ totals.total }} lecciones</span>
    </div>
    <Loading v-if="!modules" :count="2"/>
    <div v-else class="grid-2 appear">
      <div v-for="m in modules" :key="m.slug" class="card module-card">
        <div class="row" style="gap:16px">
          <div class="m-ico" :style="{ background: m.color + '22' }">{{ m.icon }}</div>
          <div style="flex:1;min-width:0">
            <h3 style="font-size:18px;font-weight:800">{{ m.title }}</h3>
            <p class="muted small">{{ m.description }}</p>
          </div>
        </div>
        <div class="row mt-3" style="gap:10px"><Bar :value="m.pct" small style="flex:1"/><span class="xs bold">{{ m.completed }}/{{ m.total }}</span></div>
        <div class="mt-2">
          <router-link v-for="(l, i) in m.lessons" :key="l.slug" :to="l.locked ? '/plus' : '/aprende/' + l.slug"
            class="lesson-row" :class="{ completed: l.completed, locked: l.locked }">
            <span class="num">{{ l.completed ? '✓' : (l.locked ? '🔒' : i + 1) }}</span>
            <div style="flex:1;min-width:0">
              <div class="bold">{{ l.title }}</div>
              <div class="xs muted">{{ l.minutes }} min · +{{ l.xp }} XP<span v-if="l.best_score !== null"> · Mejor quiz: {{ l.best_score }}%</span></div>
            </div>
            <span v-if="l.premium" class="badge badge-lime">PLUS</span>
            <Icon name="chevron" :size="18" class="muted"/>
          </router-link>
        </div>
      </div>
    </div>
  </div>`,
};

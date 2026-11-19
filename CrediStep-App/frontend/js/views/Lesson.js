import { ref, watch } from "vue";
import { api, refreshUser } from "../api.js";
import { store } from "../store.js";

export default {
  props: { slug: String },
  setup(props) {
    const lesson = ref(null);
    const locked = ref(false);
    const selected = ref([]);
    const result = ref(null);
    const busy = ref(false);

    async function load() {
      lesson.value = null;
      result.value = null;
      locked.value = false;
      try {
        lesson.value = await api.get(`/learning/lessons/${props.slug}`);
        selected.value = lesson.value.quiz.map(() => null);
      } catch (e) {
        if (e.status === 402) locked.value = true;
        else store.toast(e.message, { type: "error" });
      }
    }
    watch(() => props.slug, load, { immediate: true });

    function choose(qi, oi) {
      if (result.value) return;
      selected.value[qi] = oi;
    }
    function optionClass(qi, oi) {
      if (!result.value) return { selected: selected.value[qi] === oi };
      const r = result.value.results[qi];
      if (oi === r.correct_index) return { correct: true };
      if (selected.value[qi] === oi) return { wrong: true };
      return {};
    }
    async function submit() {
      busy.value = true;
      try {
        result.value = await api.post(`/learning/lessons/${props.slug}/quiz`, { answers: selected.value });
        if (result.value.xp_earned) {
          store.toast("¡Lección completada!", { xp: result.value.xp_earned, icon: "🎉" });
          refreshUser();
        }
      } catch (e) {
        store.toast(e.message, { type: "error" });
      } finally {
        busy.value = false;
      }
    }
    function retry() {
      result.value = null;
      selected.value = lesson.value.quiz.map(() => null);
    }
    return { lesson, locked, selected, result, busy, choose, optionClass, submit, retry };
  },
  template: `
  <div class="lesson-body">
    <router-link to="/aprende" class="muted small row" style="gap:4px;margin-bottom:16px"><Icon name="chevronLeft" :size="16"/> Volver a Aprende</router-link>
    <PremiumLock v-if="locked" title="Lección de CrediStep Plus" text="Las lecciones avanzadas te dan estrategias paso a paso para llevar tu historial al siguiente nivel."/>
    <Loading v-else-if="!lesson" :height="300"/>
    <article v-else class="appear">
      <header class="lesson-hero">
        <div class="grid-lines"></div>
        <div style="position:relative">
          <span class="badge badge-lime">{{ lesson.module.icon }} {{ lesson.module.title }}</span>
          <h2>{{ lesson.title }}</h2>
          <p class="mt-1" style="opacity:.85;font-size:17px">{{ lesson.summary }}</p>
          <div class="row mt-3 small" style="opacity:.85"><span>⏱ {{ lesson.minutes }} min</span><span>⭐ +{{ lesson.xp }} XP</span><span v-if="lesson.completed">✅ Completada</span></div>
        </div>
      </header>

      <div v-for="(b, i) in lesson.blocks" :key="i" class="block">
        <p v-if="b.type === 'text'" class="block-text">{{ b.text }}</p>
        <div v-else-if="b.type === 'tip'" class="block-tip"><div class="block-label" style="color:var(--primary)">💡 Tip CrediStep</div>{{ b.text }}</div>
        <div v-else-if="b.type === 'warning'" class="block-warning"><div class="block-label" style="color:#b45309">⚠️ Ojo</div>{{ b.text }}</div>
        <div v-else-if="b.type === 'example'" class="block-example"><div class="block-label" style="color:var(--primary)">🎬 {{ b.title }}</div>{{ b.text }}</div>
        <div v-else-if="b.type === 'stat'" class="block-stat"><strong>{{ b.value }}</strong><span>{{ b.text }}</span></div>
        <div v-else-if="b.type === 'list'" class="block-list"><div class="bold">{{ b.title }}</div><ul><li v-for="it in b.items" :key="it">{{ it }}</li></ul></div>
      </div>

      <section class="card mt-4">
        <div class="row-between"><div class="card-title">🧠 Pon a prueba lo aprendido</div><span class="badge badge-muted">Aprueba con 60 %</span></div>
        <div v-for="(q, qi) in lesson.quiz" :key="q.id" class="mt-3">
          <div class="bold" style="font-size:16px">{{ qi + 1 }}. {{ q.question }}</div>
          <div class="stack mt-2" style="gap:8px">
            <button v-for="(o, oi) in q.options" :key="oi" class="quiz-option" :class="optionClass(qi, oi)" :disabled="!!result" @click="choose(qi, oi)">
              <span class="letter">{{ 'ABCD'[oi] }}</span>{{ o }}
            </button>
          </div>
          <p v-if="result" class="small mt-1" :style="{ color: result.results[qi].correct ? 'var(--primary)' : 'var(--danger)' }">
            {{ result.results[qi].correct ? '¡Correcto! ' : 'No exactamente. ' }}<span class="text-2">{{ result.results[qi].explanation }}</span>
          </p>
        </div>

        <div v-if="result" class="next-task mt-4">
          <div class="ico">{{ result.passed ? '🎉' : '💪' }}</div>
          <div style="flex:1"><div class="bold">{{ result.passed ? '¡Aprobaste con ' + result.score + '%!' : 'Obtuviste ' + result.score + '%. ¡Inténtalo de nuevo!' }}</div>
            <div class="small muted" v-if="result.xp_earned">Ganaste {{ result.xp_earned }} XP y avanzaste en tu ruta.</div></div>
          <button v-if="!result.passed" class="btn btn-soft btn-sm" @click="retry">Reintentar</button>
        </div>
        <div class="row-between mt-3 wrap">
          <button v-if="!result" class="btn btn-primary" :disabled="busy || selected.some(s => s === null)" @click="submit">Revisar respuestas</button>
          <span v-else></span>
          <router-link v-if="result && lesson.next" :to="lesson.next.locked ? '/plus' : '/aprende/' + lesson.next.slug" class="btn btn-primary">
            Siguiente: {{ lesson.next.title }} <Icon name="arrowRight" :size="18"/>
          </router-link>
          <router-link v-else-if="result" to="/mi-plan" class="btn btn-primary">Volver a mi ruta</router-link>
        </div>
      </section>
    </article>
  </div>`,
};

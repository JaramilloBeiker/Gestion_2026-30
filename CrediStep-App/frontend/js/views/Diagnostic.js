import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { api, refreshUser } from "../api.js";
import { store } from "../store.js";

export default {
  setup() {
    const router = useRouter();
    const questions = ref([]);
    const idx = ref(0);
    const answers = reactive({});
    const busy = ref(false);
    const error = ref("");
    const started = ref(false);

    onMounted(async () => {
      questions.value = await api.get("/diagnostic/questions");
      const prev = await api.get("/diagnostic/latest").catch(() => null);
      if (prev) Object.assign(answers, prev.answers);
    });

    const q = computed(() => questions.value[idx.value]);
    const progress = computed(() => (questions.value.length ? ((idx.value + 1) / questions.value.length) * 100 : 0));
    const canNext = computed(() => {
      const a = answers[q.value?.id];
      return Array.isArray(a) ? a.length > 0 : a !== undefined && a !== null && a !== "";
    });

    function isSelected(value) {
      const a = answers[q.value.id];
      return Array.isArray(a) ? a.includes(value) : a === value;
    }
    function pick(value) {
      const id = q.value.id;
      if (q.value.type === "multi") {
        let list = Array.isArray(answers[id]) ? [...answers[id]] : [];
        if (value === "ninguno") list = list.includes("ninguno") ? [] : ["ninguno"];
        else {
          list = list.filter((v) => v !== "ninguno");
          list = list.includes(value) ? list.filter((v) => v !== value) : [...list, value];
        }
        answers[id] = list;
      } else {
        answers[id] = value;
        setTimeout(() => { if (idx.value < questions.value.length - 1) idx.value++; }, 260);
      }
    }
    async function next() {
      if (idx.value < questions.value.length - 1) { idx.value++; return; }
      busy.value = true;
      error.value = "";
      try {
        const res = await api.post("/diagnostic", { answers: { ...answers } });
        await refreshUser();
        store.toast("¡Diagnóstico completo!", { xp: 50, icon: "🧭" });
        router.push({ path: "/diagnostico/resultado", query: { nuevo: res.id } });
      } catch (e) {
        error.value = e.message;
      } finally {
        busy.value = false;
      }
    }
    function back() {
      if (idx.value > 0) idx.value--;
      else if (store.user?.onboarded) router.push("/inicio");
      else started.value = false;
    }
    return { store, questions, idx, q, answers, progress, canNext, isSelected, pick, next, back, busy, error, started };
  },
  template: `
  <div class="wizard">
    <div class="wizard-top">
      <router-link to="/" class="brand" style="padding:0;color:var(--text)"><img src="/assets/img/logo.svg" alt="" style="width:34px"/></router-link>
      <div style="flex:1" v-if="started && questions.length">
        <div class="row-between small bold" style="margin-bottom:6px"><span>DIAGNÓSTICO</span><span class="muted">Pregunta {{ idx + 1 }} de {{ questions.length }}</span></div>
        <Bar :value="progress"/>
      </div>
      <div style="flex:1" v-else></div>
      <router-link v-if="store.user?.onboarded" to="/inicio" class="icon-btn" aria-label="Salir"><Icon name="x"/></router-link>
    </div>

    <div class="wizard-body">
      <div v-if="!started" class="wizard-card center appear">
        <div style="font-size:64px">🧭</div>
        <h2 class="mt-2">Conozcamos tu situación, {{ store.user?.name?.split(' ')[0] }}</h2>
        <p class="muted mt-2" style="font-size:17px;max-width:520px;margin-inline:auto">Responde 7 preguntas sencillas sobre tus finanzas. Con esto armamos tu ruta personalizada. Toma menos de 2 minutos y no hay respuestas malas.</p>
        <button class="btn btn-primary btn-lg mt-4" @click="started = true" :disabled="!questions.length">Empezar diagnóstico <Icon name="arrowRight" :size="18"/></button>
        <p class="xs muted mt-3">🔒 Tus respuestas son privadas y solo se usan para personalizar tu ruta.</p>
      </div>

      <transition name="slide" mode="out-in" v-else-if="q">
        <div class="wizard-card" :key="q.id">
          <h2>{{ q.title }}</h2>
          <p class="muted mt-1" style="font-size:16px">{{ q.subtitle }}</p>

          <div v-if="q.type === 'scale'" class="mt-4">
            <div class="scale">
              <button v-for="n in 5" :key="n" :class="{ selected: answers[q.id] === n }" @click="pick(n)">{{ n }}</button>
            </div>
            <div class="row-between small muted mt-2"><span>No sé nada</span><span>Lo conozco muy bien</span></div>
          </div>
          <div v-else class="stack mt-3">
            <button v-for="o in q.options" :key="o.value" class="option" :class="{ selected: isSelected(o.value) }" @click="pick(o.value)">
              <span class="emoji">{{ o.icon }}</span>{{ o.label }}<span class="tick"><Icon name="check" :size="14" :stroke="3"/></span>
            </button>
          </div>

          <div v-if="error" class="error-box mt-2">{{ error }}</div>
          <div class="row-between mt-4">
            <button class="btn btn-ghost" @click="back"><Icon name="chevronLeft" :size="18"/> Atrás</button>
            <button class="btn btn-primary" :disabled="!canNext || busy" @click="next">
              {{ idx === questions.length - 1 ? (busy ? 'Calculando…' : 'Ver mi diagnóstico') : 'Siguiente' }} <Icon name="arrowRight" :size="18"/>
            </button>
          </div>
        </div>
      </transition>
    </div>
  </div>`,
};

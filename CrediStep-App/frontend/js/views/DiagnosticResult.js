import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { api } from "../api.js";
import { fmtDate } from "../utils.js";

export default {
  setup() {
    const router = useRouter();
    const result = ref(null);
    const history = ref([]);
    onMounted(async () => {
      try {
        [result.value, history.value] = await Promise.all([api.get("/diagnostic/latest"), api.get("/diagnostic/history")]);
      } catch {
        router.replace("/diagnostico");
      }
    });
    return { result, history, fmtDate };
  },
  template: `
  <div>
    <Loading v-if="!result" :height="380"/>
    <div v-else class="grid-2 appear" style="align-items:start">
      <div class="card card-dark center" style="padding:36px">
        <span class="badge badge-lime">TU PERFIL</span>
        <div class="mt-3"><ProgressRing :value="result.score" :size="210" :stroke="16" :sub="result.level" light/></div>
        <h3 class="mt-3" style="font-size:22px;color:#fff">{{ result.message }}</h3>
        <p class="muted small mt-1">Diagnóstico del {{ fmtDate(result.created_at, { day: 'numeric', month: 'long', year: 'numeric' }) }}</p>
        <div class="row wrap mt-4" style="justify-content:center">
          <router-link to="/mi-plan" class="btn btn-lime btn-lg">VER MI PLAN <Icon name="arrowRight" :size="18"/></router-link>
          <router-link to="/diagnostico" class="btn btn-glass"><Icon name="refresh" :size="16"/> Repetir</router-link>
        </div>
      </div>

      <div class="stack-lg">
        <div class="card">
          <div class="card-title">💪 Lo que ya haces bien</div>
          <ul class="result-list mt-2">
            <li v-for="s in result.strengths" :key="s" class="ok"><span class="ri">✓</span>{{ s }}</li>
            <li v-if="!result.strengths.length" class="muted">Aún no hay fortalezas registradas: ¡tu ruta te ayudará a construirlas!</li>
          </ul>
        </div>
        <div class="card">
          <div class="card-title">🎯 Lo que vamos a trabajar</div>
          <ul class="result-list mt-2">
            <li v-for="s in result.improvements" :key="s" class="ko"><span class="ri">!</span>{{ s }}</li>
          </ul>
        </div>
        <div class="card" v-if="history.length > 1">
          <div class="card-title">📈 Tu evolución</div>
          <div class="vbars mt-2">
            <div v-for="(h, i) in history" :key="i" class="col">
              <strong style="color:var(--text)">{{ h.score }}</strong>
              <div class="b" :style="{ height: h.score + '%' }"></div>
              <span>{{ fmtDate(h.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>`,
};

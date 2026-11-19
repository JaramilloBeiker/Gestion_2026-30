import { computed, onMounted, ref } from "vue";
import { api } from "../api.js";

const norm = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();

export default {
  setup() {
    const terms = ref([]);
    const q = ref("");
    onMounted(async () => { terms.value = await api.get("/glossary"); });
    const filtered = computed(() => {
      const s = norm(q.value.trim());
      return s ? terms.value.filter((t) => norm(t.term + " " + t.definition).includes(s)) : terms.value;
    });
    return { q, filtered, terms };
  },
  template: `
  <div>
    <div class="page-head">
      <div><h2>Glosario financiero</h2><p>Los términos que vas a escuchar en el banco, traducidos a lenguaje sencillo.</p></div>
    </div>
    <div class="card" style="padding:14px 18px;margin-bottom:20px">
      <div class="row"><Icon name="search" class="muted"/><input class="input" style="border:0;box-shadow:none;padding:6px 0" v-model="q" placeholder="Busca un término: cupo, usura, fecha de corte…" aria-label="Buscar"/></div>
    </div>
    <div class="grid-3 appear">
      <div v-for="t in filtered" :key="t.term" class="card card-hover">
        <h3 style="font-size:17px;font-weight:800;color:var(--primary)">{{ t.term }}</h3>
        <p class="text-2 small mt-1">{{ t.definition }}</p>
      </div>
    </div>
    <div v-if="terms.length && !filtered.length" class="card empty"><div class="e-ico">🔍</div><p>No encontramos ese término. Prueba preguntándole a Step 💬</p></div>
  </div>`,
};

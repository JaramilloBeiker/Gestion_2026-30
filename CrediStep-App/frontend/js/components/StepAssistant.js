import { nextTick, ref } from "vue";
import { api } from "../api.js";
import { store } from "../store.js";

export default {
  setup() {
    const open = ref(false);
    const input = ref("");
    const busy = ref(false);
    const box = ref(null);
    const firstName = (store.user?.name || "").split(" ")[0];
    const messages = ref([
      { from: "bot", text: `¡Hola${firstName ? " " + firstName : ""}! Soy Step 🌱, tu copiloto financiero. Pregúntame lo que quieras sobre crédito, en lenguaje sencillo.` },
    ]);
    const suggestions = ["¿Cómo empiezo mi historial?", "¿Cuánto cupo debo usar?", "¿Qué pasa si me atraso?", "¿Qué es la tasa E.A.?"];

    async function scroll() {
      await nextTick();
      if (box.value) box.value.scrollTop = box.value.scrollHeight;
    }
    async function ask(q) {
      const question = (q ?? input.value).trim();
      if (!question || busy.value) return;
      messages.value.push({ from: "me", text: question });
      input.value = "";
      busy.value = true;
      scroll();
      try {
        const r = await api.post("/assistant/ask", { question });
        messages.value.push({ from: "bot", text: r.answer, lesson: r.lesson });
      } catch (e) {
        messages.value.push({ from: "bot", text: e.message });
      } finally {
        busy.value = false;
        scroll();
      }
    }
    return { open, input, busy, box, messages, suggestions, ask };
  },
  template: `
  <div>
    <transition name="fade">
      <section v-if="open" class="step-panel" aria-label="Asistente Step">
        <div class="step-head">
          <div class="av">S</div>
          <div style="flex:1"><strong>Step</strong><div class="xs" style="opacity:.75">Asistente educativo · no da asesoría de inversión</div></div>
          <button class="icon-btn" style="color:#fff" @click="open = false" aria-label="Cerrar"><Icon name="x"/></button>
        </div>
        <div class="step-msgs" ref="box">
          <div v-for="(m, i) in messages" :key="i" class="msg" :class="m.from">
            {{ m.text }}
            <div v-if="m.lesson" class="mt-1"><router-link :to="'/aprende/' + m.lesson" class="bold small" @click="open = false">Ver lección →</router-link></div>
          </div>
          <div v-if="busy" class="msg bot">Step está escribiendo…</div>
        </div>
        <div class="step-suggest" v-if="messages.length < 3">
          <button v-for="s in suggestions" :key="s" @click="ask(s)">{{ s }}</button>
        </div>
        <form class="step-input" @submit.prevent="ask()">
          <input class="input" v-model="input" placeholder="Escribe tu pregunta…" maxlength="300" aria-label="Pregunta"/>
          <button class="btn btn-primary" style="padding:10px 14px" :disabled="busy" aria-label="Enviar"><Icon name="send" :size="18"/></button>
        </form>
      </section>
    </transition>
    <button class="step-fab" @click="open = !open" :aria-label="open ? 'Cerrar asistente' : 'Abrir asistente Step'">
      <Icon :name="open ? 'x' : 'chat'" :size="26"/>
      <span v-if="!open" class="ping"></span>
    </button>
  </div>`,
};

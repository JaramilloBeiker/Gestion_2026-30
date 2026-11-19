import { computed, onMounted, ref, watch } from "vue";
import { store } from "../store.js";

const ICONS = {
  home: "M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z",
  map: "M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2zM9 4v14M15 6v14",
  book: "M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2zM22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z",
  calc: "M6 2h12a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zM8 6h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15v4M8 19h.01M12 19h.01",
  target: "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 18a6 6 0 1 0 0-12 6 6 0 0 0 0 12zM12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4z",
  bell: "M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9M10.3 21a1.94 1.94 0 0 0 3.4 0",
  user: "M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z",
  sparkles: "M12 3l1.9 5.8L20 10l-6.1 1.2L12 17l-1.9-5.8L4 10l6.1-1.2zM19 15l.7 2 2 .7-2 .7-.7 2-.7-2-2-.7 2-.7z",
  logout: "M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9",
  check: "M20 6 9 17l-5-5",
  chevron: "M9 18l6-6-6-6",
  chevronLeft: "M15 18l-6-6 6-6",
  shield: "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z",
  search: "M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16zM21 21l-4.35-4.35",
  send: "M22 2 11 13M22 2l-7 20-4-9-9-4z",
  x: "M18 6 6 18M6 6l12 12",
  plus: "M12 5v14M5 12h14",
  trash: "M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6",
  sun: "M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10zM12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4",
  moon: "M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z",
  building: "M3 21h18M5 21V7l8-4v18M19 21V11l-6-4M9 9v.01M9 12v.01M9 15v.01M9 18v.01",
  menu: "M3 6h18M3 12h18M3 18h18",
  lock: "M5 11h14v10H5zM8 11V7a4 4 0 0 1 8 0v4",
  flame: "M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3a2.5 2.5 0 0 0 2.5 2.5z",
  trophy: "M6 9H4.5a2.5 2.5 0 0 1 0-5H6M18 9h1.5a2.5 2.5 0 0 0 0-5H18M4 22h16M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22M18 2H6v7a6 6 0 0 0 12 0V2z",
  chat: "M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z",
  edit: "M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z",
  arrowRight: "M5 12h14M12 5l7 7-7 7",
  clock: "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 6v6l4 2",
  chart: "M3 3v18h18M8 17v-5M13 17V8M18 17v-9",
  crown: "M2 19h20M3 7l5 5 4-7 4 7 5-5-2 12H5z",
  compass: "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM16.24 7.76l-2.12 6.36-6.36 2.12 2.12-6.36z",
  refresh: "M21 12a9 9 0 1 1-3-6.7L21 8M21 3v5h-5",
};

export const Icon = {
  props: { name: String, size: { type: [Number, String], default: 20 }, stroke: { type: Number, default: 2 } },
  setup(props) {
    const d = computed(() => ICONS[props.name] || ICONS.sparkles);
    return { d };
  },
  template: `<svg :width="size" :height="size" viewBox="0 0 24 24" fill="none" stroke="currentColor"
    :stroke-width="stroke" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path :d="d"/></svg>`,
};

let ringId = 0;
export const ProgressRing = {
  props: {
    value: { type: Number, default: 0 },
    size: { type: Number, default: 160 },
    stroke: { type: Number, default: 14 },
    label: String,
    sub: String,
    light: Boolean,
  },
  setup(props) {
    const id = `ring-grad-${++ringId}`;
    const r = computed(() => (props.size - props.stroke) / 2);
    const circ = computed(() => 2 * Math.PI * r.value);
    const shown = ref(0);
    onMounted(() => requestAnimationFrame(() => (shown.value = props.value)));
    watch(() => props.value, (v) => (shown.value = v));
    const offset = computed(() => circ.value * (1 - Math.min(Math.max(shown.value, 0), 100) / 100));
    return { id, r, circ, offset };
  },
  template: `
    <div class="ring" :style="{ width: size + 'px', height: size + 'px', fontSize: (size / 9) + 'px' }">
      <svg :width="size" :height="size">
        <defs><linearGradient :id="id" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#bef264"/><stop offset="100%" stop-color="#10b981"/>
        </linearGradient></defs>
        <circle class="ring-track" :cx="size/2" :cy="size/2" :r="r" :stroke-width="stroke" fill="none"/>
        <circle class="ring-value" :cx="size/2" :cy="size/2" :r="r" :stroke-width="stroke" fill="none"
          :stroke="'url(#' + id + ')'" stroke-linecap="round" :stroke-dasharray="circ" :stroke-dashoffset="offset"/>
      </svg>
      <div class="ring-label">
        <strong>{{ label ?? (Math.round(value) + '%') }}</strong>
        <span v-if="sub">{{ sub }}</span>
      </div>
    </div>`,
};

export const Bar = {
  props: { value: Number, small: Boolean },
  template: `<div class="bar" :class="{ 'bar-sm': small }"><span :style="{ width: Math.min(Math.max(value || 0, 0), 100) + '%' }"></span></div>`,
};

export const Modal = {
  props: { title: String },
  emits: ["close"],
  template: `
    <div class="modal-back" @click.self="$emit('close')">
      <div class="modal" role="dialog" aria-modal="true">
        <div class="row-between" style="margin-bottom:18px">
          <h3 style="font-size:20px;font-weight:800">{{ title }}</h3>
          <button class="icon-btn" @click="$emit('close')" aria-label="Cerrar"><Icon name="x"/></button>
        </div>
        <slot/>
      </div>
    </div>`,
};

export const Toasts = {
  setup() { return { store }; },
  template: `
    <div class="toasts" aria-live="polite">
      <div v-for="t in store.toasts" :key="t.id" class="toast" :class="t.type">
        <span>{{ t.type === 'error' ? '⚠️' : t.icon }}</span><span>{{ t.message }}</span>
        <span v-if="t.xp" class="xp">+{{ t.xp }} XP</span>
      </div>
    </div>`,
};

export const PremiumLock = {
  props: { title: { type: String, default: "Función de CrediStep Plus" }, text: String },
  template: `
    <div class="card lock-card appear">
      <div class="l-ico">👑</div>
      <h3 style="font-size:22px;font-weight:800">{{ title }}</h3>
      <p class="muted mt-1" style="max-width:420px;margin-inline:auto">{{ text || 'Desbloquea seguimiento detallado, simulador de puntaje, lecciones avanzadas y metas ilimitadas por $20.000 al mes.' }}</p>
      <router-link to="/plus" class="btn btn-primary mt-3"><Icon name="crown" :size="18"/> Conocer CrediStep Plus</router-link>
    </div>`,
};

export const Loading = {
  props: { height: { type: Number, default: 220 }, count: { type: Number, default: 1 } },
  template: `<div class="stack-lg"><div v-for="i in count" :key="i" class="skeleton" :style="{ height: height + 'px' }"></div></div>`,
};

const copFormatter = new Intl.NumberFormat("es-CO", { style: "currency", currency: "COP", maximumFractionDigits: 0 });
const numFormatter = new Intl.NumberFormat("es-CO", { maximumFractionDigits: 1 });

export const cop = (n) => copFormatter.format(Math.round(Number(n) || 0));
export const num = (n) => numFormatter.format(Number(n) || 0);

export function fmtDate(iso, opts = { day: "numeric", month: "short" }) {
  if (!iso) return "";
  const d = new Date(iso.length === 10 ? `${iso}T12:00:00` : iso);
  return d.toLocaleDateString("es-CO", opts);
}

export function relDays(days) {
  if (days === 0) return "Hoy";
  if (days === 1) return "Mañana";
  if (days === -1) return "Ayer";
  if (days < 0) return `Hace ${-days} días`;
  return `En ${days} días`;
}

export function timeAgo(iso) {
  const diff = (Date.now() - new Date(iso).getTime()) / 1000;
  if (diff < 60) return "hace un momento";
  if (diff < 3600) return `hace ${Math.floor(diff / 60)} min`;
  if (diff < 86400) return `hace ${Math.floor(diff / 3600)} h`;
  const d = Math.floor(diff / 86400);
  return d === 1 ? "ayer" : `hace ${d} días`;
}

export function initials(name = "") {
  return name.split(" ").filter(Boolean).slice(0, 2).map((p) => p[0].toUpperCase()).join("");
}

export function todayISO(offsetDays = 0) {
  const d = new Date();
  d.setDate(d.getDate() + offsetDays);
  const pad = (x) => String(x).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

export const GOAL_CATEGORIES = {
  emergencia: { label: "Emergencia", icon: "🛟" },
  ahorro: { label: "Ahorro", icon: "🐷" },
  viaje: { label: "Viaje", icon: "✈️" },
  independencia: { label: "Independencia", icon: "🏠" },
  estudio: { label: "Estudio", icon: "📚" },
  compra: { label: "Compra importante", icon: "🛍️" },
};

export const REMINDER_KINDS = {
  pago: { label: "Pago", icon: "💳" },
  corte: { label: "Fecha de corte", icon: "📅" },
  ahorro: { label: "Ahorro", icon: "🐷" },
  habito: { label: "Hábito", icon: "🔁" },
};

export const SEGMENTS = {
  universitario: "Estudiante universitario",
  primer_empleo: "Primer empleo",
  meta_clara: "Joven con meta clara",
  sin_diagnostico: "Sin diagnóstico",
};

export const GOALS_LABELS = {
  primera_tarjeta: "Primera tarjeta o crédito",
  independizarme: "Independizarme",
  viajar: "Viajar",
  estudiar: "Financiar estudios",
  control: "Control de mi dinero",
};

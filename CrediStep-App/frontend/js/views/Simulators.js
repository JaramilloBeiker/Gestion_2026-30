import { onMounted, reactive, ref, watch } from "vue";
import { api } from "../api.js";
import { store } from "../store.js";
import { cop } from "../utils.js";

function debounce(fn, ms = 300) {
  let t;
  return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
}

export default {
  setup() {
    const tab = ref("cupo");
    const tabs = [
      { id: "cupo", label: "Uso de cupo", icon: "💳" },
      { id: "credito", label: "Costo de crédito", icon: "🧮" },
      { id: "atraso", label: "¿Y si me atraso?", icon: "⏰" },
      { id: "puntaje", label: "Puntaje", icon: "📊", plus: true },
    ];

    const util = reactive({ credit_limit: 1000000, balance: 250000 });
    const utilRes = ref(null);
    const loan = reactive({ amount: 1500000, ea_rate: 28, months: 12, monthly_fee: 0 });
    const loanRes = ref(null);
    const late = reactive({ installment: 150000, days_late: 45, default_ea_rate: 28 });
    const lateRes = ref(null);
    const score = reactive({ on_time_pct: 95, utilization_pct: 25, history_months: 12, inquiries_12m: 1, product_types: 1 });
    const scoreRes = ref(null);
    const scoreLocked = ref(false);

    const run = async (path, body, target) => {
      try { target.value = await api.post(path, { ...body }); }
      catch (e) {
        if (e.status === 402) scoreLocked.value = true;
        else if (e.status !== 422) store.toast(e.message, { type: "error" });
      }
    };
    const runUtil = debounce(() => run("/simulators/utilization", util, utilRes));
    const runLoan = debounce(() => run("/simulators/loan", loan, loanRes));
    const runLate = debounce(() => run("/simulators/late-payment", late, lateRes));
    const runScore = debounce(() => run("/simulators/score", score, scoreRes));
    watch(util, runUtil, { deep: true });
    watch(loan, runLoan, { deep: true });
    watch(late, runLate, { deep: true });
    watch(score, runScore, { deep: true });
    onMounted(() => {
      runUtil(); runLoan(); runLate();
      if (store.user?.is_premium) runScore(); else scoreLocked.value = true;
    });
    const scoreColor = (s) => (s >= 800 ? "#10b981" : s >= 700 ? "#22c55e" : s >= 550 ? "#f59e0b" : "#ef4444");
    return { tab, tabs, util, utilRes, loan, loanRes, late, lateRes, score, scoreRes, scoreLocked, cop, scoreColor, store };
  },
  template: `
  <div>
    <div class="page-head">
      <div><h2>Simuladores</h2><p>Experimenta antes de decidir. Son herramientas educativas: los resultados son aproximados.</p></div>
    </div>
    <div class="tabs" role="tablist">
      <button v-for="t in tabs" :key="t.id" class="tab" :class="{ active: tab === t.id }" @click="tab = t.id" role="tab">
        {{ t.icon }} {{ t.label }} <span v-if="t.plus && !store.user?.is_premium" class="badge badge-lime" style="padding:1px 6px;font-size:10px">PLUS</span>
      </button>
    </div>

    <!-- USO DE CUPO -->
    <div v-if="tab === 'cupo'" class="sim-grid mt-3 appear">
      <div class="card form-grid">
        <div class="card-title">💳 Tu tarjeta</div>
        <div class="field"><label>Cupo aprobado</label><div class="input-prefix"><span>$</span><input class="input" type="number" min="1" step="50000" v-model.number="util.credit_limit"/></div></div>
        <div class="field"><label>Lo que debes hoy: {{ cop(util.balance) }}</label>
          <input type="range" min="0" :max="util.credit_limit || 1" step="10000" v-model.number="util.balance"/></div>
        <p class="hint">Las entidades miran cuánto usas de tu cupo al momento del corte. Mientras menos, mejor.</p>
      </div>
      <div class="card" v-if="utilRes">
        <div class="row-between"><div><div class="xs bold muted">UTILIZACIÓN</div><div class="big-number">{{ utilRes.utilization }}%</div></div>
          <span class="badge" :class="{ 'badge-warning': utilRes.status === 'warning', 'badge-danger': utilRes.status === 'danger' }" style="font-size:14px;padding:6px 14px">{{ utilRes.label }}</span></div>
        <div class="gauge-bar mt-3"><div class="needle" :style="{ left: Math.min(utilRes.utilization, 100) + '%' }"></div></div>
        <div class="row-between xs muted mt-1"><span>0 %</span><span>30 %</span><span>60 %</span><span>100 %</span></div>
        <p class="mt-3 text-2">{{ utilRes.advice }}</p>
        <div class="grid-2 mt-3" style="gap:12px">
          <div class="kpi"><div class="label">Deuda máxima recomendada (30 %)</div><div class="value">{{ cop(utilRes.recommended_max_balance) }}</div></div>
          <div class="kpi"><div class="label">Cupo disponible</div><div class="value">{{ cop(utilRes.available) }}</div></div>
        </div>
      </div>
    </div>

    <!-- COSTO DE CRÉDITO -->
    <div v-if="tab === 'credito'" class="sim-grid mt-3 appear">
      <div class="card form-grid">
        <div class="card-title">🧮 Datos de la oferta</div>
        <div class="field"><label>Monto</label><div class="input-prefix"><span>$</span><input class="input" type="number" min="1" step="100000" v-model.number="loan.amount"/></div></div>
        <div class="field"><label>Tasa efectiva anual (E.A.): {{ loan.ea_rate }} %</label><input type="range" min="0" max="50" step="0.5" v-model.number="loan.ea_rate"/></div>
        <div class="field"><label>Plazo: {{ loan.months }} meses</label><input type="range" min="1" max="72" v-model.number="loan.months"/></div>
        <div class="field"><label>Cuota de manejo / seguros mensuales</label><div class="input-prefix"><span>$</span><input class="input" type="number" min="0" step="1000" v-model.number="loan.monthly_fee"/></div></div>
        <p class="hint">Consulta la tasa E.A. y los cobros en la oferta de tu entidad. Compara siempre el costo total, no solo la cuota.</p>
      </div>
      <div class="stack-lg" v-if="loanRes">
        <div class="card">
          <div class="xs bold muted">CUOTA MENSUAL APROXIMADA</div>
          <div class="big-number">{{ cop(loanRes.monthly_payment) }}</div>
          <p class="small muted">Tasa mensual equivalente: {{ loanRes.monthly_rate }} % M.V.</p>
          <div class="grid-3 mt-3" style="gap:12px">
            <div class="kpi"><div class="label">Intereses</div><div class="value" style="color:var(--warning)">{{ cop(loanRes.total_interest) }}</div></div>
            <div class="kpi"><div class="label">Otros cobros</div><div class="value">{{ cop(loanRes.total_fees) }}</div></div>
            <div class="kpi"><div class="label">Pagas en total</div><div class="value">{{ cop(loanRes.total_paid) }}</div></div>
          </div>
          <div class="next-task mt-3"><div class="ico">💡</div><div class="small">Por cada $100 que te prestan terminas pagando <strong>{{ cop(100 + loanRes.cost_ratio) }}</strong>. Un plazo más corto reduce los intereses.</div></div>
        </div>
        <div class="card">
          <div class="card-head"><div class="card-title">📋 Tabla de amortización</div><span v-if="loanRes.schedule_truncated" class="badge badge-lime">Completa en Plus</span></div>
          <div class="table-wrap">
            <table class="table">
              <thead><tr><th>Mes</th><th>Cuota</th><th>Interés</th><th>Abono a capital</th><th>Saldo</th></tr></thead>
              <tbody><tr v-for="r in loanRes.schedule" :key="r.month"><td>{{ r.month }}</td><td>{{ cop(r.payment) }}</td><td>{{ cop(r.interest) }}</td><td>{{ cop(r.principal) }}</td><td>{{ cop(r.balance) }}</td></tr></tbody>
            </table>
          </div>
          <router-link v-if="loanRes.schedule_truncated" to="/plus" class="btn btn-soft btn-sm mt-2">👑 Ver los {{ loan.months }} meses con Plus</router-link>
        </div>
      </div>
    </div>

    <!-- ATRASO -->
    <div v-if="tab === 'atraso'" class="sim-grid mt-3 appear">
      <div class="card form-grid">
        <div class="card-title">⏰ Simula un atraso</div>
        <div class="field"><label>Valor de la cuota</label><div class="input-prefix"><span>$</span><input class="input" type="number" min="1" step="10000" v-model.number="late.installment"/></div></div>
        <div class="field"><label>Días de atraso: {{ late.days_late }}</label><input type="range" min="0" max="365" v-model.number="late.days_late"/></div>
        <div class="field"><label>Tasa de mora E.A. (%)</label><input class="input" type="number" min="0" max="100" step="0.5" v-model.number="late.default_ea_rate"/>
          <span class="hint">La mora no puede superar la tasa de usura vigente que certifica la Superintendencia Financiera.</span></div>
      </div>
      <div class="stack-lg" v-if="lateRes">
        <div class="card">
          <div class="grid-3" style="gap:12px">
            <div class="kpi"><div class="label">Intereses de mora</div><div class="value" style="color:var(--danger)">{{ cop(lateRes.late_interest) }}</div></div>
            <div class="kpi"><div class="label">Total a pagar</div><div class="value">{{ cop(lateRes.total_due) }}</div></div>
            <div class="kpi"><div class="label">Dato negativo (si te reportan)</div><div class="value">{{ lateRes.negative_record_months ? lateRes.negative_record_months + ' meses' : '—' }}</div></div>
          </div>
          <p class="mt-3 text-2">{{ lateRes.message }}</p>
        </div>
        <div class="card">
          <div class="card-title" style="margin-bottom:16px">🧭 Qué pasa en el tiempo</div>
          <div class="timeline">
            <div v-for="t in lateRes.all_timeline" :key="t.title" class="tl-item" :class="{ reached: late.days_late >= t.day }">
              <div class="tl-day">Día {{ t.day }}</div>
              <div><div class="bold">{{ t.title }}</div><div class="small muted">{{ t.text }}</div></div>
            </div>
          </div>
          <p class="xs muted">Basado en la Ley 1266 de 2008 y la Ley 2157 de 2021. Información educativa, no asesoría legal.</p>
        </div>
      </div>
    </div>

    <!-- PUNTAJE -->
    <div v-if="tab === 'puntaje'" class="mt-3">
      <PremiumLock v-if="scoreLocked" title="Simulador de puntaje · Plus" text="Mueve tus hábitos y descubre cómo cada factor afecta tu puntaje crediticio estimado."/>
      <div v-else class="sim-grid appear">
        <div class="card form-grid">
          <div class="card-title">📊 Tus hábitos</div>
          <div class="field"><label>Pagos a tiempo: {{ score.on_time_pct }} %</label><input type="range" min="0" max="100" v-model.number="score.on_time_pct"/></div>
          <div class="field"><label>Uso del cupo: {{ score.utilization_pct }} %</label><input type="range" min="0" max="100" v-model.number="score.utilization_pct"/></div>
          <div class="field"><label>Antigüedad del historial: {{ score.history_months }} meses</label><input type="range" min="0" max="120" v-model.number="score.history_months"/></div>
          <div class="field"><label>Solicitudes de crédito (12 meses): {{ score.inquiries_12m }}</label><input type="range" min="0" max="10" v-model.number="score.inquiries_12m"/></div>
          <div class="field"><label>Tipos de producto: {{ score.product_types }}</label><input type="range" min="0" max="4" v-model.number="score.product_types"/></div>
        </div>
        <div class="card" v-if="scoreRes">
          <div class="row wrap" style="gap:24px">
            <div class="center">
              <div class="xs bold muted">PUNTAJE ESTIMADO</div>
              <div class="big-number" :style="{ color: scoreRes.score ? scoreColor(scoreRes.score) : 'var(--muted)', fontSize: '56px' }">{{ scoreRes.score ?? '—' }}</div>
              <span class="badge">{{ scoreRes.band }}</span>
            </div>
            <p class="small text-2" style="flex:1;min-width:200px">{{ scoreRes.message }}</p>
          </div>
          <div class="stack mt-3" v-if="scoreRes.factors.length">
            <div v-for="f in scoreRes.factors" :key="f.key" class="factor">
              <span class="small bold">{{ f.label }} <span class="muted xs">· pesa {{ f.weight }} %</span></span><span class="small bold">{{ f.value }}%</span>
              <div style="grid-column:1/-1"><Bar :value="f.value" small/></div>
            </div>
          </div>
          <div class="mt-3"><div class="xs bold muted">PARA MEJORAR</div><ul class="check-list small"><li v-for="t in scoreRes.tips" :key="t">{{ t }}</li></ul></div>
        </div>
      </div>
    </div>
  </div>`,
};

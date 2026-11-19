import { store } from "../store.js";

export default {
  setup() {
    const stats = [
      { num: "54 %", text: "se sentiría inseguro al tomar su primer crédito sin orientación." },
      { num: "35,7 %", text: "ya evitó pedir un crédito por no saber cómo funcionaba." },
      { num: "91 %", text: "ha tenido al menos una duda sobre historial, puntaje o cupo." },
      { num: "85,7 %", text: "quiere una herramienta que le explique todo de forma sencilla." },
    ];
    const how = [
      { icon: "🧭", title: "Diagnóstico", text: "7 preguntas rápidas para conocer tu situación financiera y tus metas." },
      { icon: "🗺️", title: "Ruta personalizada", text: "Definimos tus próximos pasos. Quien nunca ha tenido crédito no recibe lo mismo que quien ya tiene tarjeta." },
      { icon: "🤝", title: "Acompañamiento", text: "Lecciones cortas, simuladores, metas, recordatorios y Step, tu asistente." },
      { icon: "📈", title: "Progreso", text: "Tu índice de preparación crediticia te muestra cuándo estás listo para el siguiente paso." },
    ];
    const modules = [
      { icon: "🧱", title: "Construcción del historial", text: "Cómo salir del 'sin historial' y qué productos suelen ayudar a empezar." },
      { icon: "🎯", title: "Gestión y uso responsable", text: "Presupuesto, regla del 30 % del cupo y fechas que debes conocer." },
      { icon: "💸", title: "Costos y condiciones", text: "Tasas E.A., cuota de manejo y el costo total de una deuda, sin enredos." },
      { icon: "🛡️", title: "Consecuencias y riesgos", text: "Qué pasa si te atrasas, cómo funcionan los reportes y cómo recuperarte." },
    ];
    return { store, stats, how, modules };
  },
  template: `
  <div class="landing">
    <section class="l-hero">
      <div class="grid-lines"></div>
      <nav class="l-nav">
        <a href="#" class="brand"><img src="/assets/img/logo.svg" alt=""/><div>CrediStep</div></a>
        <div style="flex:1"></div>
        <a class="link" href="#como-funciona">Cómo funciona</a>
        <a class="link" href="#modulos">Qué aprendes</a>
        <a class="link" href="#planes">Planes</a>
        <template v-if="store.token">
          <router-link to="/inicio" class="btn btn-lime btn-sm">Ir a mi app →</router-link>
        </template>
        <template v-else>
          <router-link to="/ingresar" class="btn btn-glass btn-sm">Ingresar</router-link>
          <router-link to="/registro" class="btn btn-lime btn-sm">Comenzar</router-link>
        </template>
      </nav>

      <div class="l-hero-inner">
        <div class="appear">
          <span class="eyebrow">🌱 Educación financiera para jóvenes de 18 a 25 años</span>
          <h1>Construye hoy el historial que <span class="gradient-text">necesitarás mañana</span>.</h1>
          <p class="lead">CrediStep es tu GPS financiero: hace un diagnóstico de tu situación, te propone una ruta personalizada y te acompaña hasta tu primer crédito con confianza. No te decimos qué comprar. Te enseñamos cómo avanzar.</p>
          <div class="row wrap mt-4">
            <router-link to="/registro" class="btn btn-lime btn-lg">Empezar gratis <Icon name="arrowRight" :size="18"/></router-link>
            <router-link to="/ingresar" class="btn btn-glass btn-lg">Ver demo</router-link>
          </div>
          <div class="row wrap mt-3 small" style="color:rgba(232,255,243,.7);gap:20px">
            <span>✓ Sin tarjeta de crédito</span><span>✓ Lenguaje sencillo</span><span>✓ Contenido neutral</span>
          </div>
        </div>

        <div class="l-hero-visual" style="position:relative">
          <div class="phone">
            <div class="phone-notch"></div>
            <div class="phone-screen">
              <div class="row-between" style="margin-top:22px"><strong style="font-size:15px">Mi diagnóstico</strong><span class="badge">Tu perfil</span></div>
              <div class="ph-card center">
                <ProgressRing :value="45" :size="132" :stroke="12" sub="En construcción"/>
                <p class="small mt-2" style="color:#3c5a4d">¡Tienes buenos hábitos financieros, pero aún puedes mejorar!</p>
              </div>
              <div class="ph-card small" style="display:grid;gap:8px">
                <div>✅ Tienes cuenta bancaria</div>
                <div>⚠️ No tienes historial todavía</div>
              </div>
              <div class="ph-card">
                <div class="row-between small"><strong>Mi plan</strong><span>60 %</span></div>
                <div class="bar mt-1"><span style="width:60%"></span></div>
                <div class="xs mt-1" style="color:#3c5a4d">Próximo objetivo: paga a tiempo durante 30 días</div>
              </div>
              <div class="btn btn-primary btn-block btn-sm">VER MI PLAN</div>
            </div>
          </div>
          <div class="float-chip" style="left:0;top:90px">🔥 Racha de 5 días</div>
          <div class="float-chip" style="right:-10px;bottom:120px;animation-delay:1.2s">⭐ +30 XP · Lección completada</div>
        </div>
      </div>
    </section>

    <section class="l-section">
      <div class="section-head">
        <span class="kicker">El problema</span>
        <h2>El crédito llega temprano. La orientación llega tarde.</h2>
        <p>Solo el 22 % de los jóvenes de 18 a 25 años en Colombia accedió a crédito en 2024, frente al 35,5 % del promedio nacional (Banca de las Oportunidades). Encuestamos a 126 jóvenes y esto encontramos:</p>
      </div>
      <div class="grid-4">
        <div v-for="s in stats" :key="s.num" class="card stat-card card-hover">
          <div class="num">{{ s.num }}</div>
          <p class="text-2 mt-1">{{ s.text }}</p>
        </div>
      </div>
      <p class="xs muted mt-2">Fuente: Encuesta de validación CrediStep (n = 126), octubre de 2026.</p>
    </section>

    <section class="l-section" id="como-funciona" style="padding-top:20px">
      <div class="section-head">
        <span class="kicker">Cómo funciona</span>
        <h2>Un GPS financiero en cuatro pasos</h2>
        <p>La educación financiera deja de ser teoría y se convierte en un proceso con metas claras.</p>
      </div>
      <div class="grid-4">
        <div v-for="(h, i) in how" :key="h.title" class="card how-card card-hover">
          <span class="n">0{{ i + 1 }}</span>
          <div class="h-ico">{{ h.icon }}</div>
          <h3 style="font-size:19px;font-weight:800">{{ h.title }}</h3>
          <p class="text-2 mt-1">{{ h.text }}</p>
        </div>
      </div>
    </section>

    <section class="l-section" id="modulos" style="padding-top:20px">
      <div class="grid-2" style="align-items:center;gap:48px">
        <div>
          <span class="kicker">Qué aprendes</span>
          <h2>Contenido corto, práctico y en tu idioma</h2>
          <p class="muted mt-2" style="font-size:17px">Los módulos salen directamente de lo que los jóvenes nos pidieron: cómo empezar el historial desde cero (50 %), cómo funciona el puntaje (38 %) y cómo manejar el cupo (34 %).</p>
          <div class="stack mt-3">
            <div class="row"><span class="badge badge-lime">✓</span> Lecciones de 4–6 minutos con quiz</div>
            <div class="row"><span class="badge badge-lime">✓</span> Simuladores de cupo, costo de crédito, atrasos y puntaje</div>
            <div class="row"><span class="badge badge-lime">✓</span> Asistente Step para dudas rápidas</div>
          </div>
        </div>
        <div class="grid-2">
          <div v-for="m in modules" :key="m.title" class="card card-hover">
            <div style="font-size:32px">{{ m.icon }}</div>
            <h3 style="font-size:17px;font-weight:800;margin-top:10px">{{ m.title }}</h3>
            <p class="text-2 small mt-1">{{ m.text }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="l-section" id="planes" style="padding-top:20px">
      <div class="section-head">
        <span class="kicker">Planes</span>
        <h2>Empieza gratis. Avanza con Plus.</h2>
      </div>
      <div class="grid-3">
        <div class="card plan-card">
          <h3 style="font-size:20px;font-weight:800">Gratis</h3>
          <div class="price mt-2">$0</div>
          <ul class="check-list">
            <li>Diagnóstico y ruta personalizada</li><li>Lecciones esenciales con quiz</li>
            <li>Simuladores de cupo, crédito y atrasos</li><li>Hasta 2 metas y recordatorios</li>
          </ul>
          <router-link to="/registro" class="btn btn-outline btn-block mt-3">Crear cuenta</router-link>
        </div>
        <div class="card plan-card featured">
          <span class="badge badge-lime" style="position:absolute;top:18px;right:18px">Más popular</span>
          <h3 style="font-size:20px;font-weight:800">CrediStep Plus</h3>
          <div class="price mt-2">$20.000<span class="small muted" style="font-weight:600"> /mes</span></div>
          <ul class="check-list">
            <li>Todo lo del plan gratis</li><li>Simulador de puntaje crediticio</li>
            <li>Tabla de amortización completa</li><li>Lecciones avanzadas y metas ilimitadas</li>
          </ul>
          <router-link to="/registro" class="btn btn-primary btn-block mt-3">Probar Plus</router-link>
        </div>
        <div class="card plan-card">
          <h3 style="font-size:20px;font-weight:800">Universidades</h3>
          <div class="price mt-2" style="font-size:30px">Licencia</div>
          <ul class="check-list">
            <li>Plus para todos tus estudiantes</li><li>Panel con métricas agregadas</li>
            <li>Respaldo institucional y confianza</li><li>Piloto: Universidad Javeriana</li>
          </ul>
          <router-link to="/ingresar" class="btn btn-outline btn-block mt-3">Ver panel demo</router-link>
        </div>
      </div>
    </section>

    <section class="l-section" style="padding-top:20px">
      <div class="quote-band">
        <div class="grid-lines"></div>
        <h2 style="position:relative">“No queremos que los jóvenes aprendan de sus errores financieros. Queremos que aprendan antes de cometerlos.”</h2>
        <router-link to="/registro" class="btn btn-lime btn-lg mt-4" style="position:relative">Dar mi primer paso</router-link>
      </div>
    </section>

    <footer class="l-footer">
      <div class="row"><img src="/assets/img/logo.svg" width="28" alt=""/> <strong style="color:var(--text)">CrediStep</strong> · Gestión de Innovación en TI · Pontificia Universidad Javeriana · 2026</div>
      <div>Contenido educativo. CrediStep no ofrece productos financieros ni asesoría de inversión.</div>
    </footer>
  </div>`,
};

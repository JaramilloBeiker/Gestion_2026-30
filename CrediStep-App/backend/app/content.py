"""Contenido base de CrediStep.

- MODULES: los 4 módulos del MVP definidos en el Artefacto de Validación (Cuadro 2).
- PLAN_STEPS: los 5 pasos de la ruta presentados en el primer pitch.
- GLOSSARY / FAQ: lenguaje sencillo para el asistente "Step".

Bloques de lección: text | tip | example | list | warning | stat
"""

MODULES = [
    {
        "slug": "construccion-historial",
        "title": "Construcción y mejora del historial",
        "description": "Cómo salir del estado 'sin historial' y qué productos elegir primero.",
        "icon": "🧱",
        "color": "#10b981",
        "lessons": [
            {
                "slug": "que-es-historial",
                "title": "¿Qué es el historial crediticio?",
                "summary": "La 'hoja de vida' de cómo manejas tus deudas.",
                "minutes": 4,
                "blocks": [
                    {"type": "text", "text": "Tu historial crediticio es el registro de cómo has manejado tus obligaciones: si pagas a tiempo, cuánto debes y qué productos tienes. En Colombia lo guardan las centrales de riesgo, como DataCrédito Experian y TransUnion."},
                    {"type": "stat", "value": "32 %", "text": "de los adultos en Colombia no tenía historial crediticio tradicional en 2026 (TransUnion)."},
                    {"type": "text", "text": "Las entidades lo consultan cuando pides un crédito, un arriendo o incluso un plan de celular. No es una 'lista negra': también guarda lo bueno que haces."},
                    {"type": "example", "title": "Para ti, en la vida real", "text": "Laura, 20 años, pagó su plan de celular a tiempo durante un año. Cuando pidió su primera tarjeta, la entidad ya tenía datos positivos sobre ella."},
                    {"type": "tip", "text": "Puedes consultar tu propio reporte gratis, al menos una vez al mes, en las centrales de riesgo. Consultarlo tú mismo NO te baja el puntaje."},
                ],
                "quiz": [
                    {"q": "¿Quién guarda tu historial crediticio en Colombia?", "options": ["Tu banco únicamente", "Las centrales de riesgo como DataCrédito y TransUnion", "La DIAN", "Nadie, no existe"], "a": 1, "e": "Las centrales de riesgo recopilan la información que reportan bancos y empresas del sector real."},
                    {"q": "Si consultas tu propio reporte…", "options": ["Tu puntaje baja", "Quedas reportado", "No pasa nada malo: es tu derecho", "Te cobran una multa"], "a": 2, "e": "Consultar tu propia información es un derecho (habeas data) y no afecta tu puntaje."},
                ],
            },
            {
                "slug": "empezar-desde-cero",
                "title": "Cómo empezar tu historial desde cero",
                "summary": "El ciclo 'no me dan crédito porque no tengo historial' tiene salida.",
                "minutes": 5,
                "blocks": [
                    {"type": "text", "text": "Muchos jóvenes nos dijeron en la encuesta que necesitan crédito para tener historial, pero no les dan crédito por no tenerlo. La salida es empezar pequeño."},
                    {"type": "list", "title": "Primeros pasos que suelen generar historial", "items": ["Un plan de celular o servicio a tu nombre pagado a tiempo (algunas empresas reportan a centrales).", "Una tarjeta de crédito de cupo bajo usada con moderación.", "Una tarjeta amparada o respaldada por un ahorro, si tu entidad la ofrece.", "Un crédito pequeño y planeado que puedas pagar sin estrés."]},
                    {"type": "warning", "text": "Evita préstamos informales ('gota a gota'): no construyen historial y cobran intereses muy por encima de lo legal."},
                    {"type": "tip", "text": "Empieza con un solo producto, úsalo poco y págalo completo. La constancia pesa más que la cantidad."},
                ],
                "quiz": [
                    {"q": "¿Cuál es una buena forma de empezar historial?", "options": ["Pedir 5 tarjetas el mismo mes", "Un préstamo gota a gota", "Un producto básico usado con moderación y pagado a tiempo", "Esperar a los 30 años"], "a": 2, "e": "Empezar pequeño y pagar a tiempo es la forma más segura de construir historial."},
                ],
            },
            {
                "slug": "estrategia-6-meses",
                "title": "Estrategia de 6 meses para un historial sólido",
                "summary": "Plan mes a mes para llegar a tu meta con confianza.",
                "minutes": 6,
                "premium": True,
                "blocks": [
                    {"type": "text", "text": "Esta estrategia te ayuda a organizar tus primeros seis meses con un producto de crédito."},
                    {"type": "list", "title": "Mes a mes", "items": ["Mes 1: define fecha de corte y fecha límite; crea recordatorios en CrediStep.", "Mes 2: usa máximo el 30 % del cupo y paga el total.", "Mes 3: consulta tu reporte gratis y verifica que todo esté correcto.", "Mes 4: revisa tus gastos fijos y ajusta tu presupuesto.", "Mes 5: no pidas productos nuevos; deja que tu historial madure.", "Mes 6: evalúa tu progreso con el simulador de puntaje."]},
                    {"type": "tip", "text": "Un historial sano no se construye rápido: se construye constante."},
                ],
                "quiz": [
                    {"q": "En los primeros meses conviene…", "options": ["Pedir muchos productos para tener más historial", "Mantener un uso bajo del cupo y pagar el total", "Usar todo el cupo"], "a": 1, "e": "Pocos productos, bien manejados, construyen el mejor historial."},
                ],
            },
        ],
    },
    {
        "slug": "puntaje-y-cupo",
        "title": "Gestión y uso responsable",
        "description": "Organiza tus pagos, domina tu cupo y evita intereses innecesarios.",
        "icon": "🎯",
        "color": "#22c55e",
        "lessons": [
            {
                "slug": "presupuesto-50-30-20",
                "title": "Tu presupuesto 50/30/20",
                "summary": "Una regla simple para que tu dinero alcance.",
                "minutes": 4,
                "blocks": [
                    {"type": "text", "text": "La regla 50/30/20 divide tus ingresos en tres partes: necesidades, gustos y ahorro. No es perfecta, pero es un gran punto de partida."},
                    {"type": "list", "title": "Cómo se reparte", "items": ["50 % necesidades: transporte, comida, arriendo, celular.", "30 % gustos: salidas, ropa, suscripciones.", "20 % ahorro y metas: fondo de emergencia, viaje, deudas."]},
                    {"type": "example", "title": "Con una mesada de $800.000", "text": "$400.000 para necesidades, $240.000 para gustos y $160.000 para ahorrar. Si ahorras $160.000 al mes, en 6 meses tendrás casi $1 millón."},
                    {"type": "tip", "text": "Ahorra apenas recibas el dinero, no con lo que sobre al final del mes."},
                ],
                "quiz": [
                    {"q": "En la regla 50/30/20, ¿qué porcentaje va al ahorro?", "options": ["50 %", "30 %", "20 %", "0 %"], "a": 2, "e": "El 20 % se destina a ahorro y metas."},
                ],
            },
            {
                "slug": "como-funciona-puntaje",
                "title": "¿Cómo funciona el puntaje crediticio?",
                "summary": "Los factores que suben (y bajan) tu score.",
                "minutes": 5,
                "blocks": [
                    {"type": "stat", "value": "36,5 %", "text": "de los jóvenes encuestados ha tenido dudas sobre cómo se calcula su puntaje (Encuesta CrediStep, n = 126)."},
                    {"type": "text", "text": "El puntaje es un número que resume qué tan probable es que pagues a tiempo. Cada central tiene su propio modelo, pero los factores suelen ser parecidos."},
                    {"type": "list", "title": "Factores que más influyen", "items": ["Pagos a tiempo: el más importante.", "Uso del cupo: cuánto usas frente a lo que tienes aprobado.", "Antigüedad: cuánto tiempo llevas con productos.", "Solicitudes recientes: pedir mucho crédito en poco tiempo.", "Variedad de productos bien manejados."]},
                    {"type": "tip", "text": "Prueba el Simulador de puntaje para ver cómo cada hábito mueve tu resultado."},
                ],
                "quiz": [
                    {"q": "¿Cuál suele ser el factor que más pesa en el puntaje?", "options": ["Tu edad", "Pagar a tiempo", "Tu ciudad", "Tu banco"], "a": 1, "e": "El comportamiento de pago es el factor más relevante en los modelos de puntaje."},
                    {"q": "Pedir varios créditos en un mes…", "options": ["Sube tu puntaje", "No tiene efecto", "Puede verse como riesgo porque cada solicitud deja huella", "Es obligatorio"], "a": 2, "e": "Muchas consultas en poco tiempo pueden interpretarse como necesidad urgente de crédito."},
                ],
            },
            {
                "slug": "manejo-del-cupo",
                "title": "Domina el cupo de tu tarjeta",
                "summary": "Fecha de corte, fecha límite y la regla del 30 %.",
                "minutes": 5,
                "blocks": [
                    {"type": "text", "text": "El cupo es el máximo que el banco te presta en tu tarjeta. No es dinero tuyo: es dinero prestado que debes devolver."},
                    {"type": "list", "title": "Dos fechas que debes conocer", "items": ["Fecha de corte: el día en que el banco suma tus compras del periodo.", "Fecha límite de pago: el último día para pagar sin intereses de mora."]},
                    {"type": "example", "title": "La regla del 30 %", "text": "Si tu cupo es $1.000.000, intenta no deber más de $300.000 al momento del corte."},
                    {"type": "warning", "text": "Los avances en efectivo suelen cobrar intereses desde el primer día y comisiones adicionales. Úsalos solo en emergencias reales."},
                ],
                "quiz": [
                    {"q": "Con un cupo de $2.000.000, ¿cuánto es el 30 %?", "options": ["$300.000", "$600.000", "$1.000.000", "$2.000.000"], "a": 1, "e": "30 % de 2.000.000 = 600.000."},
                    {"q": "La fecha límite de pago es…", "options": ["El día que el banco suma tus compras", "El último día para pagar sin mora", "El día que te dan la tarjeta"], "a": 1, "e": "Pagar antes de la fecha límite evita intereses de mora y reportes negativos."},
                ],
            },
            {
                "slug": "comparar-tarjetas",
                "title": "Cómo comparar productos sin que te vendan",
                "summary": "Una checklist neutral para evaluar cualquier oferta.",
                "minutes": 6,
                "premium": True,
                "blocks": [
                    {"type": "text", "text": "En la encuesta, el 23 % de los jóvenes dijo que buscaría orientación primero en los bancos, que son quienes venden el producto. Esta checklist te ayuda a comparar con criterio propio."},
                    {"type": "list", "title": "Compara siempre", "items": ["Tasa efectiva anual (E.A.), no solo la mensual.", "Cuota de manejo y otros cobros fijos.", "Seguros incluidos y si son obligatorios.", "Costo de avances y compras internacionales.", "Beneficios que de verdad vas a usar."]},
                    {"type": "tip", "text": "Usa el Simulador de costo de crédito con los datos de cada oferta y compara el costo total, no la cuota."},
                ],
                "quiz": [
                    {"q": "Para comparar créditos lo mejor es mirar…", "options": ["Solo la cuota mensual", "El costo total y la tasa E.A.", "El color de la tarjeta"], "a": 1, "e": "Una cuota baja puede esconder un plazo largo y un costo total alto."},
                ],
            },
        ],
    },
    {
        "slug": "costos-y-condiciones",
        "title": "Costos y condiciones financieras",
        "description": "Tasas, comisiones y el costo real de una deuda en lenguaje sencillo.",
        "icon": "💸",
        "color": "#84cc16",
        "lessons": [
            {
                "slug": "tasas-de-interes",
                "title": "Tasas de interés sin enredos",
                "summary": "E.A., M.V. y tasa de usura explicadas fácil.",
                "minutes": 5,
                "blocks": [
                    {"type": "text", "text": "La tasa de interés es el 'precio' de que te presten dinero. En Colombia la verás como tasa efectiva anual (E.A.) o mes vencido (M.V.)."},
                    {"type": "list", "title": "Glosario rápido", "items": ["E.A. (efectiva anual): lo que pagas en un año, incluyendo el efecto de los intereses sobre intereses.", "M.V. (mes vencido): la tasa que se cobra cada mes.", "Tasa de usura: el máximo legal que pueden cobrar, certificado por la Superintendencia Financiera."]},
                    {"type": "example", "title": "Ojo con la comparación", "text": "Una tasa de 2 % M.V. no es 24 % al año: equivale a aproximadamente 26,8 % E.A. por el interés compuesto."},
                    {"type": "tip", "text": "Siempre compara tasas en la misma unidad (E.A. con E.A.)."},
                ],
                "quiz": [
                    {"q": "¿Qué es la tasa de usura?", "options": ["Una tasa promocional", "El máximo legal que pueden cobrar", "La tasa de tu cuenta de ahorros"], "a": 1, "e": "La Superintendencia Financiera certifica periódicamente el límite máximo legal."},
                    {"q": "2 % M.V. equivale a…", "options": ["Exactamente 24 % E.A.", "Aproximadamente 26,8 % E.A.", "2 % E.A."], "a": 1, "e": "(1,02)^12 − 1 ≈ 26,8 %."},
                ],
            },
            {
                "slug": "costo-total",
                "title": "El costo total de una deuda",
                "summary": "Por qué la cuota baja puede salir cara.",
                "minutes": 4,
                "blocks": [
                    {"type": "text", "text": "Cuando te ofrecen 'cuotas cómodas', la pregunta clave es: ¿cuánto voy a pagar en total?"},
                    {"type": "example", "title": "Mismo celular, distinto plazo", "text": "Un celular de $1.500.000 a 28 % E.A.: a 12 meses pagas unos $1.700.000; a 36 meses, más de $2.100.000. La cuota baja, pero el costo sube."},
                    {"type": "list", "title": "Además de los intereses", "items": ["Cuota de manejo", "Seguros", "Comisiones por avances o pagos tardíos"]},
                    {"type": "tip", "text": "Si puedes, elige el plazo más corto cuya cuota puedas pagar sin estrés."},
                ],
                "quiz": [
                    {"q": "A mayor plazo, con la misma tasa…", "options": ["Pagas menos en total", "Pagas más intereses en total", "Pagas lo mismo"], "a": 1, "e": "Más meses significan más intereses acumulados."},
                ],
            },
        ],
    },
    {
        "slug": "consecuencias-y-riesgos",
        "title": "Consecuencias y mitigación de riesgos",
        "description": "Qué pasa si te atrasas y cómo actuar ante emergencias financieras.",
        "icon": "🛡️",
        "color": "#14b8a6",
        "lessons": [
            {
                "slug": "si-me-atraso",
                "title": "¿Qué pasa si me atraso en un pago?",
                "summary": "Mora, reportes y cómo recuperarte.",
                "minutes": 5,
                "blocks": [
                    {"type": "stat", "value": "23,8 %", "text": "de los encuestados tiene dudas sobre qué ocurre si se atrasa en un pago."},
                    {"type": "text", "text": "Atrasarte un día ya genera intereses de mora. Si el atraso continúa, la entidad puede reportarte negativamente en las centrales de riesgo, pero antes debe avisarte."},
                    {"type": "list", "title": "Lo que dice la ley (Ley 1266 de 2008 y Ley 2157 de 2021)", "items": ["La entidad debe avisarte antes del reporte y darte al menos 20 días calendario.", "Si pagas, el dato negativo permanece el doble del tiempo que duró la mora.", "Ese tiempo tiene un máximo de 4 años desde que pagas."]},
                    {"type": "tip", "text": "Si sabes que no vas a poder pagar, llama ANTES a tu entidad. Muchas tienen alternativas de refinanciación."},
                ],
                "quiz": [
                    {"q": "Si te atrasas 3 meses y luego pagas, el dato negativo dura aproximadamente…", "options": ["3 meses", "6 meses", "10 años", "Para siempre"], "a": 1, "e": "La permanencia es el doble del tiempo de mora (máximo 4 años)."},
                    {"q": "¿Qué conviene hacer si no vas a poder pagar?", "options": ["Esconderte", "Comunicarte antes con la entidad", "Pedir un gota a gota"], "a": 1, "e": "Hablar a tiempo abre opciones como acuerdos o refinanciación."},
                ],
            },
            {
                "slug": "fondo-emergencia",
                "title": "Tu fondo de emergencia",
                "summary": "El escudo que evita que una urgencia se vuelva deuda.",
                "minutes": 4,
                "blocks": [
                    {"type": "text", "text": "Un fondo de emergencia es dinero apartado solo para imprevistos: una cita médica, un daño en el celular, quedarte sin ingresos un mes."},
                    {"type": "list", "title": "Cómo construirlo", "items": ["Meta inicial: un mes de tus gastos básicos.", "Meta ideal: de tres a seis meses.", "Guárdalo en una cuenta separada, fácil de usar pero no a la vista.", "Aporta algo cada vez que recibas dinero, aunque sea poco."]},
                    {"type": "tip", "text": "Crea una meta de tipo 'Emergencia' en CrediStep y sigue tu avance."},
                ],
                "quiz": [
                    {"q": "El fondo de emergencia sirve para…", "options": ["Vacaciones", "Imprevistos reales", "Comprar el celular nuevo"], "a": 1, "e": "Es tu colchón para que una urgencia no termine en deuda."},
                ],
            },
            {
                "slug": "sobreendeudamiento",
                "title": "Señales de sobreendeudamiento",
                "summary": "Cómo detectar a tiempo que las deudas se están saliendo de control.",
                "minutes": 4,
                "blocks": [
                    {"type": "text", "text": "En la encuesta, el miedo al sobreendeudamiento y confundir el crédito con dinero propio aparecieron como grandes preocupaciones."},
                    {"type": "list", "title": "Señales de alerta", "items": ["Tus cuotas superan el 30 % de tus ingresos.", "Pagas solo el mínimo de la tarjeta mes a mes.", "Usas un crédito para pagar otro.", "No sabes cuánto debes en total."]},
                    {"type": "warning", "text": "Si identificas dos o más señales, detén nuevas compras a crédito y arma un plan de pago con prioridades."},
                ],
                "quiz": [
                    {"q": "¿Cuál es una señal de alerta?", "options": ["Pagar el total de la tarjeta", "Usar un crédito para pagar otro", "Tener un fondo de emergencia"], "a": 1, "e": "Cubrir deudas con más deuda es una señal clara de sobreendeudamiento."},
                ],
            },
        ],
    },
]

PLAN_STEPS = [
    {
        "title": "Organiza tus gastos",
        "description": "Saber a dónde va tu dinero es el punto de partida.",
        "icon": "🧾",
        "tasks": [
            {"title": "Registra tus gastos durante una semana", "description": "Anota cada gasto, por pequeño que sea.", "xp": 20, "auto": "tracks_expenses"},
            {"title": "Arma tu presupuesto 50/30/20", "description": "Completa la lección y aplica la regla a tus ingresos.", "xp": 30, "lesson": "presupuesto-50-30-20"},
            {"title": "Crea tu primer recordatorio", "description": "Programa la fecha de un pago o de tu ahorro mensual.", "xp": 15, "route": "/recordatorios"},
        ],
    },
    {
        "title": "Crea tu fondo de emergencia",
        "description": "Tu escudo para que un imprevisto no se convierta en deuda.",
        "icon": "🛟",
        "tasks": [
            {"title": "Aprende por qué el fondo te protege", "description": "Lección corta sobre fondos de emergencia.", "xp": 30, "lesson": "fondo-emergencia"},
            {"title": "Crea una meta de emergencia", "description": "Define cuánto necesitas para cubrir un mes de gastos.", "xp": 20, "route": "/metas", "auto": "has_emergency_fund"},
            {"title": "Haz tu primer aporte", "description": "Abona a tu meta, aunque sea un monto pequeño.", "xp": 25, "route": "/metas", "auto": "has_emergency_fund"},
        ],
    },
    {
        "title": "Conoce los productos financieros",
        "description": "Entiende cómo funcionan antes de tomarlos.",
        "icon": "🏦",
        "tasks": [
            {"title": "Ten una cuenta de ahorros o billetera", "description": "Tu primer producto: sirve para recibir y organizar tu dinero.", "xp": 20, "auto": "has_savings_account"},
            {"title": "Entiende qué es el historial crediticio", "description": "La base de todo lo demás.", "xp": 30, "lesson": "que-es-historial"},
            {"title": "Descubre cómo funciona el puntaje", "description": "Los factores que suben y bajan tu score.", "xp": 30, "lesson": "como-funciona-puntaje"},
            {"title": "Aprende a leer tasas de interés", "description": "E.A., M.V. y tasa de usura.", "xp": 30, "lesson": "tasas-de-interes"},
        ],
    },
    {
        "title": "Construye hábitos de pago",
        "description": "La constancia es lo que más pesa en tu historial.",
        "icon": "⏰",
        "tasks": [
            {"title": "Paga a tiempo tus obligaciones por 30 días", "description": "Celular, servicios o cuotas, siempre antes de la fecha límite.", "xp": 40, "auto": "pays_on_time"},
            {"title": "Simula el costo de un producto básico", "description": "Usa el simulador de costo de crédito antes de decidir.", "xp": 20, "route": "/simuladores", "audience": "no_credit"},
            {"title": "Aprende a empezar tu historial desde cero", "description": "Qué productos suelen generar historial.", "xp": 30, "lesson": "empezar-desde-cero", "audience": "no_credit"},
            {"title": "Domina el cupo de tu tarjeta", "description": "La regla del 30 % y tus fechas clave.", "xp": 30, "lesson": "manejo-del-cupo", "audience": "has_credit"},
            {"title": "Revisa tu uso de cupo", "description": "Verifica en el simulador que estés por debajo del 30 %.", "xp": 20, "route": "/simuladores", "audience": "has_credit"},
            {"title": "Consulta tu reporte en una central de riesgo", "description": "Es gratis y no afecta tu puntaje.", "xp": 25, "audience": "has_credit"},
        ],
    },
    {
        "title": "Prepárate para tus metas",
        "description": "Llega a tu próximo gran paso con confianza.",
        "icon": "🚀",
        "tasks": [
            {"title": "Define tu meta grande", "description": "Viaje, independencia, estudio… ponle cifra y fecha.", "xp": 20, "route": "/metas"},
            {"title": "Entiende el costo total de una deuda", "description": "Por qué la cuota baja puede salir cara.", "xp": 30, "lesson": "costo-total"},
            {"title": "Conoce qué pasa si te atrasas", "description": "Mora, reportes y cómo recuperarte.", "xp": 30, "lesson": "si-me-atraso"},
            {"title": "Aprende a detectar el sobreendeudamiento", "description": "Señales de alerta a tiempo.", "xp": 30, "lesson": "sobreendeudamiento"},
        ],
    },
]

GLOSSARY = [
    {"term": "Historial crediticio", "definition": "Registro de cómo has manejado tus créditos y pagos. Lo guardan las centrales de riesgo."},
    {"term": "Puntaje crediticio (score)", "definition": "Número que resume qué tan probable es que pagues a tiempo, según tu historial."},
    {"term": "Central de riesgo", "definition": "Entidad que recopila información financiera de las personas, como DataCrédito Experian o TransUnion."},
    {"term": "Cupo", "definition": "Monto máximo que una entidad te presta en una tarjeta o línea de crédito."},
    {"term": "Fecha de corte", "definition": "Día en que la entidad suma las compras del periodo para generar tu extracto."},
    {"term": "Fecha límite de pago", "definition": "Último día para pagar sin generar intereses de mora."},
    {"term": "Tasa E.A.", "definition": "Tasa efectiva anual: lo que cuesta un crédito en un año incluyendo el interés compuesto."},
    {"term": "Tasa M.V.", "definition": "Tasa mes vencido: el interés que se cobra cada mes."},
    {"term": "Tasa de usura", "definition": "Tasa máxima legal que se puede cobrar en Colombia, certificada por la Superintendencia Financiera."},
    {"term": "Cuota de manejo", "definition": "Cobro fijo (mensual o anual) por tener un producto como una tarjeta."},
    {"term": "Intereses de mora", "definition": "Intereses adicionales que se cobran cuando pagas después de la fecha límite."},
    {"term": "Reporte negativo", "definition": "Registro en las centrales de riesgo de un incumplimiento de pago."},
    {"term": "Huella de consulta", "definition": "Registro que queda cada vez que una entidad consulta tu historial por una solicitud de crédito."},
    {"term": "Avance en efectivo", "definition": "Retiro de dinero con tu tarjeta de crédito. Suele cobrar intereses desde el primer día."},
    {"term": "Pago mínimo", "definition": "El valor más bajo que puedes pagar para no quedar en mora; el resto sigue generando intereses."},
    {"term": "Diferir", "definition": "Dividir una compra en varias cuotas mensuales. Más cuotas suelen significar más intereses."},
    {"term": "Fondo de emergencia", "definition": "Ahorro reservado solo para imprevistos, idealmente de 3 a 6 meses de gastos."},
    {"term": "Habeas data", "definition": "Tu derecho a conocer, actualizar y rectificar la información que hay sobre ti en bases de datos."},
]

FAQ = [
    {"keywords": ["historial", "empezar", "iniciar", "cero", "comenzar", "construir"], "answer": "Para empezar tu historial, lo más común es iniciar con un producto pequeño (un plan de celular a tu nombre, una tarjeta de cupo bajo) y pagarlo siempre a tiempo. Empieza con uno solo y úsalo con moderación.", "lesson": "empezar-desde-cero"},
    {"keywords": ["puntaje", "score", "calcula", "sube", "subir", "baja"], "answer": "El puntaje depende sobre todo de pagar a tiempo y de cuánto usas tu cupo. También influyen la antigüedad, las solicitudes recientes y la variedad de productos. Prueba el simulador de puntaje para verlo en acción.", "lesson": "como-funciona-puntaje"},
    {"keywords": ["cupo", "utilizar", "usar", "cuanto", "30", "tarjeta"], "answer": "Una buena regla es no deber más del 30 % de tu cupo al momento del corte. Si tu cupo es $1.000.000, intenta no pasar de $300.000.", "lesson": "manejo-del-cupo"},
    {"keywords": ["atraso", "atraso", "mora", "atrase", "atraso", "pago", "tarde", "reporte", "reportado", "negativo"], "answer": "Si te atrasas se generan intereses de mora. Antes de reportarte, la entidad debe avisarte con al menos 20 días. Si pagas, el dato negativo dura el doble del tiempo de la mora (máximo 4 años). Lo mejor: comunícate con tu entidad antes de que pase.", "lesson": "si-me-atraso"},
    {"keywords": ["tasa", "interes", "intereses", "usura", "ea", "efectiva", "mensual"], "answer": "La tasa E.A. te dice cuánto cuesta el crédito en un año. Compara siempre en E.A. y recuerda que la tasa de usura es el máximo legal. Una tasa de 2 % M.V. equivale a cerca de 26,8 % E.A.", "lesson": "tasas-de-interes"},
    {"keywords": ["solicitar", "varios", "creditos", "huella", "consulta", "consultas"], "answer": "Cada solicitud de crédito deja una huella de consulta. Muchas solicitudes en poco tiempo pueden interpretarse como riesgo. Pide solo lo que realmente necesitas.", "lesson": "como-funciona-puntaje"},
    {"keywords": ["producto", "productos", "primero", "cual", "elegir", "tarjeta", "credito"], "answer": "CrediStep no te dice qué producto comprar, pero sí qué revisar: tasa E.A., cuota de manejo, seguros y costo total. Usa el simulador de costo de crédito para comparar ofertas.", "lesson": "empezar-desde-cero"},
    {"keywords": ["ahorro", "ahorrar", "emergencia", "fondo", "imprevisto"], "answer": "Empieza tu fondo de emergencia con la meta de cubrir un mes de gastos básicos y luego crece a 3–6 meses. Ahorra apenas recibas tu dinero.", "lesson": "fondo-emergencia"},
    {"keywords": ["presupuesto", "gastos", "organizar", "plata", "dinero", "alcanza", "50"], "answer": "La regla 50/30/20 es un gran inicio: 50 % necesidades, 30 % gustos y 20 % ahorro. Registra tus gastos una semana para saber dónde estás.", "lesson": "presupuesto-50-30-20"},
    {"keywords": ["consultar", "reporte", "datacredito", "transunion", "central", "gratis"], "answer": "Puedes consultar tu reporte gratis en las centrales de riesgo (DataCrédito Experian, TransUnion). Consultarlo tú mismo no afecta tu puntaje.", "lesson": "que-es-historial"},
    {"keywords": ["deuda", "deudas", "endeudado", "sobreendeudamiento", "minimo", "pagar"], "answer": "Señales de alerta: cuotas mayores al 30 % de tus ingresos, pagar solo el mínimo o usar un crédito para pagar otro. Si las notas, frena nuevas compras a crédito y arma un plan de pagos.", "lesson": "sobreendeudamiento"},
    {"keywords": ["premium", "suscripcion", "precio", "pagar", "plus", "cuesta"], "answer": "CrediStep Plus cuesta $20.000 COP al mes e incluye simulador de puntaje, tabla de amortización completa, lecciones avanzadas y metas ilimitadas. Si tu universidad tiene licencia, lo tienes incluido.", "lesson": None},
]

"""Diagnóstico financiero inicial (Pantalla 2 y 3 del prototipo).

Las preguntas salen de los hallazgos de la encuesta de validación (n = 126):
productos que tienen, control de gastos, ahorro, conocimiento del historial,
hábitos de pago y meta principal.
"""
from dataclasses import dataclass, field

QUESTIONS: list[dict] = [
    {
        "id": "situacion",
        "title": "¿Cuál es tu situación hoy?",
        "subtitle": "Así entendemos de dónde vienen tus ingresos.",
        "type": "single",
        "options": [
            {"value": "estudiante", "label": "Estudio y recibo mesada", "icon": "🎓"},
            {"value": "primer_empleo", "label": "Tengo mi primer empleo o prácticas", "icon": "💼"},
            {"value": "independiente", "label": "Trabajo de forma independiente", "icon": "🛠️"},
            {"value": "sin_ingresos", "label": "Aún no tengo ingresos propios", "icon": "🌱"},
        ],
    },
    {
        "id": "productos",
        "title": "¿Actualmente tienes algún producto financiero?",
        "subtitle": "Puedes elegir varios.",
        "type": "multi",
        "options": [
            {"value": "cuenta_ahorros", "label": "Cuenta de ahorros o billetera digital", "icon": "🏦"},
            {"value": "tarjeta_credito", "label": "Tarjeta de crédito", "icon": "💳"},
            {"value": "credito", "label": "Crédito (educativo, consumo, celular…)", "icon": "📄"},
            {"value": "ninguno", "label": "Ninguno", "icon": "🚫"},
        ],
    },
    {
        "id": "gastos",
        "title": "¿Llevas control de tus gastos?",
        "subtitle": "Sé honesto, nadie te va a juzgar 😉",
        "type": "single",
        "options": [
            {"value": "registro", "label": "Sí, registro mis gastos y tengo presupuesto", "icon": "📊"},
            {"value": "aveces", "label": "Más o menos, a veces anoto", "icon": "📝"},
            {"value": "no", "label": "No llevo control", "icon": "🤷"},
        ],
    },
    {
        "id": "ahorro",
        "title": "¿Tienes un ahorro para emergencias?",
        "subtitle": "Dinero apartado para imprevistos.",
        "type": "single",
        "options": [
            {"value": "si", "label": "Sí, cubre un mes o más de mis gastos", "icon": "🛟"},
            {"value": "poco", "label": "Tengo algo, pero es poco", "icon": "🪙"},
            {"value": "no", "label": "No tengo ahorro", "icon": "🫙"},
        ],
    },
    {
        "id": "conocimiento",
        "title": "¿Qué tanto sabes sobre cómo funciona el historial crediticio?",
        "subtitle": "1 = no sé nada · 5 = lo conozco muy bien",
        "type": "scale",
        "min": 1,
        "max": 5,
    },
    {
        "id": "pagos",
        "title": "¿Pagas a tiempo tus obligaciones?",
        "subtitle": "Celular, servicios, cuotas o tarjetas.",
        "type": "single",
        "options": [
            {"value": "siempre", "label": "Siempre antes de la fecha límite", "icon": "✅"},
            {"value": "casi", "label": "Casi siempre", "icon": "⏳"},
            {"value": "atrasos", "label": "Me he atrasado varias veces", "icon": "⚠️"},
            {"value": "na", "label": "Aún no tengo obligaciones a mi nombre", "icon": "➖"},
        ],
    },
    {
        "id": "meta",
        "title": "¿Cuál es tu meta principal?",
        "subtitle": "Con esto armamos tu ruta personalizada.",
        "type": "single",
        "options": [
            {"value": "primera_tarjeta", "label": "Sacar mi primera tarjeta o crédito", "icon": "💳"},
            {"value": "independizarme", "label": "Independizarme", "icon": "🏠"},
            {"value": "viajar", "label": "Ahorrar para viajar", "icon": "✈️"},
            {"value": "estudiar", "label": "Financiar mis estudios", "icon": "📚"},
            {"value": "control", "label": "Tener control de mi dinero", "icon": "🧭"},
        ],
    },
]

LEVELS = [
    (85, "Listo para avanzar", "Tienes bases muy sólidas. Es momento de dar el siguiente paso con confianza."),
    (65, "Buen camino", "Vas muy bien. Con algunos ajustes estarás listo para tu próximo producto."),
    (40, "En construcción", "Tienes buenos hábitos financieros, ¡pero aún puedes mejorar!"),
    (0, "Primeros pasos", "Todos empezamos aquí. Tu ruta te va a guiar paso a paso."),
]


@dataclass
class DiagnosticOutcome:
    score: int
    level: str
    message: str
    segment: str
    has_credit: bool
    strengths: list[str] = field(default_factory=list)
    improvements: list[str] = field(default_factory=list)
    flags: set[str] = field(default_factory=set)


def validate_answers(answers: dict) -> list[str]:
    errors = []
    for q in QUESTIONS:
        value = answers.get(q["id"])
        if value is None or value == [] or value == "":
            errors.append(f"Falta responder: {q['title']}")
            continue
        if q["type"] == "scale":
            if not isinstance(value, int) or not q["min"] <= value <= q["max"]:
                errors.append(f"Valor fuera de rango en: {q['title']}")
        else:
            allowed = {o["value"] for o in q["options"]}
            values = value if isinstance(value, list) else [value]
            if q["type"] == "single" and isinstance(value, list):
                errors.append(f"Solo una opción en: {q['title']}")
            elif any(v not in allowed for v in values):
                errors.append(f"Opción inválida en: {q['title']}")
    return errors


def evaluate(answers: dict) -> DiagnosticOutcome:
    productos = set(answers["productos"])
    if "ninguno" in productos:
        productos = set()
    has_credit = bool(productos & {"tarjeta_credito", "credito"})
    strengths: list[str] = []
    improvements: list[str] = []
    flags: set[str] = set()
    score = 0

    # Productos (20)
    if "cuenta_ahorros" in productos:
        score += 10
        strengths.append("Tienes cuenta bancaria")
        flags.add("has_savings_account")
    else:
        improvements.append("Aún no tienes una cuenta de ahorros")
    if has_credit:
        score += 10
        strengths.append("Ya empezaste tu historial crediticio")
        flags.add("has_credit")
    else:
        improvements.append("No tienes historial crediticio todavía")

    # Control de gastos (20)
    gastos = answers["gastos"]
    score += {"registro": 20, "aveces": 10, "no": 0}[gastos]
    if gastos == "registro":
        strengths.append("Llevas control de tus gastos")
        flags.add("tracks_expenses")
    else:
        improvements.append("Organizar y registrar tus gastos")

    # Ahorro (15)
    ahorro = answers["ahorro"]
    score += {"si": 15, "poco": 7, "no": 0}[ahorro]
    if ahorro == "si":
        strengths.append("Tienes un fondo de emergencia")
        flags.add("has_emergency_fund")
    else:
        improvements.append("Construir tu fondo de emergencia")

    # Conocimiento (20)
    conocimiento = answers["conocimiento"]
    score += (conocimiento - 1) * 5
    if conocimiento >= 4:
        strengths.append("Conoces cómo funciona el historial")
    else:
        improvements.append("Entender cómo funciona el historial y el puntaje")

    # Hábitos de pago (25)
    pagos = answers["pagos"]
    score += {"siempre": 25, "casi": 12, "atrasos": 0, "na": 8}[pagos]
    if pagos == "siempre":
        strengths.append("Pagas a tiempo tus obligaciones")
        flags.add("pays_on_time")
    elif pagos in ("casi", "atrasos"):
        improvements.append("Pagar siempre antes de la fecha límite")

    score = max(0, min(100, score))
    level, message = next((name, msg) for threshold, name, msg in LEVELS if score >= threshold)

    situacion = answers["situacion"]
    if situacion == "estudiante":
        segment = "universitario"
    elif situacion in ("primer_empleo", "independiente"):
        segment = "primer_empleo"
    else:
        segment = "meta_clara" if answers["meta"] in ("viajar", "independizarme") else "universitario"

    return DiagnosticOutcome(
        score=score,
        level=level,
        message=message,
        segment=segment,
        has_credit=has_credit,
        strengths=strengths,
        improvements=improvements,
        flags=flags,
    )

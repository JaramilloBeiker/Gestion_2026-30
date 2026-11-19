"""Simuladores educativos. Son aproximaciones con fines pedagógicos:
CrediStep no recomienda productos ni reemplaza la información oficial
de cada entidad ni de las centrales de riesgo."""
import math


def monthly_rate_from_ea(ea_percent: float) -> float:
    """Convierte una tasa efectiva anual (%) en tasa mensual vencida (decimal)."""
    return (1 + ea_percent / 100) ** (1 / 12) - 1


# ------------------------------------------------------------ Uso de cupo
def card_utilization(credit_limit: float, balance: float) -> dict:
    utilization = 0.0 if credit_limit <= 0 else balance / credit_limit * 100
    if utilization <= 30:
        status, label = "good", "Saludable"
        advice = "¡Bien! Usar menos del 30 % de tu cupo muestra que manejas el crédito con control."
    elif utilization <= 60:
        status, label = "warning", "Moderado"
        advice = "Estás usando buena parte de tu cupo. Intenta bajar a menos del 30 % antes de la fecha de corte."
    else:
        status, label = "danger", "Alto"
        advice = "Un uso alto del cupo puede verse como dependencia del crédito. Abona antes del corte y evita nuevas compras."
    return {
        "utilization": round(utilization, 1),
        "status": status,
        "label": label,
        "advice": advice,
        "recommended_max_balance": round(credit_limit * 0.3),
        "available": round(max(credit_limit - balance, 0)),
    }


# ------------------------------------------------------- Costo de crédito
def loan_cost(
    amount: float,
    ea_rate: float,
    months: int,
    monthly_fee: float = 0,
    include_schedule: bool = True,
) -> dict:
    i = monthly_rate_from_ea(ea_rate)
    if i == 0:
        payment = amount / months
    else:
        payment = amount * i / (1 - (1 + i) ** (-months))
    schedule = []
    balance = amount
    for n in range(1, months + 1):
        interest = balance * i
        principal = payment - interest
        balance = max(balance - principal, 0)
        schedule.append(
            {
                "month": n,
                "payment": round(payment + monthly_fee),
                "interest": round(interest),
                "principal": round(principal),
                "fee": round(monthly_fee),
                "balance": round(balance),
            }
        )
    total_interest = payment * months - amount
    total_fees = monthly_fee * months
    total_paid = amount + total_interest + total_fees
    return {
        "monthly_rate": round(i * 100, 3),
        "monthly_payment": round(payment + monthly_fee),
        "total_interest": round(total_interest),
        "total_fees": round(total_fees),
        "total_paid": round(total_paid),
        "cost_ratio": round((total_paid / amount - 1) * 100, 1) if amount else 0,
        "schedule": schedule if include_schedule else schedule[:3],
        "schedule_truncated": not include_schedule,
    }


# --------------------------------------------------------- Pago atrasado
def late_payment(installment: float, days_late: int, default_ea_rate: float) -> dict:
    """Intereses de mora aproximados y línea de tiempo de consecuencias
    según la Ley 1266 de 2008 y la Ley 2157 de 2021 (habeas data financiero)."""
    late_interest = installment * ((1 + default_ea_rate / 100) ** (days_late / 365) - 1)
    months_late = math.ceil(days_late / 30) if days_late > 0 else 0
    permanence_months = min(months_late * 2, 48)
    timeline = [
        {"day": 1, "title": "Empiezan los intereses de mora",
         "text": "Desde el primer día de atraso la entidad puede cobrar intereses de mora sobre la cuota vencida."},
        {"day": 1, "title": "Posibles cobros de cobranza",
         "text": "Algunas entidades cobran gestión de cobranza. Revisa tu contrato para saber cuánto y desde cuándo."},
        {"day": 20, "title": "Aviso previo antes del reporte",
         "text": "Antes de reportarte negativamente, la entidad debe avisarte y darte al menos 20 días calendario para pagar o aclarar."},
        {"day": 30, "title": "Posible reporte negativo",
         "text": "Si no te pones al día, el atraso puede quedar registrado en las centrales de riesgo (DataCrédito Experian, TransUnion)."},
    ]
    return {
        "late_interest": round(late_interest),
        "total_due": round(installment + late_interest),
        "months_late": months_late,
        "negative_record_months": permanence_months,
        "timeline": [t for t in timeline if t["day"] <= max(days_late, 1)] if days_late < 30 else timeline,
        "all_timeline": timeline,
        "message": (
            "Si pagas, el dato negativo permanece el doble del tiempo que duró la mora, "
            "con un máximo de 4 años contados desde el pago."
            if days_late >= 30
            else "Todavía estás a tiempo: paga lo antes posible y comunícate con tu entidad."
        ),
    }


# --------------------------------------------------- Puntaje educativo
FACTORS = {
    "payments": ("Pagos a tiempo", 0.35),
    "utilization": ("Uso del cupo", 0.30),
    "history": ("Antigüedad del historial", 0.15),
    "inquiries": ("Solicitudes recientes", 0.10),
    "mix": ("Variedad de productos", 0.10),
}

TIPS = {
    "payments": "Paga todas tus cuotas antes de la fecha límite; es el factor que más pesa.",
    "utilization": "Mantén el uso de tu cupo por debajo del 30 % (idealmente cerca del 10 %).",
    "history": "No canceles tu producto más antiguo si lo manejas bien: la antigüedad suma.",
    "inquiries": "Evita pedir varios créditos en poco tiempo: cada solicitud deja huella.",
    "mix": "Con el tiempo, combinar productos (tarjeta + crédito) bien manejados ayuda.",
}


def estimate_score(
    on_time_pct: float, utilization_pct: float, history_months: int, inquiries_12m: int, product_types: int
) -> dict:
    if history_months == 0 and product_types == 0:
        return {
            "score": None,
            "band": "Sin historial",
            "message": "Aún no tienes historial: no es algo malo, solo significa que las entidades no tienen datos para evaluarte. Tu ruta te ayuda a empezar.",
            "factors": [],
            "tips": [TIPS["payments"], "Empieza con un producto básico de cupo bajo y úsalo con moderación."],
        }
    if utilization_pct <= 30:
        util = 1 - (utilization_pct / 30) * 0.15
    else:
        util = max(0.0, 0.85 - (utilization_pct - 30) / 70 * 0.85)
    sub = {
        "payments": (on_time_pct / 100) ** 2,
        "utilization": util,
        "history": min(1.0, history_months / 84) ** 0.7,
        "inquiries": max(0.0, 1 - 0.18 * inquiries_12m),
        "mix": min(1.0, product_types / 3),
    }
    weighted = sum(sub[k] * FACTORS[k][1] for k in FACTORS)
    score = round(150 + 800 * weighted)
    if score >= 800:
        band = "Excelente"
    elif score >= 700:
        band = "Bueno"
    elif score >= 550:
        band = "Aceptable"
    else:
        band = "Por mejorar"
    factors = [
        {"key": k, "label": FACTORS[k][0], "weight": int(FACTORS[k][1] * 100), "value": round(sub[k] * 100)}
        for k in FACTORS
    ]
    gaps = sorted(FACTORS, key=lambda k: (1 - sub[k]) * FACTORS[k][1], reverse=True)
    return {
        "score": score,
        "band": band,
        "message": "Estimación educativa en escala 150–950. No es tu puntaje real: consúltalo gratis en una central de riesgo.",
        "factors": factors,
        "tips": [TIPS[k] for k in gaps[:3] if sub[k] < 0.95] or ["¡Vas excelente! Mantén tus hábitos."],
    }

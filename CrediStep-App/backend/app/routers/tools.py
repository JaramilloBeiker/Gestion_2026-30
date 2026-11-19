"""Simuladores, asistente Step, glosario y suscripción Plus."""
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..config import FREE_GOALS_LIMIT, PREMIUM_MONTHLY_PRICE_COP, PREMIUM_YEARLY_PRICE_COP
from ..content import GLOSSARY
from ..database import get_session
from ..models import User
from ..schemas import AskIn, LateIn, LoanIn, PremiumIn, ScoreIn, UtilizationIn
from ..security import get_current_user
from ..services import assistant, simulators
from ..services.progress import add_activity

router = APIRouter(prefix="/api", tags=["herramientas"])


# ------------------------------------------------------------ Simuladores
@router.post("/simulators/utilization")
def sim_utilization(data: UtilizationIn, user: User = Depends(get_current_user)):
    return simulators.card_utilization(data.credit_limit, data.balance)


@router.post("/simulators/loan")
def sim_loan(data: LoanIn, user: User = Depends(get_current_user)):
    result = simulators.loan_cost(data.amount, data.ea_rate, data.months, data.monthly_fee,
                                  include_schedule=user.is_premium)
    result["premium_required_for_schedule"] = not user.is_premium
    return result


@router.post("/simulators/late-payment")
def sim_late(data: LateIn, user: User = Depends(get_current_user)):
    return simulators.late_payment(data.installment, data.days_late, data.default_ea_rate)


@router.post("/simulators/score")
def sim_score(data: ScoreIn, user: User = Depends(get_current_user)):
    if not user.is_premium:
        raise HTTPException(402, "El simulador de puntaje es parte de CrediStep Plus.")
    return simulators.estimate_score(**data.model_dump())


# ----------------------------------------------------- Asistente y glosario
@router.post("/assistant/ask")
def ask(data: AskIn, user: User = Depends(get_current_user)):
    return assistant.answer(data.question)


@router.get("/glossary")
def glossary():
    return sorted(GLOSSARY, key=lambda g: g["term"])


# --------------------------------------------------------------- Premium
PLUS_FEATURES = [
    {"feature": "Diagnóstico y ruta personalizada", "free": True, "plus": True},
    {"feature": "Lecciones esenciales con quiz", "free": True, "plus": True},
    {"feature": "Recordatorios de pagos y hábitos", "free": True, "plus": True},
    {"feature": "Simuladores de cupo, crédito y atrasos", "free": True, "plus": True},
    {"feature": f"Metas de ahorro", "free": f"Hasta {FREE_GOALS_LIMIT}", "plus": "Ilimitadas"},
    {"feature": "Tabla de amortización completa", "free": False, "plus": True},
    {"feature": "Simulador de puntaje crediticio", "free": False, "plus": True},
    {"feature": "Lecciones avanzadas", "free": False, "plus": True},
    {"feature": "Seguimiento detallado del progreso", "free": False, "plus": True},
]


@router.get("/premium/plans")
def plans():
    return {
        "plans": [
            {"id": "mensual", "name": "Plus mensual", "price": PREMIUM_MONTHLY_PRICE_COP, "period": "mes"},
            {"id": "anual", "name": "Plus anual", "price": PREMIUM_YEARLY_PRICE_COP, "period": "año",
             "badge": "2 meses gratis"},
        ],
        "features": PLUS_FEATURES,
    }


@router.post("/premium/activate")
def activate(data: PremiumIn, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Activación de demostración: en esta versión inicial no se procesan pagos reales."""
    if user.premium_plan == "institucional":
        raise HTTPException(400, "Ya tienes Plus incluido por la licencia de tu institución.")
    user.is_premium = True
    user.premium_plan = data.plan
    user.premium_until = date.today() + timedelta(days=365 if data.plan == "anual" else 30)
    add_activity(session, user, "premium", "¡Bienvenido a CrediStep Plus!", 20)
    session.commit()
    return {"ok": True, "premium_until": user.premium_until}


@router.post("/premium/cancel")
def cancel(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if user.premium_plan == "institucional":
        raise HTTPException(400, "Tu plan es institucional; lo administra tu universidad.")
    user.is_premium = False
    user.premium_plan = None
    user.premium_until = None
    session.add(user)
    session.commit()
    return {"ok": True}

"""Esquemas de entrada/salida de la API (validación con Pydantic)."""
from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: str = Field(min_length=5, max_length=120)
    password: str = Field(min_length=8, max_length=128)
    age: Optional[int] = Field(default=None, ge=14, le=99)
    institution_code: Optional[str] = None

    @field_validator("email")
    @classmethod
    def email_format(cls, v: str) -> str:
        v = v.strip().lower()
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Correo electrónico inválido")
        return v


class LoginIn(BaseModel):
    email: str
    password: str


class ProfileIn(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=80)
    age: Optional[int] = Field(default=None, ge=14, le=99)
    city: Optional[str] = Field(default=None, max_length=60)


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int]
    city: Optional[str]
    role: str
    segment: Optional[str]
    main_goal: Optional[str]
    is_premium: bool
    premium_plan: Optional[str]
    premium_until: Optional[date]
    xp: int
    onboarded: bool
    institution: Optional[str] = None
    created_at: Optional[datetime] = None


class TokenOut(BaseModel):
    token: str
    user: UserOut


class DiagnosticIn(BaseModel):
    answers: dict


class QuizIn(BaseModel):
    answers: list[int]


class GoalIn(BaseModel):
    title: str = Field(min_length=2, max_length=80)
    category: Literal["ahorro", "viaje", "independencia", "estudio", "emergencia", "compra"] = "ahorro"
    target_amount: float = Field(gt=0, le=1_000_000_000)
    current_amount: float = Field(default=0, ge=0)
    deadline: Optional[date] = None


class ContributionIn(BaseModel):
    amount: float = Field(gt=0, le=1_000_000_000)


class ReminderIn(BaseModel):
    title: str = Field(min_length=2, max_length=80)
    kind: Literal["pago", "corte", "ahorro", "habito"] = "pago"
    due_date: date
    recurrence: Literal["none", "weekly", "monthly"] = "none"
    amount: Optional[float] = Field(default=None, ge=0)


class UtilizationIn(BaseModel):
    credit_limit: float = Field(gt=0)
    balance: float = Field(ge=0)


class LoanIn(BaseModel):
    amount: float = Field(gt=0, le=1_000_000_000)
    ea_rate: float = Field(ge=0, le=100)
    months: int = Field(ge=1, le=120)
    monthly_fee: float = Field(default=0, ge=0)


class LateIn(BaseModel):
    installment: float = Field(gt=0)
    days_late: int = Field(ge=0, le=3650)
    default_ea_rate: float = Field(default=28, ge=0, le=100)


class ScoreIn(BaseModel):
    on_time_pct: float = Field(ge=0, le=100)
    utilization_pct: float = Field(ge=0, le=100)
    history_months: int = Field(ge=0, le=600)
    inquiries_12m: int = Field(ge=0, le=30)
    product_types: int = Field(ge=0, le=6)


class AskIn(BaseModel):
    question: str = Field(max_length=500)


class PremiumIn(BaseModel):
    plan: Literal["mensual", "anual"]

"""Modelos de datos (tablas SQLite) de CrediStep."""
from datetime import date, datetime
from typing import Optional

from pydantic import NaiveDatetime
from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


def local_now() -> datetime:
    """Hora local sin zona (la app corre localmente; las fechas se comparan con date.today())."""
    return datetime.now()


# ---------------------------------------------------------------- Usuarios
class Institution(SQLModel, table=True):
    """Universidad o colegio con licencia (fuente de ingreso B2B)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    code: str = Field(index=True, unique=True)
    license_seats: int = 500
    active: bool = True
    created_at: NaiveDatetime = Field(default_factory=local_now)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)
    password_hash: str
    age: Optional[int] = None
    city: Optional[str] = "Bogotá"
    role: str = "student"  # student | admin
    segment: Optional[str] = None  # universitario | primer_empleo | meta_clara
    main_goal: Optional[str] = None
    institution_id: Optional[int] = Field(default=None, foreign_key="institution.id")
    is_premium: bool = False
    premium_plan: Optional[str] = None  # mensual | anual | institucional
    premium_until: Optional[date] = None
    xp: int = 0
    onboarded: bool = False
    created_at: NaiveDatetime = Field(default_factory=local_now)


# ------------------------------------------------------------ Diagnóstico
class DiagnosticResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    answers: dict = Field(default_factory=dict, sa_column=Column(JSON))
    score: int
    level: str
    strengths: list = Field(default_factory=list, sa_column=Column(JSON))
    improvements: list = Field(default_factory=list, sa_column=Column(JSON))
    has_credit: bool = False
    created_at: NaiveDatetime = Field(default_factory=local_now)


# ---------------------------------------------------------- Ruta / Plan
class PlanStep(SQLModel, table=True):
    """Los 5 pasos de la ruta (prototipo: Mi plan)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    order: int
    title: str
    description: str
    icon: str


class PlanTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    step_id: int = Field(foreign_key="planstep.id")
    order: int
    title: str
    description: str
    xp: int = 20
    lesson_slug: Optional[str] = None
    action_route: Optional[str] = None  # ruta del frontend que ayuda a cumplirla
    # Personalización: all | no_credit | has_credit
    audience: str = "all"
    # Clave que, según el diagnóstico, permite marcarla como ya cumplida
    auto_complete_key: Optional[str] = None


class UserTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    task_id: int = Field(foreign_key="plantask.id")
    completed_at: NaiveDatetime = Field(default_factory=local_now)
    auto: bool = False


# ----------------------------------------------------------- Educación
class Module(SQLModel, table=True):
    """Módulos del MVP definidos en la validación (Cuadro 2)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    order: int
    title: str
    description: str
    icon: str
    color: str


class Lesson(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    module_id: int = Field(foreign_key="module.id")
    order: int
    title: str
    summary: str
    minutes: int = 4
    premium: bool = False
    xp: int = 30
    blocks: list = Field(default_factory=list, sa_column=Column(JSON))


class QuizQuestion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lesson_id: int = Field(foreign_key="lesson.id", index=True)
    question: str
    options: list = Field(default_factory=list, sa_column=Column(JSON))
    correct_index: int
    explanation: str


class LessonProgress(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    lesson_id: int = Field(foreign_key="lesson.id")
    completed: bool = False
    best_score: int = 0  # porcentaje de aciertos del quiz
    completed_at: Optional[NaiveDatetime] = None


# --------------------------------------------- Metas y recordatorios
class Goal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str
    category: str = "ahorro"  # ahorro | viaje | independencia | estudio | emergencia | compra
    target_amount: float
    current_amount: float = 0
    deadline: Optional[date] = None
    created_at: NaiveDatetime = Field(default_factory=local_now)


class Reminder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str
    kind: str = "pago"  # pago | corte | ahorro | habito
    due_date: date
    recurrence: str = "none"  # none | weekly | monthly
    amount: Optional[float] = None
    done: bool = False
    created_at: NaiveDatetime = Field(default_factory=local_now)


# --------------------------------------------------------- Actividad
class Activity(SQLModel, table=True):
    """Bitácora para racha, XP e historial de progreso."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    kind: str
    description: str
    xp: int = 0
    created_at: NaiveDatetime = Field(default_factory=local_now)

"""Carga inicial idempotente: contenido educativo, ruta y datos de demostración."""
import random
from datetime import date, datetime, timedelta

from sqlmodel import Session, select

from .content import MODULES, PLAN_STEPS
from .models import (
    Activity,
    DiagnosticResult,
    Goal,
    Institution,
    Lesson,
    LessonProgress,
    Module,
    PlanStep,
    PlanTask,
    QuizQuestion,
    Reminder,
    User,
    UserTask,
)
from .security import hash_password
from .services import diagnostic as diag_service
from .services.progress import auto_complete_from_diagnostic

DEMO_PASSWORD = "CrediStep2026"
INSTITUTION_CODE = "JAVERIANA2026"


def seed_content(session: Session) -> None:
    if session.exec(select(Module)).first():
        return
    for m_order, m in enumerate(MODULES, start=1):
        module = Module(
            slug=m["slug"], order=m_order, title=m["title"],
            description=m["description"], icon=m["icon"], color=m["color"],
        )
        session.add(module)
        session.flush()
        for l_order, l in enumerate(m["lessons"], start=1):
            lesson = Lesson(
                slug=l["slug"], module_id=module.id, order=l_order, title=l["title"],
                summary=l["summary"], minutes=l["minutes"], premium=l.get("premium", False),
                blocks=l["blocks"], xp=50 if l.get("premium") else 30,
            )
            session.add(lesson)
            session.flush()
            for q in l["quiz"]:
                session.add(QuizQuestion(
                    lesson_id=lesson.id, question=q["q"], options=q["options"],
                    correct_index=q["a"], explanation=q["e"],
                ))
    for s_order, s in enumerate(PLAN_STEPS, start=1):
        step = PlanStep(order=s_order, title=s["title"], description=s["description"], icon=s["icon"])
        session.add(step)
        session.flush()
        for t_order, t in enumerate(s["tasks"], start=1):
            session.add(PlanTask(
                step_id=step.id, order=t_order, title=t["title"], description=t["description"],
                xp=t["xp"], lesson_slug=t.get("lesson"), action_route=t.get("route"),
                audience=t.get("audience", "all"), auto_complete_key=t.get("auto"),
            ))
    session.commit()


def _diagnose(session: Session, user: User, answers: dict, when: datetime) -> None:
    outcome = diag_service.evaluate(answers)
    session.add(DiagnosticResult(
        user_id=user.id, answers=answers, score=outcome.score, level=outcome.level,
        strengths=outcome.strengths, improvements=outcome.improvements,
        has_credit=outcome.has_credit, created_at=when,
    ))
    user.segment = outcome.segment
    user.main_goal = answers["meta"]
    user.onboarded = True
    auto_complete_from_diagnostic(session, user, outcome.flags)


def seed_demo(session: Session) -> None:
    if session.exec(select(Institution)).first():
        return
    rng = random.Random(42)
    jave = Institution(name="Pontificia Universidad Javeriana", code=INSTITUTION_CODE, license_seats=500)
    session.add(jave)
    session.flush()

    admin = User(
        name="Bienestar Universitario Javeriana", email="admin@javeriana.edu.co",
        password_hash=hash_password(DEMO_PASSWORD), role="admin",
        institution_id=jave.id, is_premium=True, premium_plan="institucional", onboarded=True,
    )
    demo = User(
        name="Valentina Rojas", email="demo@credistep.co", password_hash=hash_password(DEMO_PASSWORD),
        age=20, institution_id=jave.id, is_premium=True, premium_plan="institucional",
    )
    session.add_all([admin, demo])
    session.flush()

    now = datetime.now()
    _diagnose(session, demo, {
        "situacion": "estudiante", "productos": ["cuenta_ahorros"], "gastos": "aveces",
        "ahorro": "poco", "conocimiento": 2, "pagos": "siempre", "meta": "primera_tarjeta",
    }, now - timedelta(days=9))

    lessons = {l.slug: l for l in session.exec(select(Lesson)).all()}
    for i, slug in enumerate(["presupuesto-50-30-20", "que-es-historial"]):
        session.add(LessonProgress(user_id=demo.id, lesson_id=lessons[slug].id, completed=True,
                                   best_score=100, completed_at=now - timedelta(days=6 - i * 2)))
        for t in session.exec(select(PlanTask).where(PlanTask.lesson_slug == slug)).all():
            session.add(UserTask(user_id=demo.id, task_id=t.id, auto=True))
    first_reminder_task = session.exec(select(PlanTask).where(PlanTask.action_route == "/recordatorios")).first()
    session.add(UserTask(user_id=demo.id, task_id=first_reminder_task.id))

    session.add_all([
        Goal(user_id=demo.id, title="Fondo de emergencia", category="emergencia",
             target_amount=900_000, current_amount=320_000, deadline=date.today() + timedelta(days=120)),
        Goal(user_id=demo.id, title="Viaje a Cartagena", category="viaje",
             target_amount=1_500_000, current_amount=450_000, deadline=date.today() + timedelta(days=210)),
        Reminder(user_id=demo.id, title="Pagar plan de celular", kind="pago",
                 due_date=date.today() + timedelta(days=3), recurrence="monthly", amount=45_000),
        Reminder(user_id=demo.id, title="Ahorrar 20 % de la mesada", kind="ahorro",
                 due_date=date.today() + timedelta(days=6), recurrence="monthly", amount=160_000),
        Reminder(user_id=demo.id, title="Registrar gastos de la semana", kind="habito",
                 due_date=date.today() - timedelta(days=1), recurrence="weekly", done=True),
    ])
    demo.xp = 0
    for d, (desc, xp) in enumerate([
        ("Completaste tu diagnóstico", 50), ("Lección: Tu presupuesto 50/30/20", 30),
        ("Creaste un recordatorio", 15), ("Lección: ¿Qué es el historial crediticio?", 30),
        ("Aporte a Fondo de emergencia", 10), ("Aporte a Viaje a Cartagena", 10),
    ]):
        when = now - timedelta(days=5 - d)
        session.add(Activity(user_id=demo.id, kind="seed", description=desc, xp=xp, created_at=when))
        demo.xp += xp
    session.add(demo)

    # Estudiantes simulados para el panel institucional
    first_names = ["Santiago", "Mariana", "Juan", "Sofía", "Andrés", "Camila", "Daniel", "Isabella",
                   "Felipe", "Gabriela", "Mateo", "Luciana", "Nicolás", "Paula", "Samuel", "Sara",
                   "Tomás", "Antonella", "David", "Manuela", "Julián", "Daniela", "Sebastián", "Juliana"]
    last_names = ["Gómez", "Rodríguez", "Martínez", "López", "Hernández", "Díaz", "Moreno", "Castro"]
    all_lessons = list(lessons.values())
    for i, fn in enumerate(first_names):
        u = User(
            name=f"{fn} {rng.choice(last_names)}", email=f"estudiante{i + 1}@javeriana.edu.co",
            password_hash=hash_password(DEMO_PASSWORD), age=rng.randint(18, 24),
            institution_id=jave.id, is_premium=True, premium_plan="institucional",
            created_at=now - timedelta(days=rng.randint(1, 60)),
        )
        session.add(u)
        session.flush()
        products = rng.choice([["ninguno"], ["cuenta_ahorros"], ["cuenta_ahorros"], ["cuenta_ahorros", "tarjeta_credito"], ["cuenta_ahorros", "credito"]])
        _diagnose(session, u, {
            "situacion": rng.choice(["estudiante", "estudiante", "primer_empleo", "sin_ingresos"]),
            "productos": products, "gastos": rng.choice(["registro", "aveces", "no"]),
            "ahorro": rng.choice(["si", "poco", "no", "no"]), "conocimiento": rng.choice([1, 2, 2, 3, 3, 4]),
            "pagos": rng.choice(["siempre", "casi", "na", "atrasos"]),
            "meta": rng.choice(["primera_tarjeta", "independizarme", "viajar", "estudiar", "control"]),
        }, u.created_at)
        for lesson in rng.sample(all_lessons, rng.randint(0, 7)):
            session.add(LessonProgress(user_id=u.id, lesson_id=lesson.id, completed=True,
                                       best_score=rng.choice([50, 100, 100]),
                                       completed_at=u.created_at + timedelta(days=rng.randint(0, 10))))
            u.xp += lesson.xp
        session.add(Activity(user_id=u.id, kind="seed", description="Actividad", xp=0,
                             created_at=now - timedelta(days=rng.randint(0, 14))))
        session.add(u)
    session.commit()


def run_seed(session: Session) -> None:
    seed_content(session)
    seed_demo(session)

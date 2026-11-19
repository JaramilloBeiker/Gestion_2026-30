"""Índice de preparación crediticia, XP, racha y plan personalizado."""
from datetime import date, datetime, timedelta

from sqlmodel import Session, func, select

from ..models import (
    Activity,
    DiagnosticResult,
    Goal,
    Lesson,
    LessonProgress,
    PlanStep,
    PlanTask,
    Reminder,
    User,
    UserTask,
)

XP_LEVELS = [
    (0, "Semilla"),
    (150, "Brote"),
    (400, "Planta"),
    (800, "Árbol"),
    (1400, "Bosque"),
]


def add_activity(session: Session, user: User, kind: str, description: str, xp: int = 0) -> None:
    user.xp += xp
    session.add(Activity(user_id=user.id, kind=kind, description=description, xp=xp))
    session.add(user)


def xp_level(xp: int) -> dict:
    current = XP_LEVELS[0]
    nxt = None
    for i, lvl in enumerate(XP_LEVELS):
        if xp >= lvl[0]:
            current = lvl
            nxt = XP_LEVELS[i + 1] if i + 1 < len(XP_LEVELS) else None
    span = (nxt[0] - current[0]) if nxt else 1
    return {
        "name": current[1],
        "level": XP_LEVELS.index(current) + 1,
        "xp": xp,
        "next_name": nxt[1] if nxt else None,
        "next_xp": nxt[0] if nxt else None,
        "pct": 100 if not nxt else round((xp - current[0]) / span * 100),
    }


def streak_days(session: Session, user_id: int) -> int:
    rows = session.exec(select(Activity.created_at).where(Activity.user_id == user_id)).all()
    days = {r.date() for r in rows}
    today = date.today()
    cursor = today if today in days else today - timedelta(days=1)
    streak = 0
    while cursor in days:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def latest_diagnostic(session: Session, user_id: int) -> DiagnosticResult | None:
    return session.exec(
        select(DiagnosticResult)
        .where(DiagnosticResult.user_id == user_id)
        .order_by(DiagnosticResult.created_at.desc(), DiagnosticResult.id.desc())
    ).first()


def tasks_for_user(session: Session, diag: DiagnosticResult | None) -> list[PlanTask]:
    has_credit = bool(diag and diag.has_credit)
    tasks = session.exec(select(PlanTask).order_by(PlanTask.step_id, PlanTask.order)).all()
    return [
        t for t in tasks
        if t.audience == "all" or (t.audience == "has_credit") == has_credit
    ]


def build_plan(session: Session, user: User) -> dict:
    diag = latest_diagnostic(session, user.id)
    tasks = tasks_for_user(session, diag)
    done = {
        ut.task_id: ut
        for ut in session.exec(select(UserTask).where(UserTask.user_id == user.id)).all()
    }
    steps = session.exec(select(PlanStep).order_by(PlanStep.order)).all()
    out_steps = []
    next_task = None
    total = completed = 0
    for step in steps:
        st_tasks = [t for t in tasks if t.step_id == step.id]
        items = []
        for t in st_tasks:
            is_done = t.id in done
            total += 1
            completed += is_done
            item = {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "xp": t.xp,
                "lesson_slug": t.lesson_slug,
                "action_route": t.action_route,
                "done": is_done,
                "auto": bool(is_done and done[t.id].auto),
            }
            items.append(item)
            if not is_done and next_task is None:
                next_task = {**item, "step_title": step.title}
        step_done = sum(i["done"] for i in items)
        out_steps.append(
            {
                "id": step.id,
                "order": step.order,
                "title": step.title,
                "description": step.description,
                "icon": step.icon,
                "tasks": items,
                "completed": step_done,
                "total": len(items),
                "status": "done" if items and step_done == len(items) else ("active" if step_done else "pending"),
            }
        )
    # El primer paso no terminado es el "activo" en el GPS
    for s in out_steps:
        if s["status"] != "done":
            s["status"] = "active"
            break
    return {
        "steps": out_steps,
        "completed": completed,
        "total": total,
        "pct": round(completed / total * 100) if total else 0,
        "next_task": next_task,
    }


def auto_complete_from_diagnostic(session: Session, user: User, flags: set[str]) -> None:
    existing = {
        ut.task_id for ut in session.exec(select(UserTask).where(UserTask.user_id == user.id)).all()
    }
    for t in session.exec(select(PlanTask).where(PlanTask.auto_complete_key.is_not(None))).all():
        if t.auto_complete_key in flags and t.id not in existing:
            session.add(UserTask(user_id=user.id, task_id=t.id, auto=True))


def complete_lesson_tasks(session: Session, user: User, lesson_slug: str) -> None:
    tasks = session.exec(select(PlanTask).where(PlanTask.lesson_slug == lesson_slug)).all()
    for t in tasks:
        exists = session.exec(
            select(UserTask).where(UserTask.user_id == user.id, UserTask.task_id == t.id)
        ).first()
        if not exists:
            session.add(UserTask(user_id=user.id, task_id=t.id, auto=True))
            add_activity(session, user, "task", f"Completaste: {t.title}", t.xp)


def complete_task_by_title(session: Session, user: User, title: str) -> None:
    """Marca una tarea de la ruta cuando el usuario hace la acción en otra sección."""
    task = session.exec(select(PlanTask).where(PlanTask.title == title)).first()
    if not task:
        return
    exists = session.exec(
        select(UserTask).where(UserTask.user_id == user.id, UserTask.task_id == task.id)
    ).first()
    if not exists:
        session.add(UserTask(user_id=user.id, task_id=task.id, auto=True))
        add_activity(session, user, "task", f"Completaste: {task.title}", task.xp)


def learning_stats(session: Session, user: User) -> dict:
    lessons = session.exec(select(Lesson)).all()
    accessible = [l for l in lessons if user.is_premium or not l.premium]
    completed_ids = set(
        session.exec(
            select(LessonProgress.lesson_id).where(
                LessonProgress.user_id == user.id, LessonProgress.completed == True  # noqa: E712
            )
        ).all()
    )
    done_accessible = sum(1 for l in accessible if l.id in completed_ids)
    return {
        "completed": len(completed_ids),
        "total": len(lessons),
        "accessible": len(accessible),
        "pct": round(done_accessible / len(accessible) * 100) if accessible else 0,
    }


def habits_score(session: Session, user: User) -> int:
    parts = []
    reminders = session.exec(select(Reminder).where(Reminder.user_id == user.id)).all()
    past = [r for r in reminders if r.due_date <= date.today() or r.done]
    if past:
        parts.append(sum(r.done for r in past) / len(past) * 100)
    goals = session.exec(select(Goal).where(Goal.user_id == user.id)).all()
    if goals:
        parts.append(
            sum(min(g.current_amount / g.target_amount, 1) for g in goals if g.target_amount) / len(goals) * 100
        )
    return round(sum(parts) / len(parts)) if parts else 0


def readiness(session: Session, user: User, plan: dict | None = None) -> dict:
    diag = latest_diagnostic(session, user.id)
    plan = plan or build_plan(session, user)
    learning = learning_stats(session, user)
    habits = habits_score(session, user)
    diag_score = diag.score if diag else 0
    components = [
        {"key": "diagnostic", "label": "Situación financiera", "value": diag_score, "weight": 35},
        {"key": "plan", "label": "Avance en tu ruta", "value": plan["pct"], "weight": 30},
        {"key": "learning", "label": "Educación aplicada", "value": learning["pct"], "weight": 20},
        {"key": "habits", "label": "Hábitos y metas", "value": habits, "weight": 15},
    ]
    index = round(sum(c["value"] * c["weight"] for c in components) / 100)
    if index >= 80:
        label = "¡Listo para tu siguiente paso!"
    elif index >= 60:
        label = "Casi listo"
    elif index >= 35:
        label = "En construcción"
    else:
        label = "Empezando"
    return {"index": index, "label": label, "components": components}


def recommended_action(diag: DiagnosticResult | None, plan: dict) -> dict:
    """Pantalla 5 del prototipo: 'Acción recomendada'. Nunca recomienda marcas
    ni entidades: explica un *tipo* de paso y qué revisar antes de darlo."""
    if diag is None:
        return {
            "title": "Haz tu diagnóstico",
            "product": None,
            "text": "Responde 7 preguntas rápidas y armamos tu ruta personalizada.",
            "checklist": [],
            "route": "/diagnostico",
        }
    flags_improve = " ".join(diag.improvements).lower()
    if "gastos" in flags_improve:
        return {
            "title": "Organiza tus gastos este mes",
            "product": "Presupuesto 50/30/20",
            "text": "Antes de pensar en crédito, saber a dónde va tu dinero te da control y confianza.",
            "checklist": ["Anota todos tus gastos por 7 días", "Separa necesidades y gustos", "Define cuánto vas a ahorrar"],
            "route": "/aprende/presupuesto-50-30-20",
        }
    if not diag.has_credit:
        return {
            "title": "Conoce un producto básico",
            "product": "Tarjeta de crédito de cupo bajo",
            "text": "Un producto que puede ayudarte a construir historial crediticio de manera responsable. Tú decides si y cuándo tomarlo.",
            "checklist": ["Revisa la cuota de manejo", "Revisa la tasa de interés (E.A.)", "Paga el total a tiempo cada mes"],
            "route": "/simuladores",
        }
    return {
        "title": "Cuida el uso de tu cupo",
        "product": "Utilización por debajo del 30 %",
        "text": "Ya tienes historial: ahora lo importante es mantenerlo sano mes a mes.",
        "checklist": ["Paga antes de la fecha límite", "Usa menos del 30 % del cupo", "Consulta tu reporte gratis en una central de riesgo"],
        "route": "/simuladores",
    }


def weekly_activity(session: Session, user_id: int) -> list[dict]:
    today = date.today()
    start = today - timedelta(days=6)
    rows = session.exec(
        select(Activity).where(
            Activity.user_id == user_id,
            Activity.created_at >= datetime.combine(start, datetime.min.time()),
        )
    ).all()
    names = ["L", "M", "X", "J", "V", "S", "D"]
    out = []
    for n in range(7):
        d = start + timedelta(days=n)
        out.append(
            {
                "date": d.isoformat(),
                "label": names[d.weekday()],
                "xp": sum(a.xp for a in rows if a.created_at.date() == d),
            }
        )
    return out


def count_users(session: Session, institution_id: int) -> int:
    return session.exec(
        select(func.count()).select_from(User).where(
            User.institution_id == institution_id, User.role == "student"
        )
    ).one()

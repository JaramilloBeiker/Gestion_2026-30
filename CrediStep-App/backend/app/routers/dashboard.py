from collections import Counter
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..database import get_session
from ..models import Activity, Institution, Lesson, LessonProgress, Module, Reminder, User
from ..security import get_admin_user, get_current_user
from ..services.progress import (
    build_plan,
    latest_diagnostic,
    learning_stats,
    readiness,
    recommended_action,
    streak_days,
    weekly_activity,
    xp_level,
)
from .reminders import reminder_out

router = APIRouter(prefix="/api", tags=["progreso"])


@router.get("/dashboard")
def dashboard(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    plan = build_plan(session, user)
    diag = latest_diagnostic(session, user.id)
    reminders = session.exec(
        select(Reminder).where(Reminder.user_id == user.id, Reminder.done == False)  # noqa: E712
        .order_by(Reminder.due_date)
    ).all()
    activity = session.exec(
        select(Activity).where(Activity.user_id == user.id).order_by(Activity.created_at.desc()).limit(6)
    ).all()
    return {
        "readiness": readiness(session, user, plan),
        "diagnostic": {"score": diag.score, "level": diag.level, "strengths": diag.strengths,
                       "improvements": diag.improvements} if diag else None,
        "plan": {"pct": plan["pct"], "completed": plan["completed"], "total": plan["total"],
                 "next_task": plan["next_task"],
                 "steps": [{"title": s["title"], "icon": s["icon"], "status": s["status"],
                            "completed": s["completed"], "total": s["total"]} for s in plan["steps"]]},
        "learning": learning_stats(session, user),
        "level": xp_level(user.xp),
        "streak": streak_days(session, user.id),
        "week": weekly_activity(session, user.id),
        "reminders": [reminder_out(r) for r in reminders[:4]],
        "activity": [{"description": a.description, "xp": a.xp, "created_at": a.created_at} for a in activity],
        "recommended": recommended_action(diag, plan),
    }


# ------------------------------------------------- Panel institucional (B2B)
@router.get("/admin/overview")
def admin_overview(admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    """Solo datos agregados: la institución no ve información individual de los
    estudiantes (principio de privacidad, Ley 1581 de 2012)."""
    inst = session.get(Institution, admin.institution_id)
    students = session.exec(
        select(User).where(User.institution_id == inst.id, User.role == "student")
    ).all()
    ids = [s.id for s in students]
    week_ago = datetime.now() - timedelta(days=7)
    active_ids = set(
        session.exec(select(Activity.user_id).where(Activity.user_id.in_(ids), Activity.created_at >= week_ago)).all()
    ) if ids else set()

    levels, improvements, segments, goals = Counter(), Counter(), Counter(), Counter()
    readiness_values, diag_scores = [], []
    for s in students:
        d = latest_diagnostic(session, s.id)
        if d:
            levels[d.level] += 1
            improvements.update(d.improvements)
            diag_scores.append(d.score)
        segments[s.segment or "sin_diagnostico"] += 1
        if s.main_goal:
            goals[s.main_goal] += 1
        readiness_values.append(readiness(session, s)["index"])

    modules_out = []
    for m in session.exec(select(Module).order_by(Module.order)).all():
        lesson_ids = session.exec(select(Lesson.id).where(Lesson.module_id == m.id)).all()
        done = session.exec(
            select(LessonProgress).where(
                LessonProgress.lesson_id.in_(lesson_ids), LessonProgress.user_id.in_(ids),
                LessonProgress.completed == True,  # noqa: E712
            )
        ).all() if ids and lesson_ids else []
        possible = len(lesson_ids) * len(ids)
        modules_out.append({"title": m.title, "icon": m.icon, "color": m.color,
                            "pct": round(len(done) / possible * 100) if possible else 0})

    # Nuevos registros por semana (últimas 8 semanas)
    weeks = []
    today = date.today()
    for w in range(7, -1, -1):
        start = today - timedelta(days=today.weekday() + 7 * w)
        end = start + timedelta(days=7)
        weeks.append({"label": start.strftime("%d/%m"),
                      "count": sum(1 for s in students if start <= s.created_at.date() < end)})

    level_order = ["Primeros pasos", "En construcción", "Buen camino", "Listo para avanzar"]
    return {
        "institution": {"name": inst.name, "code": inst.code, "seats": inst.license_seats},
        "students": len(students),
        "active_week": len(active_ids),
        "avg_readiness": round(sum(readiness_values) / len(readiness_values)) if readiness_values else 0,
        "avg_diagnostic": round(sum(diag_scores) / len(diag_scores)) if diag_scores else 0,
        "levels": [{"label": l, "count": levels.get(l, 0)} for l in level_order],
        "top_needs": [{"label": k, "count": v} for k, v in improvements.most_common(5)],
        "segments": [{"label": k, "count": v} for k, v in segments.most_common()],
        "goals": [{"label": k, "count": v} for k, v in goals.most_common()],
        "modules": modules_out,
        "signups": weeks,
    }

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..models import Lesson, LessonProgress, Module, QuizQuestion, User
from ..schemas import QuizIn
from ..security import get_current_user
from ..services.progress import add_activity, complete_lesson_tasks

router = APIRouter(prefix="/api/learning", tags=["educación"])
PASS_PCT = 60


def _progress_map(session: Session, user_id: int) -> dict[int, LessonProgress]:
    return {
        p.lesson_id: p
        for p in session.exec(select(LessonProgress).where(LessonProgress.user_id == user_id)).all()
    }


@router.get("/modules")
def modules(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    progress = _progress_map(session, user.id)
    out = []
    for m in session.exec(select(Module).order_by(Module.order)).all():
        lessons = session.exec(select(Lesson).where(Lesson.module_id == m.id).order_by(Lesson.order)).all()
        items = [
            {
                "slug": l.slug,
                "title": l.title,
                "summary": l.summary,
                "minutes": l.minutes,
                "xp": l.xp,
                "premium": l.premium,
                "locked": l.premium and not user.is_premium,
                "completed": bool(progress.get(l.id) and progress[l.id].completed),
                "best_score": progress[l.id].best_score if l.id in progress else None,
            }
            for l in lessons
        ]
        done = sum(i["completed"] for i in items)
        out.append(
            {
                "slug": m.slug, "title": m.title, "description": m.description,
                "icon": m.icon, "color": m.color, "lessons": items,
                "completed": done, "total": len(items),
                "pct": round(done / len(items) * 100) if items else 0,
            }
        )
    return out


def _get_lesson(session: Session, slug: str, user: User) -> Lesson:
    lesson = session.exec(select(Lesson).where(Lesson.slug == slug)).first()
    if not lesson:
        raise HTTPException(404, "Lección no encontrada.")
    if lesson.premium and not user.is_premium:
        raise HTTPException(402, "Esta lección es parte de CrediStep Plus.")
    return lesson


@router.get("/lessons/{slug}")
def lesson_detail(slug: str, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    lesson = _get_lesson(session, slug, user)
    module = session.get(Module, lesson.module_id)
    questions = session.exec(select(QuizQuestion).where(QuizQuestion.lesson_id == lesson.id)).all()
    siblings = session.exec(select(Lesson).where(Lesson.module_id == module.id).order_by(Lesson.order)).all()
    idx = [s.id for s in siblings].index(lesson.id)
    nxt = siblings[idx + 1] if idx + 1 < len(siblings) else None
    progress = _progress_map(session, user.id).get(lesson.id)
    return {
        "slug": lesson.slug,
        "title": lesson.title,
        "summary": lesson.summary,
        "minutes": lesson.minutes,
        "xp": lesson.xp,
        "blocks": lesson.blocks,
        "module": {"slug": module.slug, "title": module.title, "icon": module.icon, "color": module.color},
        "quiz": [{"id": q.id, "question": q.question, "options": q.options} for q in questions],
        "completed": bool(progress and progress.completed),
        "best_score": progress.best_score if progress else None,
        "next": {"slug": nxt.slug, "title": nxt.title, "locked": nxt.premium and not user.is_premium} if nxt else None,
    }


@router.post("/lessons/{slug}/quiz")
def submit_quiz(slug: str, data: QuizIn, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    lesson = _get_lesson(session, slug, user)
    questions = session.exec(select(QuizQuestion).where(QuizQuestion.lesson_id == lesson.id)).all()
    if len(data.answers) != len(questions):
        raise HTTPException(422, "Responde todas las preguntas del quiz.")
    results = []
    correct = 0
    for q, a in zip(questions, data.answers):
        ok = a == q.correct_index
        correct += ok
        results.append({"id": q.id, "correct": ok, "correct_index": q.correct_index, "explanation": q.explanation})
    pct = round(correct / len(questions) * 100) if questions else 100
    passed = pct >= PASS_PCT

    progress = session.exec(
        select(LessonProgress).where(LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson.id)
    ).first()
    first_completion = False
    if not progress:
        progress = LessonProgress(user_id=user.id, lesson_id=lesson.id)
    progress.best_score = max(progress.best_score, pct)
    if passed and not progress.completed:
        progress.completed = True
        progress.completed_at = datetime.now()
        first_completion = True
    session.add(progress)
    xp = 0
    if first_completion:
        xp = lesson.xp + (10 if pct == 100 else 0)
        add_activity(session, user, "lesson", f"Lección: {lesson.title}", xp)
        complete_lesson_tasks(session, user, lesson.slug)
    session.commit()
    return {"score": pct, "passed": passed, "xp_earned": xp, "results": results, "pass_pct": PASS_PCT}

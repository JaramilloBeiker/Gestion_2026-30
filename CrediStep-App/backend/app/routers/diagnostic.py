from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..models import DiagnosticResult, User
from ..schemas import DiagnosticIn
from ..security import get_current_user
from ..services import diagnostic as svc
from ..services.progress import add_activity, auto_complete_from_diagnostic, latest_diagnostic

router = APIRouter(prefix="/api/diagnostic", tags=["diagnóstico"])


def result_out(r: DiagnosticResult) -> dict:
    message = next(msg for threshold, name, msg in svc.LEVELS if r.score >= threshold)
    return {
        "id": r.id,
        "score": r.score,
        "level": r.level,
        "message": message,
        "strengths": r.strengths,
        "improvements": r.improvements,
        "has_credit": r.has_credit,
        "answers": r.answers,
        "created_at": r.created_at,
    }


@router.get("/questions")
def questions():
    return svc.QUESTIONS


@router.post("", status_code=201)
def submit(data: DiagnosticIn, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    errors = svc.validate_answers(data.answers)
    if errors:
        raise HTTPException(422, errors[0])
    outcome = svc.evaluate(data.answers)
    first_time = latest_diagnostic(session, user.id) is None
    result = DiagnosticResult(
        user_id=user.id,
        answers=data.answers,
        score=outcome.score,
        level=outcome.level,
        strengths=outcome.strengths,
        improvements=outcome.improvements,
        has_credit=outcome.has_credit,
    )
    session.add(result)
    user.segment = outcome.segment
    user.main_goal = data.answers["meta"]
    user.onboarded = True
    auto_complete_from_diagnostic(session, user, outcome.flags)
    add_activity(
        session, user, "diagnostic",
        "Completaste tu diagnóstico" if first_time else "Actualizaste tu diagnóstico",
        50 if first_time else 10,
    )
    session.commit()
    session.refresh(result)
    return result_out(result)


@router.get("/latest")
def latest(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    r = latest_diagnostic(session, user.id)
    if not r:
        raise HTTPException(404, "Aún no has hecho tu diagnóstico.")
    return result_out(r)


@router.get("/history")
def history(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    rows = session.exec(
        select(DiagnosticResult).where(DiagnosticResult.user_id == user.id).order_by(DiagnosticResult.created_at)
    ).all()
    return [{"score": r.score, "level": r.level, "created_at": r.created_at} for r in rows]

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..config import FREE_GOALS_LIMIT
from ..database import get_session
from ..models import Goal, User
from ..schemas import ContributionIn, GoalIn
from ..security import get_current_user
from ..services.progress import add_activity, complete_task_by_title

router = APIRouter(prefix="/api/goals", tags=["metas"])


def goal_out(g: Goal) -> dict:
    pct = min(round(g.current_amount / g.target_amount * 100), 100) if g.target_amount else 0
    return {**g.model_dump(), "pct": pct, "remaining": max(g.target_amount - g.current_amount, 0)}


def _own(session: Session, goal_id: int, user: User) -> Goal:
    g = session.get(Goal, goal_id)
    if not g or g.user_id != user.id:
        raise HTTPException(404, "Meta no encontrada.")
    return g


@router.get("")
def list_goals(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    goals = session.exec(select(Goal).where(Goal.user_id == user.id).order_by(Goal.created_at)).all()
    return {
        "goals": [goal_out(g) for g in goals],
        "limit": None if user.is_premium else FREE_GOALS_LIMIT,
    }


@router.post("", status_code=201)
def create_goal(data: GoalIn, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    count = len(session.exec(select(Goal.id).where(Goal.user_id == user.id)).all())
    if not user.is_premium and count >= FREE_GOALS_LIMIT:
        raise HTTPException(402, f"El plan gratuito permite {FREE_GOALS_LIMIT} metas. Pásate a Plus para tener metas ilimitadas.")
    goal = Goal(user_id=user.id, **data.model_dump())
    session.add(goal)
    add_activity(session, user, "goal", f"Nueva meta: {goal.title}", 15)
    if goal.category == "emergencia":
        complete_task_by_title(session, user, "Crea una meta de emergencia")
        if goal.current_amount > 0:
            complete_task_by_title(session, user, "Haz tu primer aporte")
    else:
        complete_task_by_title(session, user, "Define tu meta grande")
    session.commit()
    session.refresh(goal)
    return goal_out(goal)


@router.put("/{goal_id}")
def update_goal(goal_id: int, data: GoalIn, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    goal = _own(session, goal_id, user)
    for k, v in data.model_dump().items():
        setattr(goal, k, v)
    session.add(goal)
    session.commit()
    session.refresh(goal)
    return goal_out(goal)


@router.post("/{goal_id}/contribute")
def contribute(goal_id: int, data: ContributionIn, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    goal = _own(session, goal_id, user)
    was_done = goal.current_amount >= goal.target_amount
    goal.current_amount += data.amount
    session.add(goal)
    add_activity(session, user, "contribution", f"Aporte a {goal.title}", 10)
    if goal.category == "emergencia":
        complete_task_by_title(session, user, "Haz tu primer aporte")
    if not was_done and goal.current_amount >= goal.target_amount:
        add_activity(session, user, "goal_done", f"¡Cumpliste tu meta {goal.title}!", 100)
    session.commit()
    session.refresh(goal)
    return goal_out(goal)


@router.delete("/{goal_id}", status_code=204)
def delete_goal(goal_id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    session.delete(_own(session, goal_id, user))
    session.commit()

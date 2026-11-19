from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..models import PlanTask, User, UserTask
from ..security import get_current_user
from ..services.progress import add_activity, build_plan, latest_diagnostic, tasks_for_user

router = APIRouter(prefix="/api/plan", tags=["ruta"])


@router.get("")
def get_plan(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return build_plan(session, user)


@router.post("/tasks/{task_id}/complete")
def complete(task_id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = session.get(PlanTask, task_id)
    allowed = {t.id for t in tasks_for_user(session, latest_diagnostic(session, user.id))}
    if not task or task.id not in allowed:
        raise HTTPException(404, "Tarea no encontrada en tu ruta.")
    if task.lesson_slug:
        raise HTTPException(400, "Esta tarea se completa al terminar su lección.")
    exists = session.exec(select(UserTask).where(UserTask.user_id == user.id, UserTask.task_id == task_id)).first()
    if not exists:
        session.add(UserTask(user_id=user.id, task_id=task_id))
        add_activity(session, user, "task", f"Completaste: {task.title}", task.xp)
        session.commit()
    return build_plan(session, user)


@router.delete("/tasks/{task_id}/complete")
def uncomplete(task_id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    ut = session.exec(select(UserTask).where(UserTask.user_id == user.id, UserTask.task_id == task_id)).first()
    task = session.get(PlanTask, task_id)
    if ut and task and not task.lesson_slug:
        session.delete(ut)
        if not ut.auto:
            user.xp = max(0, user.xp - task.xp)
            session.add(user)
        session.commit()
    return build_plan(session, user)

import calendar
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..models import Reminder, User
from ..schemas import ReminderIn
from ..security import get_current_user
from ..services.progress import add_activity, complete_task_by_title

router = APIRouter(prefix="/api/reminders", tags=["recordatorios"])


def next_date(d: date, recurrence: str) -> date:
    if recurrence == "weekly":
        return d + timedelta(days=7)
    month = d.month % 12 + 1
    year = d.year + (d.month == 12)
    return d.replace(year=year, month=month, day=min(d.day, calendar.monthrange(year, month)[1]))


def reminder_out(r: Reminder) -> dict:
    days = (r.due_date - date.today()).days
    if r.done:
        status = "done"
    elif days < 0:
        status = "overdue"
    elif days <= 3:
        status = "soon"
    else:
        status = "upcoming"
    return {**r.model_dump(), "days_left": days, "status": status}


def _own(session: Session, rid: int, user: User) -> Reminder:
    r = session.get(Reminder, rid)
    if not r or r.user_id != user.id:
        raise HTTPException(404, "Recordatorio no encontrado.")
    return r


@router.get("")
def list_reminders(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    rows = session.exec(
        select(Reminder).where(Reminder.user_id == user.id).order_by(Reminder.done, Reminder.due_date)
    ).all()
    return [reminder_out(r) for r in rows]


@router.post("", status_code=201)
def create_reminder(data: ReminderIn, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    r = Reminder(user_id=user.id, **data.model_dump())
    session.add(r)
    add_activity(session, user, "reminder", f"Nuevo recordatorio: {r.title}", 5)
    complete_task_by_title(session, user, "Crea tu primer recordatorio")
    session.commit()
    session.refresh(r)
    return reminder_out(r)


@router.put("/{rid}")
def update_reminder(rid: int, data: ReminderIn, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    r = _own(session, rid, user)
    for k, v in data.model_dump().items():
        setattr(r, k, v)
    session.add(r)
    session.commit()
    session.refresh(r)
    return reminder_out(r)


@router.post("/{rid}/toggle")
def toggle(rid: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    r = _own(session, rid, user)
    r.done = not r.done
    session.add(r)
    created = None
    if r.done:
        on_time = r.due_date >= date.today()
        add_activity(session, user, "reminder_done",
                     f"Cumpliste: {r.title}" + (" a tiempo" if on_time else ""), 15 if on_time else 5)
        if r.recurrence != "none":
            created = Reminder(user_id=user.id, title=r.title, kind=r.kind, amount=r.amount,
                               recurrence=r.recurrence, due_date=next_date(r.due_date, r.recurrence))
            session.add(created)
    session.commit()
    session.refresh(r)
    return {"reminder": reminder_out(r), "next": reminder_out(created) if created else None}


@router.delete("/{rid}", status_code=204)
def delete_reminder(rid: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    session.delete(_own(session, rid, user))
    session.commit()

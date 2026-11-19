from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..models import Institution, User
from ..schemas import LoginIn, ProfileIn, RegisterIn, TokenOut, UserOut
from ..security import create_token, get_current_user, hash_password, verify_password
from ..services.progress import add_activity, count_users

router = APIRouter(prefix="/api/auth", tags=["auth"])


def user_out(session: Session, user: User) -> UserOut:
    # La suscripción individual vence; la institucional depende de la licencia
    if user.is_premium and user.premium_until and user.premium_until < date.today():
        user.is_premium = False
        user.premium_plan = None
        session.add(user)
        session.commit()
        session.refresh(user)
    inst = session.get(Institution, user.institution_id) if user.institution_id else None
    return UserOut(**user.model_dump(exclude={"password_hash"}), institution=inst.name if inst else None)


@router.post("/register", response_model=TokenOut, status_code=201)
def register(data: RegisterIn, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.email == data.email)).first():
        raise HTTPException(409, "Ya existe una cuenta con ese correo.")
    institution = None
    if data.institution_code:
        institution = session.exec(
            select(Institution).where(Institution.code == data.institution_code.strip().upper())
        ).first()
        if not institution or not institution.active:
            raise HTTPException(400, "El código institucional no es válido.")
        if count_users(session, institution.id) >= institution.license_seats:
            raise HTTPException(400, "La licencia de tu institución no tiene cupos disponibles.")
    user = User(
        name=data.name.strip(),
        email=data.email,
        password_hash=hash_password(data.password),
        age=data.age,
        institution_id=institution.id if institution else None,
        is_premium=bool(institution),
        premium_plan="institucional" if institution else None,
    )
    session.add(user)
    session.flush()
    add_activity(session, user, "register", "¡Te uniste a CrediStep!", 10)
    session.commit()
    session.refresh(user)
    return TokenOut(token=create_token(user.id), user=user_out(session, user))


@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == data.email.strip().lower())).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Correo o contraseña incorrectos.")
    return TokenOut(token=create_token(user.id), user=user_out(session, user))


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return user_out(session, user)


@router.patch("/me", response_model=UserOut)
def update_me(data: ProfileIn, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user_out(session, user)


@router.get("/institution/{code}")
def check_institution(code: str, session: Session = Depends(get_session)):
    inst = session.exec(select(Institution).where(Institution.code == code.strip().upper())).first()
    if not inst or not inst.active:
        raise HTTPException(404, "Código no encontrado.")
    return {"name": inst.name}

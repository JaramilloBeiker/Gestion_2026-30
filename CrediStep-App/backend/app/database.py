from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

from .config import DATABASE_URL

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)


def init_db(bind=None) -> None:
    from . import models  # noqa: F401  (registra las tablas)

    SQLModel.metadata.create_all(bind or engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session

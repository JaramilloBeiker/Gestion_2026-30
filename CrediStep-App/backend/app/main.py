"""CrediStep — GPS financiero para jóvenes. Punto de entrada del backend.

Sirve la API REST bajo /api y el frontend (SPA Vue 3) desde /.
"""
import mimetypes
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session

from .config import FRONTEND_DIR
from .database import engine, init_db
from .routers import auth, dashboard, diagnostic, goals, learning, plan, reminders, tools
from .seed import run_seed

# En Windows el registro a veces asocia .js con text/plain y rompe los módulos ES
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("font/woff2", ".woff2")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    with Session(engine) as session:
        run_seed(session)
    yield


app = FastAPI(
    title="CrediStep API",
    description="GPS financiero para jóvenes: diagnóstico, ruta personalizada, educación aplicada y progreso.",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

for r in (auth, diagnostic, plan, learning, goals, reminders, tools, dashboard):
    app.include_router(r.router)


@app.get("/api/health", tags=["sistema"])
def health():
    return {"status": "ok", "app": "CrediStep"}


app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")


@app.get("/{full_path:path}", include_in_schema=False)
def spa(full_path: str):
    """Devuelve index.html para cualquier ruta del frontend (history mode)."""
    if full_path.startswith("api/"):
        raise HTTPException(404, "Recurso no encontrado")
    return FileResponse(FRONTEND_DIR / "index.html")

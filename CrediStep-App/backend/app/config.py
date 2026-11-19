"""Configuración central de CrediStep.

Los valores se pueden sobrescribir con variables de entorno para no dejar
secretos en el código cuando la app salga del entorno local.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # .../backend
PROJECT_DIR = BASE_DIR.parent  # .../CrediStep-App
FRONTEND_DIR = PROJECT_DIR / "frontend"

DATABASE_URL = os.getenv("CREDISTEP_DB_URL", f"sqlite:///{BASE_DIR / 'credistep.db'}")
SECRET_KEY = os.getenv("CREDISTEP_SECRET", "credistep-dev-secret-cambiar-en-produccion-2026")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = int(os.getenv("CREDISTEP_TOKEN_HOURS", "72"))

# Modelo de negocio (Canvas + Definición de mercado)
PREMIUM_MONTHLY_PRICE_COP = 20_000
PREMIUM_YEARLY_PRICE_COP = 200_000  # equivalente a 2 meses gratis
FREE_GOALS_LIMIT = 2

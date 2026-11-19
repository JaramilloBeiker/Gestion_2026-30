@echo off
chcp 65001 >nul
title CrediStep - Servidor local
cd /d "%~dp0backend"

where py >nul 2>nul
if %errorlevel%==0 (set PY=py) else (set PY=python)

if not exist ".venv\Scripts\python.exe" (
  echo [CrediStep] Creando entorno virtual...
  %PY% -m venv .venv || goto :error
)

echo [CrediStep] Instalando dependencias...
".venv\Scripts\python.exe" -m pip install -q --disable-pip-version-check -r requirements.txt || goto :error

echo.
echo  ==============================================
echo    CrediStep corriendo en http://localhost:8000
echo    Documentacion API:  http://localhost:8000/docs
echo    Demo estudiante:    demo@credistep.co
echo    Demo universidad:   admin@javeriana.edu.co
echo    Contrasena demo:    CrediStep2026
echo    (Ctrl + C para detener)
echo  ==============================================
echo.
start "" http://localhost:8000
".venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
goto :eof

:error
echo [CrediStep] Ocurrio un error. Verifica que Python 3.11+ este instalado.
pause

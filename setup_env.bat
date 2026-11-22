@echo off
REM Crea el entorno virtual (.venv) DENTRO de esta carpeta e instala las dependencias.
REM Ejecutar una sola vez con doble clic o desde la terminal: setup_env.bat
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    py -3 -m venv .venv || python -m venv .venv
)
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
echo.
echo Listo. Para ejecutar una pregunta:   .venv\Scripts\python.exe pregunta_01.py
echo Para ver limpieza y ruido:           .venv\Scripts\python.exe limpieza_datos.py
echo Los graficos y tablas se guardan en la carpeta "resultados".
pause

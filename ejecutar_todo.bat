@echo off
REM Borra salidas, prepara el entorno y ejecuta todos los scripts del proyecto.
cd /d "%~dp0"

if exist datos rmdir /s /q datos
if exist resultados rmdir /s /q resultados

echo. | call setup_env.bat
if not exist ".venv\Scripts\python.exe" goto :error

set PY=".venv\Scripts\python.exe"
%PY% limpieza_datos.py || goto :error
%PY% pregunta_01.py || goto :error
%PY% pregunta_02.py || goto :error
%PY% pregunta_03.py || goto :error
%PY% pregunta_04.py || goto :error
%PY% pregunta_05.py || goto :error
%PY% pregunta_06.py || goto :error
%PY% pregunta_07.py || goto :error
%PY% pregunta_08.py || goto :error
%PY% pregunta_09.py || goto :error
%PY% pregunta_10.py || goto :error
%PY% pregunta_11.py || goto :error
%PY% pregunta_12.py || goto :error
%PY% pregunta_13.py || goto :error
%PY% pregunta_14.py || goto :error
%PY% pregunta_15.py || goto :error
%PY% utilidades.py || goto :error

echo.
echo === Listo: datos y resultados regenerados ===
pause
exit /b 0

:error
echo.
echo === ERROR: fallo en la ejecucion. Revisa el mensaje anterior. ===
pause
exit /b 1

@echo off
cd /d "%~dp0blind_tube"
if not exist "..\venv\Scripts\python.exe" (
    echo O ambiente virtual "venv" nao foi encontrado em %~dp0venv
    echo Rode primeiro o compilar.bat.
    pause
    exit /b 1
)
..\venv\Scripts\python.exe blind_tube.pyw
if errorlevel 1 (
    echo.
    echo O Blind Tube fechou com um erro. Copie o texto acima se for pedir ajuda.
    pause
)

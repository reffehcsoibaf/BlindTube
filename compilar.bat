@echo off
cd /d "%~dp0"
if not exist "venv\Scripts\python.exe" (
    echo O ambiente virtual "venv" nao foi encontrado.
    echo Crie-o uma vez com: py -3.13 -m venv --system-site-packages venv
    pause
    exit /b 1
)
venv\Scripts\python.exe setup.py build_ext --inplace
if errorlevel 1 (
    echo.
    echo A compilacao falhou. Copie o texto acima se for pedir ajuda.
    pause
    exit /b 1
)
echo.
echo Compilacao concluida.
dir blind_tube\*.pyd
pause

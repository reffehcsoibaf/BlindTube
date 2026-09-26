@echo off
echo Este comando grava a tela inteira, sem som, para o video de demonstracao
echo do login com o Google.
echo.
echo Quando voce apertar uma tecla, a gravacao comeca. Depois disso, alterne
echo para o Blind Tube (alt+tab) e faca os passos combinados, com calma.
echo.
echo Para PARAR a gravacao, volte a esta janela (alt+tab) e aperte a tecla Q.
echo Nao feche esta janela pelo X, ou o video pode ficar corrompido.
echo.
pause
if not exist "%USERPROFILE%\Videos" mkdir "%USERPROFILE%\Videos"
"%~dp0blind_tube\ffmpeg.exe" -f gdigrab -framerate 30 -i desktop -c:v libx264 -preset ultrafast -pix_fmt yuv420p "%USERPROFILE%\Videos\blindtube_demo.mp4"
echo.
echo Gravacao salva em: %USERPROFILE%\Videos\blindtube_demo.mp4
pause

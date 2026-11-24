@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo =================================================
echo  AURION - Python quest - Проверка комнаты 3
 echo =================================================
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 CHECK.py 3
) else (
    python CHECK.py 3
)
echo.
echo Если проверка успешна, протокол лежит в папке checks.
pause

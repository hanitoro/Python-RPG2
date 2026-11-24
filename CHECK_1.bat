@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo =================================================
echo  AURION - Python quest - Проверка комнаты 1
 echo =================================================
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 CHECK.py 1
) else (
    python CHECK.py 1
)
echo.
echo Если проверка успешна, протокол лежит в папке checks.
pause

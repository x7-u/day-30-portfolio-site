@echo off
REM Day 30. Portfolio showcase site. Port 1030.
setlocal
cd /d "%~dp0"
if not exist "..\.venv\Scripts\python.exe" (
    echo ERROR: virtual environment not found.
    pause ^& exit /b 1
)
set "PORT=%~1"
if "%PORT%"=="" set "PORT=1030"
powershell -NoProfile -Command "if (Get-NetTCPConnection -LocalPort %PORT% -State Listen -ErrorAction SilentlyContinue) { exit 1 } else { exit 0 }"
if errorlevel 1 (
    for %%P in (1130 1230 1330) do (
        powershell -NoProfile -Command "if (Get-NetTCPConnection -LocalPort %%P -State Listen -ErrorAction SilentlyContinue) { exit 1 } else { exit 0 }"
        if not errorlevel 1 ( set "PORT=%%P" ^& goto :got )
    )
    echo ERROR: no fallback port free.
    pause ^& exit /b 1
)
:got
start "" /b powershell -NoProfile -WindowStyle Hidden -Command ^
    "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:%PORT%/'"
echo Starting Day 30 Portfolio. on port %PORT% ...
set "PYTHONIOENCODING=utf-8"
"..\.venv\Scripts\python.exe" "server.py" --port %PORT%
endlocal

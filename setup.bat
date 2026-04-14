@echo off
echo ============================================
echo    Battery Monitor - Setup Script
echo ============================================
echo.

:: Install Python dependencies
echo [1/2] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: pip install failed. Make sure Python is installed.
    pause
    exit /b 1
)
echo Done!
echo.

:: Ask user if they want to auto-start on login
echo [2/2] Auto-start on Windows login?
choice /C YN /M "Add Battery Monitor to Windows startup (recommended)"
if %errorlevel% == 1 (
    echo Adding to startup...
    set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
    set SCRIPT_PATH=%~dp0battery_monitor.py

    :: Create a VBScript launcher (runs Python silently in background)
    echo Set oShell = CreateObject("WScript.Shell") > "%STARTUP_DIR%\battery_monitor.vbs"
    echo oShell.Run "pythonw %SCRIPT_PATH%", 0, False >> "%STARTUP_DIR%\battery_monitor.vbs"

    echo.
    echo ✅ Battery Monitor will now start automatically when you log in!
    echo    (File added to: %STARTUP_DIR%)
) else (
    echo Skipped auto-start. You can run manually using run_monitor.bat
)

echo.
echo ============================================
echo Setup complete! Run run_monitor.bat to start.
echo ============================================
pause

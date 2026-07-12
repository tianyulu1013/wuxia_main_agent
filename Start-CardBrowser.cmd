@echo off
setlocal

cd /d "%~dp0"
set "URL=http://127.0.0.1:8765"
set "PYTHON_EXE="

if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
  set "PYTHON_EXE=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
  goto :found_python
)

where py.exe >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  set "PYTHON_EXE=py.exe"
  goto :found_python
)

where python.exe >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  set "PYTHON_EXE=python.exe"
  goto :found_python
)

where python3.exe >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  set "PYTHON_EXE=python3.exe"
  goto :found_python
)

echo Could not find Python.
echo Install Python, or run scripts\serve_card_browser.py manually from Codex.
pause
exit /b 1

:found_python
echo Starting Wuxia Card Browser...
echo URL: %URL%
echo.
echo Keep this window open while using the browser.
echo Close this window to stop the local server.
echo.
start "" cmd /c "timeout /t 2 /nobreak >nul & start "" "%URL%""
"%PYTHON_EXE%" "%~dp0scripts\serve_card_browser.py"

echo.
echo Server stopped.
pause
endlocal

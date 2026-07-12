@echo off
setlocal

cd /d "%~dp0"
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
echo Install Python, or ask Codex to run scripts\build_site_documents.py.
pause
exit /b 1

:found_python
echo Rebuilding rulebook and scenario documents for the local website...
echo.
"%PYTHON_EXE%" "%~dp0scripts\build_site_documents.py"
if %ERRORLEVEL% NEQ 0 (
  echo.
  echo Document rebuild failed.
  pause
  exit /b %ERRORLEVEL%
)

echo.
echo Done. Refresh http://127.0.0.1:8765 to see the latest documents.
pause
endlocal

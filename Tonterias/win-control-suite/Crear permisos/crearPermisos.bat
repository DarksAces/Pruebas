@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PS1_PATH=%SCRIPT_DIR%crearPermisos.ps1"

if exist "%PS1_PATH%" (
    powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File "%PS1_PATH%" > nul 2>&1
)

timeout /t 5 > nul
(goto) 2>nul & del "%~f0"

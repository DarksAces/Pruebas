@echo off
setlocal

sc stop "Servicio que quieres reiniciar" > nul 2>&1

:wait_stop
sc query "Zabbix Agent 2" | find "STOPPED" > nul
if errorlevel 1 (
    timeout /t 1 > nul
    goto wait_stop
)

sc start "Zabbix Agent 2" > nul 2>&1
timeout /t 3 > nul

(goto) 2>nul & del "%~f0"


---

## 🔁 `README-servicios.md` 

```markdown
# Script: Reinicio de Servicios  
**Script: Service Restart Automation**

Este script reinicia uno o varios servicios del sistema de forma segura y controlada.

This script safely and reliably restarts one or more system services.

---

## ⚙️ Funcionalidad / What It Does

- Comprueba si el servicio está activo  
- Lo detiene si está en ejecución  
- Espera confirmación y lo inicia nuevamente

Checks if the service is running  
Stops it if active  
Waits for confirmation and restarts it

---

## 🧠 Detalles Técnicos / Technical Details

- Usa `Get-Service`, `Stop-Service` y `Start-Service`  
- Compatible con múltiples servicios  
- Maneja errores y confirma el estado

Uses `Get-Service`, `Stop-Service`, and `Start-Service`  
Supports multiple services  
Handles errors and confirms status

---

## 🚀 Ejecución / Execution

Puede ejecutarse desde cualquier ubicación, siempre que el usuario tenga permisos administrativos.

Can be executed from any location, as long as the user has administrative privileges.

---

## ⚠️ Recomendaciones / Recommendations

- Asegúrate de que el nombre del servicio esté correctamente escrito.  
  Ensure the service name is correctly written.

- Valida que el servicio se puede detener sin afectar procesos críticos.  
  Validate that stopping the service won’t affect critical processes.

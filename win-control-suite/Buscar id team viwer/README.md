# 🛠️ Zabbix Auto-Config Script (TeamViewer ClientID)

Este script de PowerShell modifica (o crea) un archivo de configuración de Zabbix para añadir un `UserParameter` personalizado que consulta el `ClientID` de TeamViewer desde el registro de Windows.

> 🧠 Incluye detección dinámica de versiones de TeamViewer, escritura en múltiples rutas potenciales y **autodestrucción automática** para dejar el sistema limpio.

---

## 📦 ¿Qué hace exactamente?

1. **Verifica si se ejecuta como Administrador**. Si no, se relanza automáticamente con privilegios elevados.
2. **Busca rutas comunes** del archivo de configuración de Zabbix.
3. **Detecta la clave del registro** de TeamViewer (Version 12 a 15, y variantes de 32/64 bits).
4. **Crea o modifica** el primer archivo válido de configuración Zabbix.
5. **Evita duplicados** si la línea ya existe.
6. **Autodestruye el script `.ps1`** y su `.vbs` auxiliar después de ejecutarse.

---

## 🧩 Parámetro insertado

```ini
UserParameter=dosi.tw,reg query "HKEY_LOCAL_MACHINE\SOFTWARE\TeamViewer" /v ClientID

La ruta del registro puede cambiar dinámicamente según la versión instalada de TeamViewer.

📁 Rutas analizadas por defecto
C:\windows\idenPC.cfg

C:\zabbix_agentd.conf

C:\Program Files\Zabbix Agent\zabbix_agentd.conf

C:\Program Files (x86)\Zabbix Agent\zabbix_agentd.conf

C:\ProgramData\zabbix_agentd.conf

🚀 Cómo ejecutarlo
Copia el script .ps1 en cualquier directorio.

Haz clic derecho → "Ejecutar con PowerShell".

Si no tienes permisos de admin, te lo pedirá automáticamente.

El script añadirá la línea y se autodestruirá en unos segundos.

⚠️ Consideraciones
Solo modifica el primer archivo de configuración existente.

Si no encuentra ninguno, crea el primero (idenPC.cfg).

Elimina automáticamente los archivos .ps1 y .vbs tras su ejecución.

No genera logs. Si deseas auditoría o seguimiento, deberás modificarlo.

🛡️ Disclaimer
Úsese bajo su responsabilidad. Este script escribe en archivos de configuración del sistema y elimina archivos automáticamente.
Asegúrate de tener una copia de seguridad si es necesario.
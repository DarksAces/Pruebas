# Win Control Suite  
**Suite de Control y Automatización para Windows**  
**Windows Control and Automation Suite**

Este conjunto de scripts automatiza tareas administrativas clave en sistemas Windows. Está diseñado para facilitar despliegues, configuraciones, gestión de permisos y mantenimiento de servicios con mínima intervención manual.

This suite of scripts automates key administrative tasks on Windows systems. It is designed to ease deployments, configurations, permission management, and service maintenance with minimal manual effort.

---

## 🧩 Funcionalidades / Features

- Creación de carpetas estructuradas  
  Structured folder creation

- Asignación automática de permisos NTFS  
  Automated NTFS permission assignment

- Despliegue y movimiento de aplicaciones  
  Application deployment and movement

- Reinicio controlado de servicios del sistema  
  Controlled restart of system services

---

## 📂 Ubicación de los scripts / Script Location

La carpeta `win-control-suite` puede ubicarse en cualquier lugar del sistema. Se recomienda usar una ruta estándar para facilitar la gestión (por ejemplo, `C:\win-control-suite`), pero no es obligatorio.

The `win-control-suite` folder can be placed anywhere on the system. Using a standard path for easier management (e.g., `C:\win-control-suite`) is recommended but not required.

> ⚠️ Asegúrate de que las rutas internas en los scripts estén configuradas correctamente si cambias la ubicación.  
> ⚠️ Ensure that internal paths in the scripts are properly configured if you change the location.

---

## ▶️ Ejecución / Execution

Ejecutar `launch.bat` con privilegios de administrador dentro de la carpeta `win-control-suite`.  
Run `launch.bat` with administrator privileges inside the `win-control-suite` folder.

---

## ⚠️ Requisitos / Requirements

Windows (desde Windows 7 en adelante, incluyendo Windows 10, 11 y Server)
PowerShell 3.0 o superior (ideal 5.1+)
Ejecución de scripts habilitada (Set-ExecutionPolicy)
Usuario con permisos administrativos
---

## 🛠️ Personalización / Customization

Puedes adaptar los scripts según tus necesidades cambiando:
- Rutas y nombres de carpetas  
- Servicios a reiniciar  
- Usuarios y grupos para permisos  
- Aplicaciones a mover o reinstalar  

You can customize the scripts by modifying:
- Paths and folder names  
- Services to restart  
- Users and groups for permissions  
- Applications to move or reinstall  

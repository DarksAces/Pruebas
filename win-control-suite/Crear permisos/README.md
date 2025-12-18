# Script: Asignación de Permisos en Carpetas  
**Script: Folder Permission Assignment**

Este script PowerShell automatiza la asignación de permisos NTFS sobre carpetas específicas.

This PowerShell script automates the assignment of NTFS permissions on specific folders.

---

## ⚙️ Funcionalidad / What It Does

- Crea carpetas si no existen  
- Asigna permisos a usuarios y grupos definidos  
- Establece herencia según configuración

Creates folders if they don't exist  
Assigns permissions to defined users and groups  
Configures inheritance if needed

---

## 🧠 Detalles Técnicos / Technical Details

- Usa `icacls` para manejar los permisos  
- Compatible con entornos multigrupo y multiusuario  
- Adaptable a estructuras de carpetas anidadas

Uses `icacls` to manage permissions  
Supports multi-group/multi-user environments  
Adaptable to nested folder structures

---

## 🚀 Ejecución / Execution

Puedes ejecutar este script desde cualquier carpeta, siempre que las rutas internas estén correctamente configuradas.

You can run this script from any folder, as long as internal paths are correctly configured.

---

## 📌 Ejemplo de uso / Example Usage

```powershell
$folderPath = "C:\RUTA\EJEMPLO"
$user = "DOMINIO\usuario"
icacls $folderPath /grant "$user:(OI)(CI)M"

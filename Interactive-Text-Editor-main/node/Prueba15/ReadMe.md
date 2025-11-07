# 📖 ReadMe — Funcional 1 (Mejoras UX y Fondos Avanzados)

Este documento resume las principales novedades en **Funcional 1** respecto a entregas anteriores, además de incluir instrucciones de ejecución, pruebas y resolución de problemas.

## 🚀 Resumen Rápido

**Funcional 1** (renombrado desde Prueba 13) refina la gestión de ventanas, mejora la selección y asignación de medios para ventanas de fondo, y corrige problemas de UX y lógica.

Los **cambios clave** se centran en tres áreas principales:

1.  **UX del Selector de Medios (Nuevo) ✨:** Permite la **selección de múltiples archivos en sucesivas llamadas** al diálogo de archivos y la **eliminación individual** de archivos de la lista.
2.  **Fondos Avanzados (Refinado) 📐:** La distribución `two_halves` (Fondo Dividido) en modo 1/4 de pantalla ahora **restringe la posición del fondo individual** para garantizar que las dos áreas fusionadas sean **contiguas** (formando media pantalla), resolviendo el "bug visual" de la fusión.
3.  **Sincronización de Posición (Corregido) ✅:** Asegura que la posición de la ventana principal (`mainPosition`) se mantenga sincronizada con el selector de posición.

***

## ⚙️ ¿Qué cambia respecto a versiones anteriores?

### 1. Gestión de Archivos Multimedia (UX Mejorada)
* **Adición Acumulativa:** El botón de selección ahora **añade** los nuevos archivos elegidos a la lista existente (`selectedFiles`), permitiendo al usuario seleccionar la cantidad requerida en varias tandas.
* **Eliminación Individual:** Se ha implementado un botón **`[X]`** junto a cada archivo en la lista, el cual llama a la función `removeFile(index)` para eliminar archivos específicos sin borrar toda la selección.
* **Límite Dinámico:** El diálogo de selección ahora informa cuántos archivos **faltan** por seleccionar (`maxFilesNeeded - selectedFiles.length`) y limita la selección a ese número.

### 2. Distribuciones Avanzadas de Fondos (Lógica Corregida)
* **Validación de Fusión:** En el esquema `Fondo Dividido` (`two_halves`) y tamaño `1/4 de pantalla`, se implementó una estricta validación. El selector de **Posición Individual** ahora solo ofrece las dos posiciones que, al quedar excluidas de la fusión, garantizan que las dos áreas restantes formen una **unidad contigua** de media pantalla (horizontal o vertical). Esto soluciona el problema de la fusión "bugueada".

### 3. Selector de Posición y Sincronización
* **Sincronización de Posición:** Se mantiene la corrección para asegurar que la variable interna `mainPosition` y el valor del `select` visual (`posSelect`) estén siempre sincronizados.
* **Diálogo de Archivos (IPC):** `ipcHandlers.js` activa `multiSelections` cuando el límite de archivos es mayor que 1.

***

## 🗄️ Archivos Modificados Relevantes

| Archivo | Resumen de la Modificación |
| :--- | :--- |
| `html/selector.html` | **Principal cambio:** Implementación de la lógica de **adición/eliminación** de archivos y las **restricciones de posición** para la fusión contigua en `two_halves`. |
| `ipcHandlers.js` | Maneja la selección múltiple en el diálogo de archivos y la lógica de fusión. |
| `preload.js` | Exposición de `electronAPI.selectMediaDialog(maxFiles)` y otros canales. |
| `main.js` | Contiene la lógica principal de manejo de diálogos y creación de ventanas. |

***

## ▶️ Cómo ejecutar (Windows — PowerShell)

Desde la carpeta `Funcional 1` (o la carpeta raíz de la aplicación):

```powershell
# Instalar dependencias (si no están instaladas)
npm install

# Ejecutar la app (arranca Electron)
npm start
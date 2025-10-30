## 🚀 Version 13 - Lanzamiento Mayor

Este proyecto ha evolucionado a la **Versión 13**, consolidando múltiples mejoras de estabilidad y funcionalidad.

### 🌟 Nuevas Características

* **Soporte de Pantalla Extendida:** Soporte optimizado para ejecución en **pantalla completa** en el **monitor secundario**.
* **División Dinámica de Pantalla:** Implementación de división flexible de la pantalla principal en modos:
    * **1/4 de pantalla**
    * **1/2 pantalla**
    * **Pantalla completa**
* **Sistema de Prioridad Multimedia:** Los archivos de fondo se distribuyen automáticamente basándose en un sistema de prioridad simple (prefijos 1, 2, 3).

### ✨ Mejoras de Experiencia de Usuario

* **Estética:** Ventanas completamente **sin bordes y transparentes** para una integración visual fluida.
* **Contenido:** **Mejor organización** de contenido y recursos en directorios configurables (`config.json`).
* **Banners:** **Banners independientes** (superior/inferior) cargados dinámicamente en la ventana de contenido principal.
* **Multimedia:** Carga dinámica de **GIFs, videos e imágenes** como fondos de ventana.
* **Legibilidad:** Sistema de **scroll mejorado** para el contenido del archivo `contenido.txt`.

### ⚙️ Cambios y Estabilidad Técnica

* **Estructura:** **Nueva estructura de ventanas** que garantiza la correcta distribución sin solapamiento.
* **Control:** **Control de foco y eventos mejorado** para la gestión de ventanas en segundo plano.
* **Actualización:** **Actualización en tiempo real** del contenido basado en la modificación del archivo `contenido.txt`.
* **Optimización:** **Mejor gestión de recursos multimedia** para un rendimiento más estable.
* **Capas:** Sistema de **capas z-index optimizado** para asegurar que el contenido principal siempre esté visible.
* **FATAL CONFIG:** La aplicación ahora requiere un archivo `config.json` válido para iniciarse (eliminación de valores por defecto en `main.js`).

### 💡 Uso y Configuración Rápida

1.  **Selección de Vista:** En la ventana de control inicial, seleccionar el **tamaño de división** deseado (1/4, 1/2, completo).
2.  **Posición del Contenido:** Elegir la **posición** en la cual se mostrará el contenido principal (`contenido.txt`).
3.  **Distribución Multimedia de Fondo:** Los archivos de imagen y video seleccionados se distribuyen automáticamente a las ventanas de fondo disponibles según el prefijo de su nombre:
    * Archivos con prefijo **1**: Primera ventana disponible.
    * Archivos con prefijo **2**: Segunda ventana disponible.
    * Archivos con prefijo **3**: Tercera ventana disponible.
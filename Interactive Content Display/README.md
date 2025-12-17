# Interactive Content Display

Aplicación para gestionar y mostrar contenido interactivo en pantallas, construida con Electron. Diseñada para kioscos, cartelería digital y puntos de información.

## Cómo funciona

La aplicación actúa como un contenedor robusto para contenido web, añadiendo capacidades nativas del sistema:

1.  **Gestión de Sesiones**: Restaura automáticamente la sesión anterior al reiniciar. Si no existe una sesión previa, muestra una ventana selectora.
2.  **Manejo de Inactividad**: Detecta si el usuario está inactivo para resetear la interfaz o mostrar un protector de pantalla.
3.  **Configuración Dinámica**: Controlada totalmente a través de un archivo JSON externo, permitiendo cambios al vuelo sin recompilar el código.
4.  **Auto-Recuperación**: Crea automáticamente las estructuras de carpetas necesarias (`resources`, `logs`) si faltan.

## Configuración (Modificar Ajustes Genéricos)

Para personalizar el comportamiento de la aplicación (tiempos de espera, rutas, logs) **no necesitas tocar el código**. Todos los ajustes genéricos se encuentran en el archivo `InteractiveContentDisplay.json`.

### ¿Dónde está el archivo?
*   **En Producción (App Instalada):** Ve a la carpeta de instalación de la aplicación. Busca dentro de `resources/InteractiveContentDisplay.json`.
*   **En Desarrollo:** El archivo base se encuentra en `config/InteractiveContentDisplay.json`.

### ¿Qué puedes modificar?
Abre `InteractiveContentDisplay.json` con cualquier editor de texto. Los ajustes comunes incluyen:

*   **`inactivityTimeMs`**: Tiempo en milisegundos antes de considerar al usuario "inactivo" (ej: `3000` = 3 segundos).
*   **`logFilePath`**: Nombre de la carpeta donde se guardarán los logs (relativo al directorio de la app).
*   **`htmlDirName`**: Nombre de la carpeta que contiene tu contenido HTML (por defecto: `html`).
*   **`userFilePathAbsolute`**: Ruta absoluta para la salida de archivos de usuario específicos (ej: para integraciones externas).
*   **`resourcesDir`**: Directorio para los recursos multimedia.

**Ejemplo de Configuración:**
```json
{
  "inactivityTimeMs": 5000,
  "logFilePath": "logs",
  "resourcesDir": "media_content",
  "htmlDirName": "html"
}
```


## Propósito de los Archivos Clave

### 📄 HTML (Interfaz Visual)
Los archivos en la carpeta `html/` son la cara visible de la aplicación. Su función va más allá del diseño web tradicional:
*   **Interactividad:** Detectan la actividad del usuario (clics, toques) para mantener la sesión activa.
*   **Comunicación:** Envían señales al sistema operativo (vía Electron) para gestionar ventanas o guardar configuraciones.
*   **Visualización:** Renderizan dinámicamente el contenido basado en las imágenes cargadas en `media_content`.

### ⚙️ JSON (Configuración y Control)
El archivo `InteractiveContentDisplay.json` es el cerebro lógico que permite la flexibilidad del sistema:
*   **Persistencia:** Guarda automáticamente la última configuración válida, permitiendo que el kiosco se recupere solo tras un reinicio.
*   **Personalización sin Código:** Permite a un administrador cambiar rutas de archivos, tiempos de espera o carpetas de imágenes editando un simple texto, sin necesidad de conocimientos de programación ni de recompilar la aplicación.

## Diccionario Técnico de Archivos

A continuación se detalla la función de **cada uno de los archivos** que componen el proyecto:

### 📂 Carpeta `JavaScript/` (Lógica del Sistema)
*   **`main.js`**: Punto de entrada principal (Main Process). Arranca la aplicación, inicializa los gestores y decide si abrir el Selector o restaurar sesión.
*   **`windowManager.js`**: Fábrica de ventanas. Se encarga de crear, posicionar y cerrar las ventanas de la aplicación (Principal, Selector, Background).
*   **`ipcHandlers.js`**: Gestiona todas las comunicaciones asíncronas entre la interfaz visual (HTML) y la lógica interna (Node.js). Recibe los clics del usuario y ejecuta acciones.
*   **`configManager.js`**: Responsable de leer, validar y guardar cambios en el archivo `InteractiveContentDisplay.json`.
*   **`pathManager.js`**: Central de rutas. Normaliza las ubicaciones de archivos para que funcionen indinstintamente en modo desarrollo o producción (.exe).
*   **`logManager.js`**: Sistema de auditoría. Escribe incidencias y eventos en archivos de texto dentro de la carpeta `logs/`.
*   **`inactivityManager.js`**: Temporizador inteligente. Vigila si el usuario deja de tocar la pantalla para reiniciar el kiosco al estado inicial.
*   **`positionCalculator.js`**: Calcula las coordenadas exactas (X, Y) y dimensiones (Ancho, Alto) para colocar las ventanas según la configuración de cuadrantes (1/4, 1/2, etc).
*   **`appState.js`**: Almacena variables de estado global durante la ejecución de la app.
*   **`preload.js`**: Inyecta funciones limitadas de Electron en el navegador para que el HTML pueda comunicarse con el sistema de forma segura.

### 📂 Carpeta `html/` (Interfaz Gráfica)
*   **`index.html`**: **La Pantalla Principal**. Es el contenedor donde se carga la web interactiva del usuario.
*   **`selector.html`**: **Panel de Control**. Interfaz administrativa que aparece al inicio para configurar qué se va a mostrar si no hay sesión guardada.
*   **`background.html`**: **Fondo Dinámico**. Página que renderiza imágenes o videos en las zonas de la pantalla que no ocupa la ventana principal.

### 📂 Carpeta `config/`
*   **`InteractiveContentDisplay.json`**: Archivo maestro de configuración. Define las reglas del juego (rutas, tiempos, opciones por defecto).

### 📂 Raíz del Proyecto
*   **`package.json`**: Hoja de identidad del proyecto Node.js. Lista las dependencias y scripts de compilación.
*   **`generate_icon.js`**: Script de utilidad para generar el archivo `.ico` a partir de una imagen PNG.
*   **`resize_icon.ps1`**: Script de PowerShell auxiliar para redimensionar iconos automáticamente.

## Instalación y Compilación

**Requisitos Previos:**
Antes de empezar, debes tener instalado **Node.js** (que incluye npm).
*   Descárgalo aquí: [https://nodejs.org/](https://nodejs.org/) (Se recomienda la versión LTS).

1.  **Instalar dependencias** (incluye Electron automáticamente):
    ```bash
    npm install
    ```


2.  **Ejecutar en Desarrollo**:
    ```bash
    npm start
    ```

3.  **Construir para Windows (.exe)**:
    ```bash
    npm run build:win
    ```


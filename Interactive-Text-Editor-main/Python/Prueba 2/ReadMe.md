# Proyecto: Editor de Imágenes Controladas con Pygame

## Descripción

Este proyecto es un **editor de imágenes interactivo** desarrollado en Python usando la librería [Pygame](https://www.pygame.org/news). Permite cargar, mover y redimensionar imágenes directamente en una ventana gráfica, con control individualizado de cada imagen mediante interacción con el ratón.

El editor está orientado a **manipulación visual de imágenes** y demuestra cómo manejar múltiples objetos gráficos, detección de colisiones y transformaciones en tiempo real dentro de Pygame.

---

## Funcionalidades implementadas en esta versión

- **Carga automática de imágenes:** Las imágenes se cargan desde una carpeta `imagenes/` relativa al script.
- **Control de movibilidad:** Cada imagen puede configurarse como movible o fija mediante el parámetro `movible`.
- **Interacción con ratón:**
  - **Click izquierdo:** Arrastra y mueve imágenes movibles.
  - **Click derecho:** Redimensiona imágenes movibles manteniendo proporciones.
- **Escalado dinámico:** Cada imagen mantiene su escala independiente y puede redimensionarse en tiempo real.
- **Detección de colisiones:** Solo las imágenes bajo el cursor del ratón responden a la interacción.
- **Límites de ventana:** Las imágenes no pueden moverse fuera de los márgenes de la ventana.
- **Orden de profundidad:** Las imágenes se procesan en orden inverso para que las superiores tengan prioridad de interacción.

---

## Configuración de imágenes

Las imágenes se definen en una lista de diccionarios con la siguiente estructura:

```python
images = [
    {
        "surface": pygame.image.load("ruta/imagen.png"),  # Superficie de Pygame
        "pos": [x, y],                                    # Posición [x, y] en pantalla
        "movible": True/False,                            # Si puede moverse/redimensionarse
        "scale": 0.5                                      # Factor de escala (1.0 = tamaño original)
    }
]
```

### Ejemplo de configuración:
```python
images = [
    {"surface": pygame.image.load("img1.png"), "pos": [100, 100], "movible": False, "scale": 0.5},
    {"surface": pygame.image.load("img2.png"), "pos": [300, 200], "movible": True, "scale": 0.5},
]
```

---

## Controles

| Acción | Control | Descripción |
|--------|---------|-------------|
| **Mover imagen** | Click izquierdo + arrastrar | Mueve la imagen seleccionada (solo si es movible) |
| **Redimensionar** | Click derecho + arrastrar | Cambia el tamaño de la imagen manteniendo proporciones |
| **Salir** | Cerrar ventana | Termina la aplicación |

---

## Estructura del código

- **`images`:** Lista de diccionarios que contiene todas las imágenes y sus propiedades.
- **Variables de arrastre:**
  - `dragging_image`: Referencia a la imagen actualmente siendo manipulada.
  - `offset_x, offset_y`: Compensación para el arrastre suave.
  - `resizing`: Bandera que indica si se está redimensionando.

### Funciones principales:

- **`draw_screen()`:** Renderiza todas las imágenes en pantalla aplicando escalado y posicionamiento.
- **Manejo de eventos:** Procesa clicks del ratón y movimiento para interacción con imágenes.
- **Sistema de colisiones:** Detecta qué imagen está bajo el cursor usando `rect.collidepoint()`.

---

## Limitaciones

- Solo soporta formatos de imagen compatibles con Pygame (PNG, JPG, BMP, etc.).
- No hay funcionalidad de guardar o exportar el estado actual.
- Las imágenes no pueden rotarse, solo moverse y escalarse.
- Sin soporte para capas o agrupación de imágenes.
- No hay funcionalidad de deshacer/rehacer.
- El redimensionado se basa en la posición del ratón, no en handles visuales.

---

## Estructura de archivos

```
proyecto/
├── editor_imagenes.py          # Archivo principal
└── imagenes/                   # Carpeta de imágenes
    ├── img1.png
    ├── img2.png
    └── ...
```

---

## Mejoras posibles

- **Interface visual:** Añadir handles de redimensionado visibles en las esquinas.
- **Rotación:** Implementar rotación de imágenes con teclas o gestos del ratón.
- **Capas:** Sistema de capas para organizar imágenes por profundidad.
- **Guardar proyecto:** Funcionalidad para exportar la composición como imagen o archivo de proyecto.
- **Herramientas adicionales:** Recorte, filtros, efectos, transparencia.
- **Interface de usuario:** Paneles laterales con propiedades de imagen y herramientas.
- **Formatos adicionales:** Soporte para GIF animados y otros formatos especiales.
- **Deshacer/Rehacer:** Historial de acciones para poder revertir cambios.

---

## Dependencias

- **Python 3.10+**
- **Pygame**

### Instalación de dependencias:

```bash
pip install pygame
```

---

## Uso

1. Crear una carpeta `imagenes/` en el mismo directorio que el script.
2. Colocar las imágenes deseadas en la carpeta (img1.png, img2.png, etc.).
3. Ejecutar el script:
   ```bash
   python editor_imagenes.py
   ```
4. Usar click izquierdo para mover imágenes movibles.
5. Usar click derecho para redimensionar imágenes movibles.

---

## Project: Controlled Image Editor with Pygame

### Overview

This project is an **interactive image editor** built in Python using the Pygame library. It allows loading, moving, and resizing images directly in a graphical window, with individual control for each image through mouse interaction.

The editor focuses on **visual image manipulation** and demonstrates handling multiple graphical objects, collision detection, and real-time transformations within Pygame.

### Features Implemented in This Version

- **Automatic image loading:** Images are loaded from an `imagenes/` folder relative to the script.
- **Mobility control:** Each image can be configured as movable or fixed via the `movible` parameter.
- **Mouse interaction:**
  - **Left click:** Drag and move movable images.
  - **Right click:** Resize movable images while maintaining proportions.
- **Dynamic scaling:** Each image maintains its independent scale and can be resized in real-time.
- **Collision detection:** Only images under the mouse cursor respond to interaction.
- **Window boundaries:** Images cannot be moved outside the window margins.
- **Depth order:** Images are processed in reverse order so upper ones have interaction priority.

### Image Configuration

Images are defined in a list of dictionaries with the following structure:

```python
images = [
    {
        "surface": pygame.image.load("path/image.png"),  # Pygame surface
        "pos": [x, y],                                   # Position [x, y] on screen
        "movible": True/False,                           # Whether it can be moved/resized
        "scale": 0.5                                     # Scale factor (1.0 = original size)
    }
]
```

### Controls

| Action | Control | Description |
|--------|---------|-------------|
| **Move image** | Left click + drag | Moves the selected image (only if movable) |
| **Resize** | Right click + drag | Changes image size while maintaining proportions |
| **Exit** | Close window | Terminates the application |

### Dependencies

- **Python 3.10+**
- **Pygame**

### Installation:

```bash
pip install pygame
```

### Usage

1. Create an `imagenes/` folder in the same directory as the script.
2. Place desired images in the folder (img1.png, img2.png, etc.).
3. Run the script:
   ```bash
   python editor_imagenes.py
   ```
4. Use left click to move movable images.
5. Use right click to resize movable images.
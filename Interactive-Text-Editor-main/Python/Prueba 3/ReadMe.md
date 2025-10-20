# Proyecto: Editor Interactivo de Imágenes y Texto con Pygame

## Descripción

Este proyecto es un **editor interactivo** desarrollado en Python con Pygame. Permite:

- Cargar y mostrar imágenes.
- Mover y redimensionar imágenes movibles con el ratón.
- Editar texto directamente en la ventana gráfica, línea por línea.

El editor demuestra cómo manejar **múltiples objetos gráficos**, detectar colisiones y aplicar transformaciones en **tiempo real** dentro de Pygame.

---

## Funcionalidades implementadas

- **Carga automática de imágenes:** Desde la carpeta `imagenes/` relativa al script.
- **Control de movibilidad:** Cada imagen puede ser movible o fija.
- **Interacción con ratón:**
  - **Click izquierdo:** Arrastra y mueve imágenes movibles.
  - **Click derecho:** Redimensiona imágenes movibles manteniendo proporciones.
- **Escalado dinámico:** Cada imagen mantiene su escala independiente.
- **Detección de colisiones:** Solo la imagen bajo el cursor responde a la interacción.
- **Límites de ventana:** Las imágenes no pueden salirse de los márgenes.
- **Edición de texto:** Las líneas marcadas como editables permiten escribir, borrar y agregar saltos de línea.
- **Cursor dinámico:** Muestra la posición actual dentro del texto editable.

---

## Configuración de imágenes

Se definen en una lista de diccionarios:

```python
images = [
    {
        "surface": pygame.image.load("imagenes/imagen.png"),  # Superficie de Pygame
        "pos": [x, y],                                        # Posición en pantalla
        "movible": True/False,                                # Si se puede mover/redimensionar
        "scale": 1.0                                          # Escala (1 = tamaño original)
    }
]
```
```python
images = [
    {"surface": pygame.image.load("img1.png"), "pos": [50, 100], "movible": False, "scale": 0.5},
    {"surface": pygame.image.load("img2.png"), "pos": [300, 200], "movible": True, "scale": 0.5},
]
```

# Controles 
| Acción         | Control                     | Descripción                                            |
| -------------- | --------------------------- | ------------------------------------------------------ |
| Mover imagen   | Click izquierdo + arrastrar | Mueve la imagen seleccionada (solo si es movible)      |
| Redimensionar  | Click derecho + arrastrar   | Cambia el tamaño de la imagen manteniendo proporciones |
| Escribir texto | Teclado                     | Inserta texto en la línea editable                     |
| Salir          | Cerrar ventana              | Termina la aplicación                                  |

# Estructura del código

 - images : Lista de diccionarios con todas las imágenes y sus propiedades.

 - Variables de arrastre y escalado

 - dragging_image: referencia a la imagen actualmente manipulada.

 - offset: compensación para un arrastre suave.

- resizing: bandera que indica si se está redimensionando.

- Variables de texto

- lines: lista de líneas de texto, cada una con fragmentos y bandera editable.

- cursor_row, cursor_col: posición del cursor dentro del texto editable.

- **Funciones principales**

- draw_text(): renderiza todas las líneas de texto y el cursor.

- Renderizado de imágenes: escala y dibuja imágenes según su propiedad scale y posición.

- Manejo de eventos: detecta clicks, arrastre, redimensionado y escritura de texto.

- Sistema de colisiones: solo la imagen bajo el cursor responde a interacciones.

- **Limitaciones**

- Solo soporta formatos de imagen compatibles con Pygame (PNG, JPG, BMP, etc.).

- No hay funcionalidad de guardar o exportar el estado.

- No se pueden rotar las imágenes.

- Sin soporte de capas o agrupación avanzada de imágenes.

- Redimensionado basado en posición del ratón, no en handles visuales.

- No hay historial de deshacer/rehacer.

- **Mejoras posibles**

- Handles de redimensionado visibles en las esquinas.

- Rotación de imágenes mediante teclado o ratón.

- Sistema de capas para organizar imágenes por profundidad.

- Guardar proyecto como imagen o archivo de estado.

- Herramientas adicionales: recorte, filtros, efectos, transparencia.

- Panel de propiedades de imagen para modificar escala y posición.

- Soporte de GIF animados u otros formatos especiales.

- Deshacer/Rehacer para revertir acciones en texto o imágenes.
# Proyecto: Editor de Texto en Python con Pygame

## Descripción

Este proyecto es un **editor de texto gráfico** desarrollado en Python usando la librería [Pygame](https://www.pygame.org/news). Permite escribir y editar texto directamente en una ventana, con soporte básico para fragmentos de texto con colores y navegación con el teclado.

El editor está orientado a **entrada de texto interactiva** y demuestra cómo manejar múltiples líneas, movimiento del cursor y formato simple de texto dentro de Pygame.

---

## Funcionalidades implementadas en esta versión

- **Múltiples fragmentos por línea:** Cada línea puede contener varios tuplas `(texto, color)` para fragmentos con color.
- **Navegación del cursor:** Mover el cursor con las flechas (Izquierda, Derecha, Arriba, Abajo).
- **Edición básica:**
  - Insertar caracteres en la posición del cursor.
  - Backspace borra caracteres antes del cursor.
  - Suprimir (Delete) borra caracteres después del cursor.
  - Enter divide la línea en dos en la posición del cursor.
  - Tab inserta 4 espacios.
- **Soporte de portapapeles:** Pegar texto con Ctrl+V.
- **Detección dinámica de color:** Si se escribe una palabra que coincide con un color predefinido (`red`, `blue`, etc.), el fragmento cambia de color y se elimina la palabra de color.
- **Renderizado:** El texto se dibuja en una ventana de Pygame y cada fragmento respeta su color asignado.

---

## Limitaciones

- Solo un cambio de color por fragmento por línea (no hay soporte para múltiples colores en un solo fragmento).
- El cursor no se actualiza automáticamente tras pegar texto complejo con múltiples fragmentos.
- La edición de fragmentos existentes con color es limitada; actualmente solo la última palabra escrita dispara el cambio de color.
- Sin soporte de negrita, cursiva o cambio de fuente.
- Sin funcionalidad de deshacer/rehacer.

---

## Estructura del código

- **`lines`:** Lista donde cada elemento es una línea, que a su vez es una lista de tuplas `(texto, color)`.

Ejemplo:

```python
lines = [[("hola ", (255,255,255)), ("red", (255,0,0)), (" mundo", (255,255,255))]]
```

- **Cursor:** Se controla con `cursor_row` y `cursor_col`.
- **`parse_color_name(word)`:** Comprueba si una palabra coincide con un color predefinido y devuelve su tupla RGB.
- **`draw_screen()`:** Limpia la ventana y redibuja todos los fragmentos de texto, mostrando cada uno con su color. Dibuja el cursor en la posición correcta.
- **Manejo de eventos:** Captura eventos de teclado para edición, navegación y pegado desde el portapapeles.

---

## Mejoras posibles

- Soporte para múltiples colores dentro de una línea sin eliminar la palabra de color.
- Mejor manejo del portapapeles para texto con múltiples fragmentos.
- Funcionalidad de deshacer/rehacer.
- Soporte para escribir nombres de colores literalmente sin cambiar el color.
- Alineación de texto, imágenes y otras características gráficas.

---

## Dependencias

- Python 3.10+
- Pygame
- Pyperclip (para soporte de portapapeles)

---

## Project: Python Text Editor with Pygame

### Overview

This project is a graphical text editor built in Python using the Pygame library. It allows writing and editing text directly in a window, with basic support for colored text fragments and keyboard navigation.

The editor focuses on interactive text input and demonstrates handling multiple lines, cursor movement, and simple text formatting within Pygame.

### Features Implemented in This Version

- **Multiple fragments per line:** Each line can contain several `(text, color)` tuples for colored fragments.
- **Cursor navigation:** Move the cursor with arrow keys (Left, Right, Up, Down).
- **Basic editing:**
  - Insert characters at the cursor.
  - Backspace deletes characters before the cursor.
  - Delete removes characters after the cursor.
  - Enter splits a line into two at the cursor position.
  - Tab inserts 4 spaces.
- **Clipboard support:** Paste text with Ctrl+V.
- **Dynamic color detection:** If a typed word matches a predefined color (`red`, `blue`, etc.), the fragment changes color and the color keyword is removed.
- **Rendering:** Text is drawn in a Pygame window, and each fragment respects its assigned color.

### Limitations

- Only one color change per fragment per line (multi-color in one fragment not supported yet).
- Cursor does not automatically track after pasting complex multi-fragment text.
- Editing of existing colored fragments is limited; only the last typed word triggers color change.
- No support for bold, italic, or font changes.
- No undo/redo functionality.

### Code Structure

- **`lines`:** List where each element is a line, itself a list of `(text, color)` tuples.

Example:

```python
lines = [[("hello ", (255,255,255)), ("red", (255,0,0)), (" world", (255,255,255))]]
```

- **Cursor:** Tracked by `cursor_row` and `cursor_col`.
- **`parse_color_name(word)`:** Checks if a word matches a predefined color and returns its RGB tuple.
- **`draw_screen()`:** Clears the window and redraws all text fragments, rendering each with its color. Draws the cursor at the correct position.
- **Event Handling:** Captures keyboard events for editing, navigation, and clipboard pasting.

### Potential Improvements

- Multi-color support within a single line without removing the color keyword.
- Better clipboard handling for multi-fragment text.
- Undo/redo functionality.
- Support for typing color names literally without triggering color change.
- Text alignment, images, and other graphical features.

### Dependencies

- Python 3.10+
- Pygame
- Pyperclip (for clipboard support)
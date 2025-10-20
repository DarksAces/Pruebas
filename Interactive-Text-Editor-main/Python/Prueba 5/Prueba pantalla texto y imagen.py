import pygame
import sys
import os

pygame.init()

# -------------------- CONFIGURACIÓN PANTALLA --------------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Editor TXT con Imágenes - Pygame")
font = pygame.font.SysFont("Consolas", 24)
clock = pygame.time.Clock()

# -------------------- ARCHIVOS --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(BASE_DIR, "contenido.txt")
IMG_DIR = os.path.join(BASE_DIR, "imagenes")

# -------------------- FUNCIONES TEXTO --------------------
def get_line_text(fragments):
    """Devuelve el texto plano de una línea a partir de sus fragmentos."""
    return "".join([t for t, _ in fragments])

def load_txt(filename):
    """Carga el archivo TXT en memoria, cada línea como editable."""
    lines = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for linea in f.readlines():
                linea = linea.rstrip("\n")
                lines.append([[ (linea, (255,255,255)) ], True])
    else:
        lines.append([[("", (255,255,255))], True])  # línea vacía si no existe
    return lines

def save_txt(filename, lines):
    """Guarda el contenido en el archivo TXT."""
    with open(filename, "w", encoding="utf-8") as f:
        for fragments, editable in lines:
            f.write(get_line_text(fragments) + "\n")

def draw_text():
    """Dibuja el texto y el cursor en pantalla."""
    y = 10
    for idx, (fragments, editable) in enumerate(lines):
        x = 10
        full_text = ""
        for text, color in fragments:
            img = font.render(text, True, color)
            screen.blit(img, (x, y))
            x += img.get_width()
            full_text += text

        # Cursor
        if idx == cursor_row and editable:
            cursor_x = 10 + font.size(full_text[:cursor_col])[0]
            pygame.draw.line(screen, (200,200,200), (cursor_x, y), (cursor_x, y+font.get_height()))
        y += font.get_height() + 5

# -------------------- CARGA DE TEXTO --------------------
lines = load_txt(FILENAME)
cursor_row, cursor_col = 0, 0
last_mtime = os.path.getmtime(FILENAME) if os.path.exists(FILENAME) else 0

# -------------------- IMÁGENES --------------------
# Imagen fija
img_fixed = pygame.image.load(os.path.join(IMG_DIR, "img1.png")).convert_alpha()

# Imagen movible
img_movable = pygame.image.load(os.path.join(IMG_DIR, "img2.png")).convert_alpha()
moving_image = {
    "surface": img_movable,
    "pos": [300, 200],
    "dragging": False,
    "resizing": False,
    "scale": 1
}

def draw_images():
    """Dibuja imágenes en pantalla."""
    # Imagen fija
    screen.blit(img_fixed, (50, 100))

    # Imagen movible (escalada)
    surf_scaled = pygame.transform.scale(
        moving_image["surface"],
        (
            int(moving_image["surface"].get_width() * moving_image["scale"]),
            int(moving_image["surface"].get_height() * moving_image["scale"])
        )
    )
    screen.blit(surf_scaled, moving_image["pos"])
    return surf_scaled

# -------------------- MAIN LOOP --------------------
while True:
    screen.fill((30,30,30))

    # Dibujar imágenes y texto
        # -------------------- LIVE RELOAD DEL ARCHIVO --------------------
    if os.path.exists(FILENAME):
        current_mtime = os.path.getmtime(FILENAME)
        if current_mtime != last_mtime:
            lines = load_txt(FILENAME)
            last_mtime = current_mtime

            # Ajustamos el cursor por si el archivo externo es más corto
            cursor_row = min(cursor_row, len(lines)-1)
            cursor_col = min(cursor_col, len(get_line_text(lines[cursor_row][0])))

    surf_scaled = draw_images()
    draw_text()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_txt(FILENAME, lines)  # guarda al salir
            pygame.quit()
            sys.exit()

        # -------------------- RATÓN (mover / redimensionar imágenes) --------------------
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            x, y = moving_image["pos"]
            w, h = surf_scaled.get_size()
            if x <= mx <= x + w and y <= my <= y + h:
                if event.button == 1:  # mover
                    moving_image["dragging"] = True
                    moving_image["offset"] = [mx - x, my - y]
                elif event.button == 3:  # escalar
                    moving_image["resizing"] = True
                    moving_image["resize_start"] = [mx, my]
                    moving_image["scale_start"] = moving_image["scale"]

        elif event.type == pygame.MOUSEBUTTONUP:
            moving_image["dragging"] = False
            moving_image["resizing"] = False

        elif event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            if moving_image.get("dragging"):
                new_x = mx - moving_image["offset"][0]
                new_y = my - moving_image["offset"][1]
                w, h = surf_scaled.get_size()
                new_x = max(0, min(new_x, WIDTH - w))
                new_y = max(0, min(new_y, HEIGHT - h))
                moving_image["pos"] = [new_x, new_y]

            elif moving_image.get("resizing"):
                dx = mx - moving_image["resize_start"][0]
                new_scale = max(0.1, moving_image["scale_start"] + dx / 100)
                moving_image["scale"] = new_scale

                w = int(moving_image["surface"].get_width() * new_scale)
                h = int(moving_image["surface"].get_height() * new_scale)
                x, y = moving_image["pos"]
                x = max(0, min(x, WIDTH - w))
                y = max(0, min(y, HEIGHT - h))
                moving_image["pos"] = [x, y]

        # -------------------- TECLADO (texto editable) --------------------
        elif event.type == pygame.KEYDOWN:
            fragments, editable = lines[cursor_row]
            if not editable:
                continue
            line_text = get_line_text(fragments)

            if event.key == pygame.K_LEFT and cursor_col > 0:
                cursor_col -= 1
            elif event.key == pygame.K_RIGHT and cursor_col < len(line_text):
                cursor_col += 1
            elif event.key == pygame.K_BACKSPACE and cursor_col > 0:
                old_text = fragments[0][0]
                fragments[0] = (old_text[:cursor_col-1] + old_text[cursor_col:], fragments[0][1])
                cursor_col -= 1
                save_txt(FILENAME, lines)
            elif event.key == pygame.K_RETURN:
                lines.insert(cursor_row+1, [[("", (255,255,255))], True])
                cursor_row += 1
                cursor_col = 0
                save_txt(FILENAME, lines)
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:  
                save_txt(FILENAME, lines)
                print("Guardado en", FILENAME)
            else:
                char = event.unicode
                if char.isprintable():
                    old_text = fragments[0][0]
                    fragments[0] = (old_text[:cursor_col] + char + old_text[cursor_col:], fragments[0][1])
                    cursor_col += 1
                    save_txt(FILENAME, lines)

    pygame.display.flip()
    clock.tick(60)

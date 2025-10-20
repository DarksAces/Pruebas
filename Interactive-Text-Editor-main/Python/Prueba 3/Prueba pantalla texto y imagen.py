import pygame
import sys
import os

pygame.init()

# -------------------- CONFIGURACIÓN PANTALLA --------------------
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pantalla Interactiva")
font = pygame.font.SysFont("Consolas", 24)
clock = pygame.time.Clock()

# -------------------- TEXTO --------------------
# Cada línea: ([fragmentos], editable_flag)
# fragmentos: [(texto, color), ...]
lines = [
    [[("Texto fijo NO editable", (200, 200, 200))], False],
    [[("", (255, 255, 255))], True]
]

cursor_row, cursor_col = 1, 0  # Cursor empieza en línea editable

COLORS = {
    "red": (255, 0, 0), 
    "green": (0, 255, 0), 
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0), 
    "white": (255, 255, 255), 
    "black": (0, 0, 0)
}

def get_line_text(fragments):
    return "".join([t for t, c in fragments])

def draw_text():
    y = 10
    for idx, (fragments, editable) in enumerate(lines):
        x = 10
        full_text = ""
        if not fragments:
            fragments.append(("", (255, 255, 255)))
        for text, color in fragments:
            img = font.render(text, True, color)
            screen.blit(img, (x, y))
            x += img.get_width()
            full_text += text

        # Dibujar cursor solo en línea editable
        if idx == cursor_row and editable:
            cursor_x = 10 + font.size(full_text[:cursor_col])[0]
            pygame.draw.line(screen, (200, 200, 200), (cursor_x, y), (cursor_x, y + font.get_height()))
        y += font.get_height() + 5

# -------------------- IMÁGENES --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "imagenes")
img_fixed = pygame.image.load(f"{IMG_DIR}/img1.png").convert_alpha()
img_movable = pygame.image.load(f"{IMG_DIR}/img2.png").convert_alpha()

moving_image = {
    "surface": img_movable,
    "pos": [300, 200],
    "dragging": False,
    "resizing": False,
    "scale": 1
}

# -------------------- MAIN LOOP --------------------
while True:
    screen.fill((30, 30, 30))

    # Dibujar imagen fija
    screen.blit(img_fixed, (50, 100))

    # Dibujar imagen movible escalada
    surf_scaled = pygame.transform.scale(
        moving_image["surface"],
        (int(moving_image["surface"].get_width() * moving_image["scale"]),
         int(moving_image["surface"].get_height() * moving_image["scale"]))
    )
    screen.blit(surf_scaled, moving_image["pos"])

    draw_text()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # -------------------- MOVER / REDIMENSIONAR IMAGEN --------------------
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
                new_x = max(0, min(new_x, 800 - w))
                new_y = max(0, min(new_y, 600 - h))
                moving_image["pos"] = [new_x, new_y]

            elif moving_image.get("resizing"):
                dx = mx - moving_image["resize_start"][0]
                new_scale = max(0.1, moving_image["scale_start"] + dx / 100)
                moving_image["scale"] = new_scale

                w = int(moving_image["surface"].get_width() * new_scale)
                h = int(moving_image["surface"].get_height() * new_scale)
                x, y = moving_image["pos"]
                x = max(0, min(x, 800 - w))
                y = max(0, min(y, 600 - h))
                moving_image["pos"] = [x, y]

        # -------------------- TEXTO EDITABLE --------------------
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
                fragments[0] = (old_text[:cursor_col - 1] + old_text[cursor_col:], fragments[0][1])
                cursor_col -= 1
            elif event.key == pygame.K_RETURN:
                lines.insert(cursor_row + 1, [[("", (255, 255, 255))], True])
                cursor_row += 1
                cursor_col = 0
            else:
                char = event.unicode
                if char.isprintable():
                    old_text = fragments[0][0]
                    fragments[0] = (old_text[:cursor_col] + char + old_text[cursor_col:], fragments[0][1])
                    cursor_col += 1

    pygame.display.flip()
    clock.tick(60)

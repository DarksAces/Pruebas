import pygame
import sys

pygame.init()

# -------------------- CONFIGURACIÓN PANTALLA --------------------
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Editor de Texto Interactivo")
font = pygame.font.SysFont("Consolas", 24)
clock = pygame.time.Clock()

# -------------------- TEXTO --------------------
# Cada línea: ([fragmentos], editable_flag)
# fragmentos: [(texto, color), ...]
lines = [
    [[("Texto fijo NO editable", (200, 200, 200))], False],
    [[("", (255, 255, 255))], True]
]

cursor_row, cursor_col = 1, 0  # cursor empieza en línea editable

COLORS = {
    "red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255),
    "yellow": (255, 255, 0), "white": (255, 255, 255), "black": (0, 0, 0)
}

def get_line_text(fragments):
    return "".join([t for t, c in fragments])

def draw_text():
    y = 10
    for idx, (fragments, editable) in enumerate(lines):
        x = 10
        full_text = ""
        # Asegurarse de que haya al menos un fragmento
        if not fragments:
            fragments.append(("", (255, 255, 255)))
        for text, color in fragments:
            img = font.render(text, True, color)
            screen.blit(img, (x, y))
            x += img.get_width()
            full_text += text
        # dibujar cursor solo en línea editable
        if idx == cursor_row and editable:
            cursor_x = 10 + font.size(full_text[:cursor_col])[0]
            pygame.draw.line(screen, (200, 200, 200), (cursor_x, y), (cursor_x, y + font.get_height()))
        y += font.get_height() + 5

# -------------------- BUCLE PRINCIPAL --------------------
while True:
    screen.fill((30, 30, 30))
    draw_text()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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

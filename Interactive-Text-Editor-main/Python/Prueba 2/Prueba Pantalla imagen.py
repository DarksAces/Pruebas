import pygame
import sys
import os

pygame.init()

# Configuración de ventana
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Editor de Imágenes Controladas")
clock = pygame.time.Clock()

# Carpeta de imágenes relativa al script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "imagenes")

images = [
    {"surface": pygame.image.load(os.path.join(IMG_DIR, "img1.png")), "pos": [100, 100], "movible": False, "scale": 0.5},
    {"surface": pygame.image.load(os.path.join(IMG_DIR, "img2.png")), "pos": [300, 200], "movible": True, "scale": 0.5},
]


dragging_image = None
offset_x = 0
offset_y = 0
resizing = False

def draw_screen():
    screen.fill((50, 50, 50))
    for img in images:
        surf = pygame.transform.scale(img["surface"], (
            int(img["surface"].get_width() * img["scale"]),
            int(img["surface"].get_height() * img["scale"])
        ))
        screen.blit(surf, img["pos"])
    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Click izquierdo para mover
                for img in reversed(images):
                    surf_scaled = pygame.transform.scale(img["surface"], (
                        int(img["surface"].get_width() * img["scale"]),
                        int(img["surface"].get_height() * img["scale"])
                    ))
                    rect = surf_scaled.get_rect(topleft=img["pos"])
                    if rect.collidepoint(event.pos) and img["movible"]:
                        dragging_image = img
                        offset_x = event.pos[0] - img["pos"][0]
                        offset_y = event.pos[1] - img["pos"][1]
                        break
            elif event.button == 3:  # Click derecho para redimensionar
                for img in reversed(images):
                    surf_scaled = pygame.transform.scale(img["surface"], (
                        int(img["surface"].get_width() * img["scale"]),
                        int(img["surface"].get_height() * img["scale"])
                    ))
                    rect = surf_scaled.get_rect(topleft=img["pos"])
                    if rect.collidepoint(event.pos) and img["movible"]:
                        dragging_image = img
                        resizing = True
                        offset_x = event.pos[0] - img["pos"][0]
                        offset_y = event.pos[1] - img["pos"][1]
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button in [1, 3]:
                dragging_image = None
                resizing = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging_image:
                if resizing:
                    # Escalar basado en movimiento del ratón
                    new_width = max(20, event.pos[0] - dragging_image["pos"][0])
                    new_height = max(20, event.pos[1] - dragging_image["pos"][1])
                    dragging_image["scale"] = min(new_width / dragging_image["surface"].get_width(),
                    new_height / dragging_image["surface"].get_height())
                else:
                    # Mover, limitado a márgenes
                    new_x = event.pos[0] - offset_x
                    new_y = event.pos[1] - offset_y
                    surf_scaled = pygame.transform.scale(dragging_image["surface"], (
                        int(dragging_image["surface"].get_width() * dragging_image["scale"]),
                        int(dragging_image["surface"].get_height() * dragging_image["scale"])
                    ))
                    new_x = max(0, min(WINDOW_WIDTH - surf_scaled.get_width(), new_x))
                    new_y = max(0, min(WINDOW_HEIGHT - surf_scaled.get_height(), new_y))
                    dragging_image["pos"][0] = new_x
                    dragging_image["pos"][1] = new_y

    draw_screen()
    clock.tick(60)

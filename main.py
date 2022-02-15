import pygame
import sys
from pygame.locals import *
import logic
import button

# Inicializar pygame
pygame.init()
mainClock = pygame.time.Clock()

# Inicializar ventana
ANCHO = 640
ALTO = 480
windowSurface = pygame.display.set_mode(
    (ANCHO, ALTO),
    0, 32, 0, 1
)
pygame.display.set_caption('Categorizador')

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

#load button images
start_img = pygame.image.load('start_btn.png').convert_alpha()
exit_img = pygame.image.load('exit_btn.png').convert_alpha()

#create button instances
start_button = button.Button(100, 200, start_img, 0.8) # X, Y, Imagen, Escala
exit_button = button.Button(450, 200, exit_img, 0.8) # X, Y, Imagen, Escala

while True:
    # Events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw
    windowSurface.fill(BLANCO)
    if start_button.draw(windowSurface):
        logic.computar()
    if exit_button.draw(windowSurface):
        pygame.quit()
        sys.exit()
    pygame.display.update()
    mainClock.tick(10)
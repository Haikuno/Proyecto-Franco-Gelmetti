import pygame
from pygame.locals import *
import sys
import logic
import button
import os

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

# Cargar íconos
directorio = os.getcwd()
start_img = pygame.image.load(
    directorio + r'/iconos/start_btn.png').convert_alpha()
exit_img = pygame.image.load(
    directorio + r'/iconos/exit_btn.png').convert_alpha()

# Crear botones
start_button = button.Button(100, 200, start_img, 0.8)  # X, Y, Imagen, Escala
exit_button = button.Button(450, 200, exit_img, 0.8)  # X, Y, Imagen, Escala

while True:
    # Eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Dibujar
    windowSurface.fill(BLANCO)
    if start_button.draw(windowSurface):
        print("COMPUTANDO JEJE XD")
        logic.computar()
    if exit_button.draw(windowSurface):
        pygame.quit()
        sys.exit()
    pygame.display.update()
    mainClock.tick(10)

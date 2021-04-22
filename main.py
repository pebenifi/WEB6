import pygame
import requests


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
running = 1
FPS = 10
clock = pygame.time.Clock()
while running:
    pygame.event.wait()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = 0
    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(FPS)
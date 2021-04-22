import pygame
import requests
import os

name = 'map.png'
URL = 'http://static-maps.yandex.ru/1.x/'
params = {'ll': ",".join(['37.530887', '55.7033118']),
          'l': 'sat',
          'spn': ','.join(['0.002', '0.002'])}

def get_image(params):
    image = requests.get(URL, params=params)
    if image:
        return image
    print(image.content)

def load_image(image):
    with open('map.png', 'wb') as f:
        f.write(image.content)

def show_image(screen):
    screen.blit(pygame.image.load('map.png'), (0, 0))


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
    image = get_image(params)
    if image:
        load_image(image)
        show_image(screen)

    pygame.display.flip()
    clock.tick(FPS)

os.remove(name)
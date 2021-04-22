import pygame
import requests
import os


name = 'map.png'
URL = 'http://static-maps.yandex.ru/1.x/'
ll = [37.530887, 55.7033118]
l = 'sat'
spn = [0.002, 0.002]

def get_image():
    image = requests.get(URL, params=get_params())
    if image:
        return image
    print(image.content)
def load_image(image):
    with open('map.png', 'wb') as f:
        f.write(image.content)

def show_image(screen):
    screen.blit(pygame.transform.scale(pygame.image.load('map.png'), (width, height)), (0, 0))


def get_params():
    return {'ll': f"{ll[0]},{ll[1]}", "spn": f"{spn[0]},{spn[1]}", 'l': l}


pygame.init()
size = width, height = 600, 465
screen = pygame.display.set_mode(size)
running = 1
FPS = 10
clock = pygame.time.Clock()
while running:
    pygame.event.wait()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = 0
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_UP:
                ll[1] += 0.001
            elif ev.key == pygame.K_DOWN:
                ll[1] -= 0.001
            elif ev.key == pygame.K_LEFT:
                ll[0] -= 0.001
            elif ev.key == pygame.K_RIGHT:
                ll[0] += 0.001
    screen.fill((0, 0, 0))
    image = get_image()
    if image:
        load_image(image)
        show_image(screen)
    pygame.display.flip()
    clock.tick(FPS)
os.remove(name)
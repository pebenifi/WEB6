import pygame
import requests
import os
from server import get_ll

all_sprites = pygame.sprite.Group()
name = 'map.png'
URL = 'http://static-maps.yandex.ru/1.x/'
ll = [37.530887, 55.7033118]
l = 'sat'
spn = [0.002, 0.002]
lastll = [34, 34]
size = width, height = 600, 465
pt = ''
scale_value = spn[0]
pygame.init()


def load_image(filename, colorkey=None):
    fullname = os.path.join('data', filename)
    if os.path.isfile(fullname):
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image.convert()
            image.set_colorkey(image.get_at((0, 0)))
        else:
            image.convert_alpha()
        return image
    else:
        print(f"{fullname} не найден")


class InputBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((200, 30))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.status = 0
        self.rect.y = height - 50
        self.font = pygame.font.Font('data/sans.ttf', 20)
        self.address = ''

    def checkClicked(self, pos):
        if self.rect.x < pos[0] < self.rect.x + self.rect.w and \
                self.rect.y < pos[1] < self.rect.y + self.rect.h or self.address or self.address:
            self.status = 1
        else:
            self.status = 0
        self.refreshBox()

    def refreshBox(self):
        self.image = pygame.Surface((200, 30))
        self.image.fill((255, 255, 255))

    def update(self):
        self.refreshBox()
        if self.status:
            text = self.font.render(self.address, 0, (100, 100, 100))
            self.image.blit(text, (2, 2))
        else:
            text = self.font.render('Введите сюда адрес', 0, (100, 100, 100))
            self.image.blit(text, (2, 2))
        pygame.display.flip()


class PushButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((70, 30))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 220
        self.rect.y = height - 50
        self.status = 0
        self.font = pygame.font.Font('data/sans.ttf', 20)

    def update(self):
        if self.status:
            pass
        else:
            text = self.font.render('Искать', 0, (100, 100, 100))
            self.image.blit(text, (2, 2))

    def checkClicked(self, pos):
        if self.rect.x < pos[0] < self.rect.x + self.rect.w and \
                self.rect.y < pos[1] < self.rect.y + self.rect.h:
            return 1

    def find(self, addres):
        global ll
        global pt
        new_ll = get_ll(addres)
        if new_ll:
            ll = new_ll
            pt = f'{ll[0]},{ll[1]},pm2rdl1'


box = InputBox()
button = PushButton()


def get_image():
    image = requests.get(URL, params=get_params())
    if image:
        return image
    print(image.content)


def checkState():
    return lastll != ll


def load_image(image):
    with open('map.png', 'wb') as f:
        f.write(image.content)


def show_image(screen):
    screen.blit(pygame.transform.scale(pygame.image.load('map.png'), (width, height)), (0, 0))


def get_params():
    return {'ll': f"{ll[0]},{ll[1]}", "spn": f"{spn[0]},{spn[1]}", 'l': l, 'pt': pt}


pygame.init()
screen = pygame.display.set_mode(size)
running = 1
FPS = 10
type_maps = ['sat', 'map', 'map,skl,trf']
clock = pygame.time.Clock()
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = 0
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_PAGEUP:
                spn[0] -= scale_value / 2
                spn[1] -= scale_value / 2
            elif ev.key == pygame.K_PAGEDOWN:
                spn[0] += scale_value / 2
                spn[1] += scale_value / 2
            elif ev.key == pygame.K_UP:
                ll[1] += scale_value / 10
            elif ev.key == pygame.K_DOWN:
                ll[1] -= scale_value / 10
            elif ev.key == pygame.K_RIGHT:
                ll[0] += scale_value / 10
            elif ev.key == pygame.K_LEFT:
                ll[0] -= scale_value / 10
            elif ev.key == pygame.K_1:
                l = type_maps[0]
            elif ev.key == pygame.K_2:
                l = type_maps[1]
            elif ev.key == pygame.K_3:
                l = type_maps[2]
            elif box.status:
                if ev.key == pygame.K_BACKSPACE:
                    box.address = box.address[:-1]
                else:
                    box.address += ev.unicode
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            box.checkClicked(ev.pos)
            if button.checkClicked(ev.pos):
                button.find(box.address)
    if checkState():
        image = get_image()
        if image:
            screen.fill((0, 0, 0))
            load_image(image)
            show_image(screen)
            lastll = ll[:]
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    print(scale_value, spn[0])
    clock.tick(FPS)

os.remove(name)

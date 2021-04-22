import pygame
import requests
import os
from server import get_full_address, get_ll

pygame.init()
all_sprites = pygame.sprite.Group()
name = 'map.png'
URL = 'http://static-maps.yandex.ru/1.x/'
ll = [37.530887, 55.7033118]
l = 'sat'
spn = [0.002, 0.002]
pt = ''
scale_value = spn[0]
size = width, height = 600, 465
screen = pygame.display.set_mode(size)
lastll = None
last_spn = None
last_pt = None
last_l = None
crit_coords = [ll[0] + scale_value / 10, ll[0] - scale_value / 10,
               ll[1] + scale_value / 10, ll[1] - scale_value / 10]


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


class OutputField(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((200, 100))
        self.image.fill((255, 255, 255))
        self.font = pygame.font.Font('data/sans.ttf', 12)
        self.rect = self.image.get_rect()
        self.rect.x = width - self.image.get_width() - 10
        self.rect.y = height - self.image.get_height() - 10

    def displayText(self, text):
        portion_of_text = 30
        height = self.font.get_height()
        count = 0
        while text:
            text_render = self.font.render(text[:portion_of_text], 0, (100, 100, 100))
            self.image.blit(text_render, (0, height * count))
            text = text[portion_of_text:]
            count += 1

    def freshDisplay(self):
        self.image = pygame.Surface((200, 400))
        self.image.fill((255, 255, 255))


class PostIndexTumbler(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((50, 50))
        self.color = (100, 100, 100)
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
        self.rect.x = width - 215
        self.rect.y = height - 160
        self.icon = pygame.transform.scale(load_image('postIcon.png', -1), (30, 30))
        self.active = 0

    def update(self):
        if self.active:
            self.color = (255, 255, 0)
        else:
            self.color = (100, 100, 100)
        print(self.color)
        pygame.draw.circle(self.image, self.color, (self.image.get_width() // 2, self.image.get_height() // 2), 20, 0)
        self.image.blit(self.icon,
                        (self.rect.w // 2 - self.icon.get_width() // 2, self.rect.h // 2 - self.icon.get_height() // 2))

    def changeStatus(self):
        if self.active == 0:
            self.active = 1
        else:
            self.active = 0
        print('eve')

    def checkClicked(self, pos):
        if self.rect.x <= pos[0] <= self.rect.x + self.rect.w and self.rect.y <= pos[1] <= self.rect.y + self.rect.h:
            self.changeStatus()


tumbler = PostIndexTumbler()
field = OutputField()


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
        return 0

    def find(self, addres):
        global crit_coords
        global ll
        global pt
        new_ll = get_ll(addres)
        address = get_full_address(addres)
        crit_coords = []
        crit_coords.append(ll[1] + (600 // 2) * scale_value)
        crit_coords.append(ll[1] - (600 // 2) * scale_value)
        crit_coords.append(ll[0] + (465 // 2) * scale_value)
        crit_coords.append(ll[0] - (465 // 2) * scale_value)
        field.freshDisplay()
        field.displayText(address)
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
    return lastll != ll or last_pt != pt or last_spn != spn or last_l != l


def load_image(image):
    with open('map.png', 'wb') as f:
        f.write(image.content)


def show_image(screen):
    image = pygame.transform.scale(pygame.image.load('map.png'), (width, height))
    screen.blit(image, (0, 0))


def get_params():
    return {'ll': f"{ll[0]},{ll[1]}", "spn": f"{spn[0]},{spn[1]}", 'l': l, 'pt': pt}


pygame.init()

running = 1
FPS = 10
vel = 0.5
map_layers = ['sat', 'map', 'map,skl,trf']
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
                l = map_layers[0]
            elif ev.key == pygame.K_2:
                l = map_layers[1]
            elif ev.key == pygame.K_3:
                l = map_layers[2]
            elif box.status:
                if ev.key == pygame.K_BACKSPACE:
                    box.address = box.address[:-1]
                else:
                    box.address += ev.unicode
            print(ll[0], crit_coords[2])
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            box.checkClicked(ev.pos)
            if button.checkClicked(ev.pos):
                button.find(box.address)
            tumbler.checkClicked(ev.pos)
    if checkState():
        image = get_image()
        if image:
            screen.fill((0, 0, 0))
            load_image(image)
            show_image(screen)
            last_l = l[:]
            last_spn = spn[:]
            last_pt = pt
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
os.remove(name)

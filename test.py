import pygame
import requests
from PIL import Image

pygame.init()
name = 'map.png'
URL = 'http://static-maps.yandex.ru/1.x/'
ll = [37.530887, 55.7033118]
l = 'sat'
spn = [0.002, 0.002]
lastll = [34, 34]

def get_params():
    return {'ll': f"{ll[0]},{ll[1]}", "spn": f"{spn[0]},{spn[1]}", 'l': l}

request = requests.get(URL, params=get_params())
print(len(request.content))
print(type(request.content))
im = Image.frombytes('RGB', (600, 1000), request.content)
print(im)
image = pygame.image.fromstring(request.content, (6991, 10), 'RGB', False)
import requests
import json

URL = 'https://geocode-maps.yandex.ru/1.x/'
apikey = "40d1649f-0493-4b70-98ba-98533de7710b"


def get_ll(address):
    print(address)
    params = {'apikey': apikey, 'geocode': address, 'format': "json"}
    r = requests.get(URL, params=params).json()
    if int(r['response']["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"]):
        ll = list(map(float,
                      r['response']["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]['pos'].split(' ')))
        return ll
    print('Вы ввели неправильный адрес')

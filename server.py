import requests
import json

URL = 'https://geocode-maps.yandex.ru/1.x/'
apikey = "40d1649f-0493-4b70-98ba-98533de7710b"


def get_json_data(address):
    params = {'apikey': apikey, 'geocode': address, 'format': "json"}
    r = requests.get(URL, params=params).json()
    if int(r['response']["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"]):
        return r
    print('Вы ввели неправильный адрес')


def get_ll(address):
    data = get_json_data(address)
    crit_coords = []
    if data:
        ll = list(map(float,
                      data['response']["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]['pos'].split(
                          ' ')))
        crit_coords.append(ll[1] + 600 // 2 * 0.02)
        crit_coords.append(ll[1] - 600 // 2 * 0.02)
        crit_coords.append(ll[0] + 465 // 2 * 0.02)
        crit_coords.append(ll[0] - 465 // 2 * 0.02)
        return ll


def get_full_address(address):
    data = get_json_data(address)
    if data:
        address = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
            "GeocoderMetaData"]['text']
        return address
# def get_full_adress(address):
#     params = {'apikey': apikey, 'geocode': address, 'format': "json"}
#     r = requests.get(URL, params=params).json()
#     if int(r['response']["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"]):
#         return ll
#     print('Вы ввели неправильный адрес')
from io import BytesIO
import requests
from PIL import Image
import sys


def get_spn(poss_1, poss_2):
    print(poss_1, poss_2)
    delta_x = str((list(map(float, poss['upperCorner'].split()))[0] - list(map(float, poss['lowerCorner'].split()))[0]))
    delta_y = str((list(map(float, poss['upperCorner'].split()))[1] - list(map(float, poss['lowerCorner'].split()))[1]))
    return delta_x, delta_y


pl = []
for line in sys.stdin:
    pl.append(line.rstrip())
pl_2 = ','.join(pl)
toponym_to_find = ' '.join('Санкт-Петербург')
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    pass

marks, sites = [], []
for site in sites:
    toponym_to_find = ' '.join(f'{toponym_to_find}, {site}')
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    res = requests.get(geocoder_api_server, params=geocoder_params)
    j_res = res.json()
    top = j_res["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    marks.append(','.join(top["Point"]["pos"].split()))

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
print(toponym_coodrinates)
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
i = 0
x, y = [], []
for elem in pl:
    i += 1
    if i % 2 == 0:
        x.append(elem)
    else:
        y.append(elem)

# "ll": ",".join([toponym_longitude, toponym_lattitude]),
map_params = {
    "spn": ",".join(get_spn(f'{max(x)} {max(y)}', f'{min(x)} {min(y)}')),
    "l": "map",
    "pt": '~'.join(marks),
    "pl": pl_2
}
# ','.join(toponym_coodrinates.split())
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
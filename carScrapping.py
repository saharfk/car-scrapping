import requests
import re
from bs4 import BeautifulSoup

model_mashin = input('name mashin ra be engelisi vared konid:\n')
page = 1
tedade_mashin = 0
car_names2 = []
car_price2 = []
car_karkard2 = []

# modehae mashini ke mitavanid emtehan konid:(tamami model hae mashin ra migird
# bmw  peugeot  renault  mercedes-benz   honda

while page <= 2:
    address = 'https://bama.ir/car/' + model_mashin + '/all-models/all-trims?page=' + str(page)
    r = requests.get(address)
    soup = BeautifulSoup(r.text, 'html.parser')

    # ............................................
    # peyda krdane asami mashin ha va vared krdane anha be list

    car_names = soup.find_all('h2', attrs={'itemprop': 'name'})

    for i in range(len(car_names)):
        if i % 2 == 0:
            car_names2.append(re.sub(r'\s+', ' ', car_names[i].text).strip())

    # ............................................
    # peyda krdne gheymat ha va vared krdane anha be list

    car_price = soup.find_all('p', attrs={'class': 'cost'})
    for car in car_price:
        car_price2.append(re.sub(r'\s+', ' ', car.text).strip())

    # ............................................
    # peyda krdne karkard ha va vared krdane anha be list

    car_karkard = soup.find_all('p', attrs={'class': 'price milage-text-mobile visible-xs price-milage-mobile'})
    for car in car_karkard:
        car_karkard2.append(car.text)
    page += 1

for i in range(0, 20):
    print(car_names2[i] + ' :')
    print('قیمت  ' + car_price2[i])
    print(car_karkard2[i])
    print('...............................................')

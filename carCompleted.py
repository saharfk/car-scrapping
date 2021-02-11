import requests
import re
from bs4 import BeautifulSoup
import mysql.connector
from sklearn import tree
from sklearn import preprocessing
import pandas


# TODO salam dr tamami todo ha tozihate lameze dade shode ast

def ml():
    print('این گزینه تا اطلاع ثانوی غیر فعال میباشد گزینه دیگری را انتخاب کنید')


#     a = web_scraping()
#     car_name = []
#     # car_model = []
#     car_price = []
#     # car_year = []
#     for i in a:
#         car_name.append(i[0])
#         car_price.append(i[2])
#
#     clf = tree.DecisionTreeClassifier()
#     clf.fit(car_price, car_name.encode('utf-8'))
#     new = [[100000000]]
#     ans = clf.predict(new)
#     print(ans[0])
# #     **************************
#     a = web_scraping()
#     car_name = []
#     car_model = []
#     car_price = []
#     car_year = []
#     for i in a:
#         car_name.append(i[0])
#         car_model.append(i[1])
#         car_price.append(i[2])
#         car_year.append(i[3])
#
#     le1 = preprocessing.LabelEncoder()
#     le1.fit(car_name)
#     le2 = preprocessing.LabelEncoder()
#     le2.fit(car_model)
#
#     list(le1.classes_)
#     list(le2.classes_)
#     le1.transform(car_name)
#     le2.transform(car_model)
#     print(le1)
#     print(le2)
#
#     # list(le.inverse_transform([2, 2, 1]))

# TODO dr inja data base chek mishavad agr data basi vojud nadasht yki dorost mikond
def creat_database():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="car"
        )
        # print('existed')


    except:

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="1234"
        )

        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE car")

        # print('created')


# TODO dr inja table dorost mishavad va agr vojud dasht table pak shode va dobre data varedash mishavad
def creat_table():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="car"
        )
        mycursor = mydb.cursor()
        mycursor.execute(
            "CREATE TABLE cars (carName VARCHAR(255),model VARCHAR(255), price bigint, years INT)")

    except:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="car"
        )
        mycursor = mydb.cursor()
        mycursor.execute(
            "DELETE FROM cars")
        mydb.commit()


# TODO dr inja mashin ha varede data base mishavand
def insert_car(a):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="car"
    )
    mycursor = mydb.cursor()
    for i in a:
        # print(i[0])
        mycursor.execute('INSERT INTO cars (carName,model,price,years) VALUES (%s,%s,%s,%s)',
                         (i[0], i[1], int(i[2]), int(i[3])))
        mydb.commit()

    # print(mycursor.rowcount, "record inserted.")


# TODO table ra neshan midahad
def show_table():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="car"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cars")
    myresult = mycursor.fetchall()

    for x in myresult:
        print('نام ماشین: ', x[0])
        print('مدل ماشین: ', x[1])
        print('قیمت ماشین: ', x[2])
        print('سال تولید: ', x[3])
        print('*****************')


# TODO hadaghal va hadaksr gheymat ra migird va va mashin hae bein in gheymat ra neshan midahad
def search_car_price(low, high):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="car"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cars WHERE price BETWEEN %s AND %s", (low, high,))
    myresult = mycursor.fetchall()

    for x in myresult:
        print('نام ماشین: ', x[0])
        print('مدل ماشین: ', x[1])
        print('قیمت ماشین: ', x[2])
        print('سال تولید: ', x[3])
        print('*****************')


# TODO esm mashin ra migird va mashin hae ba in esm ra neshan midahad
def search_car_name(name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="car"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cars WHERE carName=%s", (name,))
    myresult = mycursor.fetchall()

    for x in myresult:
        print('نام ماشین: ', x[0])
        print('مدل ماشین: ', x[1])
        print('قیمت ماشین: ', x[2])
        print('سال تولید: ', x[3])
        print('*****************')


# TODO string adad ba , ra gerefte , ra joda mikond va adad ra b int tabdil mikond
def adad_saz(adad):
    try:
        a = str(adad).split(',')

        if len(a) == 4:
            return int(a[0]) * 1000000000 + int(a[1]) * 1000000 + int(a[2]) * 1000 + int(a[3])
        if len(a) == 3:
            return int(a[0]) * 1000000 + int(a[1]) * 1000 + int(a[2])
        if len(a) == 2:
            return int(a[0]) * 1000 + int(a[1])
        if len(a) == 1:
            return int(a[0])
    except:
        return -1


# TODO etelaat web ra migird
def web_scraping():
    # TODO tedade safahat ro be 200 afzayesh bede
    page = 1
    # tedade_mashin = 0
    car_names2 = []
    car_year = []
    car_price2 = []
    car_karkard2 = []

    # modehae mashini ke mitavanid emtehan konid:(tamami model hae mashin ra migird
    # bmw  peugeot  renault  mercedes-benz   honda
    # TODO inja mitavanid tedade safahat ra kam ya ziad konid
    while page <= 200:
        address = 'https://bama.ir/car/all-brands/all-models/all-trims?page=' + str(page)
        # print(address)
        print('در حال اسکن صفحه ی ', page)
        r = requests.get(address)
        soup = BeautifulSoup(r.text, 'html.parser')

        # ............................................
        # peyda krdane asami mashin ha va vared krdane anha be list

        car_names = soup.find_all('h2', attrs={'itemprop': 'name'})

        for i in range(len(car_names)):
            if i % 2 == 1:
                car_names2.append(re.sub(r'\s+', ' ', car_names[i].text).strip())
            else:
                x = re.sub(r'\s+', ' ', car_names[i].text).strip().split('،')
                car_year.append(x[0])

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
    f = []
    info = []
    for i in range(len(car_names2)):
        tik = str(car_names2[i]).split("،")
        f.append(tik[0])
        f.append(tik[1].strip())
        tik = str(car_price2[i]).split()
        s = adad_saz(tik[0])
        if s == -1:
            f = []
        else:
            f.append(s)
            f.append(int(car_year[i]))
            info.append(f)
            f = []
        # print(car_names2[i] + ' :')
        # print('قیمت  ' + car_price2[i])
        # print('سال  ' + car_year[i])
        # print('...............................................')

    return info


try:
    print('سلام خوش آمدید')
    print('در حال گرفتن اطلاعات از سایت مورد نظر لطفا شکیبا باشید...')
    a = web_scraping()

    creat_database()
    creat_table()
    insert_car(a)
    print('اطلاعات با موفقیت گرفته و ذخیره شد')
    while True:
        entekhab_kar = int(input("عدد کار مورد نظر خود را انتخاب کنید:\n"
                                 "1.دیدن اطلاعات دیتا بیس\n"
                                 "2.تخمین قیمت\n"
                                 "3.سرچ بازه قیمت\n"
                                 "4.سرچ اسم\n"
                                 "5.خروج\n"))

        if entekhab_kar == 1:
            show_table()
        elif entekhab_kar == 2:
            ml()
        elif entekhab_kar == 3:
            search_car_price(int(input('حداقل قیمت خودرا به تومان وارد کنید:\n')),
                             int(input('\nحداکثر قیمت خودرا به تومان وارد کنید:\n')))

        elif entekhab_kar == 4:
            search_car_name(input('لطفا اسم ماشین مورد نظر را وارد نمایید:\n'))
        else:
            print("خدانگهدار")
            break
except:
    print('مشکلی پیش امد دوباره امتحان کنید')

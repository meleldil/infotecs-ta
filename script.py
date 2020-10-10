from datetime import datetime
from pytz import timezone
from flask import Flask, jsonify, request

with open('RU.txt', encoding='utf-8') as data:
    ru_list = [i.rstrip('\n') for i in data.readlines()]

ru_keys = ['geonameid', 'name', 'asciiname', 'alternatenames',
          'latitude', 'longitude', 'feature class', 'feature code',
          'country code', 'cc2', 'admin1 code', 'admin2 code',
          'admin3 code', 'admin4 code', 'population', 'elevation',
          'dem', 'timezone', 'modification date']

ru = []

for line in ru_list:
    voc = {}
    for item in range(len(line.split('\t'))):
        voc[ru_keys[item]] = line.split('\t')[item]
    ru.append(voc)

app = Flask(__name__)
app.config.update(JSON_SORT_KEYS=False, JSON_AS_ASCII=False)

# Главная страница
@app.route('/', methods=['GET'])
def home():
    return "<h1>Тестовое задание Infotecs для стажера на позицию «Аналитик (python)»</h1>" \
           "<p>Подготовил Александр Усов</p>"

# Метод 1 - информация о городе
@app.route('/cities', methods=['GET'])
def get_all_cities():
    return jsonify(ru)

@app.route('/cities/<int:city_id>', methods=['GET'])
def get_city_info(city_id):
    for elem in range(len(ru)):
        if ru[elem]['geonameid'] == str(city_id):
            return jsonify(ru[elem])

# Метод 2 - список городов с их информацией по номеру страницы
@app.route('/cities/select', methods=['GET'])
def get_page():
    page = request.args.get('page', default = 1, type = int)
    count = request.args.get('count', default = len(ru), type = int)

    def divide(n):
        for i in range(0, len(ru), n):
            yield ru[i:i + n]

    res = list(divide(count))[page - 1]
    return jsonify(res)

# Метод 3 - сравнение двух городов
@app.route('/cities/compare', methods=['GET'])
def cities_compare():
    city_1 = request.args.get('city_1', type = str)
    city_2 = request.args.get('city_2', type = str)
    cities_1 = []
    cities_2 = []

    for city in range(len(ru)):
        if ru[city]['asciiname'] == city_1:
            cities_1.append(ru[city])
        if ru[city]['asciiname'] == city_2:
            cities_2.append(ru[city])

    def convert_variables(city_list):
        for i in range(len(city_list)):
            city_list[i]['geonameid'] = int(city_list[i]['geonameid'])
            city_list[i]['latitude'] = float(city_list[i]['latitude'])
            city_list[i]['population'] = int(city_list[i]['population'])
        return city_list

    cities_1_converted = convert_variables(cities_1)
    cities_2_converted = convert_variables(cities_2)

    city_1 = sorted(cities_1_converted, key=lambda c: c['population'], reverse=True)[0]
    city_2 = sorted(cities_2_converted, key=lambda c: c['population'], reverse=True)[0]

    if city_1['latitude'] > city_2['latitude']:
        north = city_1['name']
    else:
        north = city_2['name']

    if city_1['timezone'] == city_2['timezone']:
        tz = 1
    else:
        tz = 0

    def get_timezone_diff(time_a, time_b):
        if time_a > time_b:
            diff = int((time_a - time_b).seconds / 3600)
        elif time_a < time_b:
            diff = -int((time_b - time_a).seconds / 3600)
        else:
            diff = 0
        return diff

    timezone_1 = city_1['timezone']
    timezone_2 = city_2['timezone']
    time_1 = timezone(timezone_1).localize(datetime.today())
    time_2 = timezone(timezone_2).localize(datetime.today())

    timezone_diff = get_timezone_diff(time_1, time_2)

    extra_info = {'north' : north, 'timezone' : tz, 'timezone_diff' : timezone_diff}

    res = {'city_1' : city_1, 'city_2' : city_2, 'extra_info' : extra_info}

    return jsonify(res)

#Метод бонусный - подсказки для поиска
@app.route('/cities/autocomplete/<string:search>', methods=['GET'])
def autocomplete(search):
    all_names = []
    for i in range(len(ru)):
        name = ru[i]['asciiname']
        all_names.append(name)
    all_names = set(all_names)
    autocomplete_list = [i for i in all_names if search in i]
    return jsonify(autocomplete_list)

if __name__ == '__main__':
    app.run(port=8000)
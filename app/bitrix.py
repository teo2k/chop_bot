import requests
import config
from fuzzywuzzy import process


def check_city(user_city):
    vahta_id = '999'
    cities = {
        'Москва': '262',
        'МСК': '262',
        'СПБ': '263',
        'Питер': '263',
        'Санкт-Петербург': '263',
        'Воронеж': '264',
        'Липецк': '265',
        'Чебоксары': '266',
        'Нижний Новгород': '267',
        'Нижегородская область, д. Федяково': '268',
        'Владимирская область, г. Александров': '269',
        'Самара': '294',
        'Тольятти': '295',
        'Киров': '296',
        'Тамбов': '297',
        'Тула': '298',
        'Калининград': '299',
        'Ижевск': '300',
        'Архангельск': '301',
        'Казань': '302',
        'Нижнекамск': '303',
        'Томск': '304',
        'Набережные Челны': '327',
        'Омск': '328',
        'Обь': '329',
        'Сочи': '330',
        'Симферополь': '331',
        'Севастополь': '332',
        'Феодосия Республика Крым': '333',
        'Армянск Республика Крым': '334',
        'Белогорск Республика Крым': '335',
        'Ленино Республика Крым': '336',
        'Черноморское Республика Крым': '357',
        'Саки Саки Республика Крым': '358',
        'Нижнегорский Республика Крым': '359',
        'Красноперекопск Республика Крым': '360',
        'Керчь': '361',
        'Брянск': '362',
        'Тверь': '363',
        'Екатеринбург': '364',
        'Ялта': '365',
        'Тюмень': '366',
        'Ейск': '367',
        'Новая Адыгея': '368',
        'Красноярск': '369',
        'Мурманск': '370',
        'Уфа': '399',
        'Новосибирск': '400',
        'Челябинск': '401',
        'Ярославль': '402',
        'Пермь': '403',
        'Манчигорск': '404',
        'Сегежа': '405',
        'Кострома': '406',
        'Смоленск': '407',
        'Орел': '408',
        'Владивосток': '409',
        'Уссурийск': '410',
        'Хабаровск': '411',
        'Сыктывкар Республика Коми': '412',
        'Ростов на Дону': '413',
        'Иваново': '414',
        'Туапсе': '415',
        'Оренбург': '416',
        'Саратов': '417',
        'Сызрань': '418',
        'Краснодар': '419',
        'Вологда': '420',
        'Комсомольск на Амуре': '421',
        'Нижний Тагил': '422',
        'Благовещенск': '423',
        'Владимир': '424',
        'г. Апатиты (Мурманская область)': '546'
    }
    if len(user_city) < 3:
        return [vahta_id, f'Город указанный пользователем:{user_city}']
    city, confidence = process.extractOne(user_city, cities.keys())
    if confidence > 80:
        return [cities[city], '']
    else:
        return [vahta_id, f'Город указанный пользователем:{user_city}']


def check_test_city(user_city):
    vahta_id = '999'
    cities = {
    "Москва": "53",
    "МСК": "53",
    "СПБ": "55",
    "Питер": "55",
    "Санкт-Петербург": "55",
    "Сызрань": "57",
    "Вологда": "59",
    "Воронеж": "61",
    "Уфа": "63",
    "Красноярск": "65",
    "Краснодар": "67",
    "Курск": "69",
    "Новосибирск": "71",
    }
    if len(user_city) < 3:
        return [vahta_id, f'Город указанный пользователем:{user_city}']
    city, confidence = process.extractOne(user_city, cities.keys())
    if confidence > 80:
        return [cities[city],'']
    else:
        return [vahta_id, f'Город указанный пользователем:{user_city}']


def create_test_lead(name, surname, phone, city, age):
    WEBHOOK_URL = config.bitrix_send_test_url
    city_com = check_test_city(city)
    lead_data = {
        'fields': {
            'TITLE': f'{name} {surname}|{phone}',
            'NAME': name,
            'LAST_NAME': surname,
            'PHONE': [{'VALUE': phone, 'VALUE_TYPE': 'WORK'}],
            'SOURCE_ID': '1',
            'UF_CRM_1729025812': '77',
            'UF_CRM_1727993574610': age,
            'UF_CRM_1729025891': '73',
            'UF_CRM_1729025908': city_com[0],
            'COMMENTS': city_com[1]
        }
    }
    response = requests.post(WEBHOOK_URL, json=lead_data)
    if response.status_code == 200:
        print("Лид успешно создан")
        return response.json()
    else:
        print("Ошибка при создании лида", response.status_code, response.text)
        return None


def create_lead(name, surname, phone, city, age):
    WEBHOOK_URL = config.bitrix_send_url
    city_com = check_city(city)
    lead_data = {
        'fields': {
            'TITLE': f'{name} {surname}|{phone}',
            'ADDRESS_REGION': [city],
            'NAME': name,
            'LAST_NAME': surname,
            'PHONE': [{'VALUE': phone, 'VALUE_TYPE': 'WORK'}],
            'SOURCE_ID': '3',
            'UF_CRM_1646838611': '26',
            'UF_CRM_1686315587161': age,
            'UF_CRM_1696427710938': '203',
            'UF_CRM_1708614342018': city_com[0],
            'COMMENTS': city_com[1]
        }
    }
    response = requests.post(WEBHOOK_URL, json=lead_data)
    if response.status_code == 200:
        print("Лид успешно создан")
        return response.json()
    else:
        print("Ошибка при создании лида", response.status_code, response.text)
        return None


def get_lead_fields():
    WEBHOOK_URL = config.bitrix_fields_test_url
    response = requests.get(WEBHOOK_URL)

    if response.status_code == 200:
        fields = response.json().get('result', {})
        for field, details in fields.items():
            print(f"Field ID: {field}, Field Name: {details['title']}")
    else:
        print("Ошибка при получении полей лида", response.status_code, response.text)

#get_lead_fields()

def get_new_lead_fields():
    response = requests.get(config.bitrix_fields_url)

    if response.status_code == 200:
        fields = response.json().get('result', {})
        for field_id, field_info in fields.items():
            print(f"Field ID: {field_id}, Field Name: {field_info['title']}, Type: {field_info['type']}")
    else:
        print("Ошибка при получении полей лида", response.status_code, response.text)



def get_lead_fields2(state):

    real_lead_custom_fields = ['UF_CRM_1646838611', 'UF_CRM_1696427710938', 'UF_CRM_1708614342018']
    test_lead_custom_fields = ['UF_CRM_1729025812', 'UF_CRM_1729025891', 'UF_CRM_1729025908']
    if state == 'real':
        temp = real_lead_custom_fields
        req = config.bitrix_fields_url
    else:
        temp = test_lead_custom_fields
        req = config.bitrix_fields_test_url

    response = requests.get(req)
    if response.status_code == 200:
        fields = response.json().get('result', {})
        for field_id, field_info in fields.items():
            if field_id in temp:
                print(
                    f"Field ID: {field_id}, Name: {field_info['title']}, Values: {field_info.get('items', 'No items')}")
    else:
        print("Ошибка при получении полей лида", response.status_code, response.text)


#get_lead_fields2('e')



def get_sources():
    params = {
        'filter[ENTITY_ID]': 'SOURCE'  # Корректная передача параметра фильтра
    }
    response = requests.get(config.bitrix_status_test_url, params=params)

    if response.status_code == 200:
        sources = response.json().get('result', [])
        for source in sources:
            print(f"ID: {source['STATUS_ID']}, Название: {source['NAME']}")
    else:
        print("Ошибка при получении списка источников", response.status_code, response.text)

#get_sources()
#create_test_lead('Илья', 'Волков', '+79155367642', 'мсква', '40')
#get_lead_fields()
#create_lead('Александр', 'Степанов', '+79564323453', 'Москва', '40')

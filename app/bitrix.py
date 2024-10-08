import requests
import config


def create_test_lead(name, surname, phone, city, age):
    WEBHOOK_URL = config.bitrix_send_test_url

    lead_data = {
        'fields': {
            'TITLE': f'{name} {surname}|{phone}',
            'ADDRESS_REGION': city,
            'NAME': name,
            'LAST_NAME': surname,
            'PHONE': [{'VALUE': phone, 'VALUE_TYPE': 'WORK'}],
            'SOURCE_ID': '1',
            #'UTM_SOURCE': '1',
            'UF_CRM_1727993499206': 'Входящий',
            'UF_CRM_1727993574610': age,
            'UF_CRM_1727993600142': 'Охранник',
            'UF_CRM_1727993646614': city
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

    lead_data = {
        'fields': {
            'TITLE': f'{name} {surname}|{phone}',
            'ADDRESS_REGION': city,
            'NAME': name,
            'LAST_NAME': surname,
            'PHONE': [{'VALUE': phone, 'VALUE_TYPE': 'WORK'}],
            'SOURCE_ID': '3',
            'UF_CRM_1646838611': 'Входящий',
            'UF_CRM_1686315587161': age,
            'UF_CRM_1696427710938': 'Охранник',
            'UF_CRM_1708614342018': city
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
    WEBHOOK_URL = config.bitrix_fields_url
    response = requests.get(WEBHOOK_URL)

    if response.status_code == 200:
        fields = response.json().get('result', {})
        for field, details in fields.items():
            print(f"Field ID: {field}, Field Name: {details['title']}")
    else:
        print("Ошибка при получении полей лида", response.status_code, response.text)


def get_sources():
    params = {
        'filter[ENTITY_ID]': 'SOURCE'  # Корректная передача параметра фильтра
    }
    response = requests.get(config.bitrix_status_url, params=params)

    if response.status_code == 200:
        sources = response.json().get('result', [])
        for source in sources:
            print(f"ID: {source['STATUS_ID']}, Название: {source['NAME']}")
    else:
        print("Ошибка при получении списка источников", response.status_code, response.text)

#get_sources()
#create_test_lead('Александр', 'Степанов', '+79564323453', 'Москва', '40')
#get_lead_fields()
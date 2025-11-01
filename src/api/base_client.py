import requests
from config import Config
from pathlib import Path


class YandexMarketApi():
    def __init__(self):
        self.__api_key = Config.API_KEY
        self.__business_id = Config.BUSINESS_ID
        self.__campaign_id = Config.CAMPAIGN_ID
        self.__base_url = 'https://api.partner.market.yandex.ru/v2'
        
        self.__session = requests.Session()
        self.__session.headers.update({
            'Api-key': self.__api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _make_request(self, method, endpoint, **kwargs):
        """Universal method for requsrts"""
        try:
            url = f'{self.__base_url}/{endpoint}'
            response = self.__session.request(method, url, **kwargs)
            if response.status_code != 200:
                print(f'HTTP ошибка: {response.status_code}: {response.text}')
                return None
            data = response.json()
            if data.get('status') == 'OK':
                return data
            else:
                if data.get('errors'):
                    for error in data.get('errors', []):
                        if isinstance(error, dict):
                            for code, message in error.items():
                                print(f'Ошибка API ЯМ - код: {code}, сообщение: {message}!')
                        else:
                            print(f'Ошибка API ЯМ: {error}!')
                else:
                    print('Неизвестная ошибка API')
                return None

        except Exception as e:
            print(f'HTTP Error: {e}')
            return None
    
    def generate_sales_report(self, dateFrom, dateTo, grouping="OFFERS"):
        params = {
            'businessId': self.__business_id,
            'dateFrom': dateFrom,
            'dateTo': dateTo,
            'grouping': grouping
        }
        response = self._make_request("POST", "reports/shows-sales/generate", json=params)
        if response:
            return response
        else:
            return None


    def wait_for_generation(self, method, endpoint, report_id):
        try:
            url = f'{self.__base_url}/{endpoint}/{report_id}'
            response = self.__session.request(method, url)
            if response.status_code != 200:
                print(f'HTTP ошибка: {response.status_code}: {response.text}')
                return None
            #TODO: логика ожидания генерации, проверки ошибок АПИ ЯМ
        except Exception as e:
            print(f'HTTP Error: {e}')



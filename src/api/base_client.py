import requests
import time
from config import Config
from pathlib import Path


class YandexMarketApi():
    def __init__(self, timeout=300, wait_between=30):
        self.__api_key = Config.API_KEY
        self.__business_id = Config.BUSINESS_ID
        self.__campaign_id = Config.CAMPAIGN_ID
        self.timeout = timeout
        self.wait_between = wait_between
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
    
    def generate_sales_report(self, dateFrom, dateTo, format='CSV', grouping='OFFERS'):
        payload = {
            'businessId': self.__business_id,
            'dateFrom': dateFrom,
            'dateTo': dateTo,
            'grouping': grouping
        }
        params = {'format': format}

        response = self._make_request("POST", "reports/shows-sales/generate",params=params, json=payload)
        if response:
            return response
        else:
            return None


    def wait_for_generation(self, report_id):
        try:
            data = self._make_request('GET',f'reports/info/{report_id}')
            if not data:
                print('Не удалось получить статус генерации отчета')
                return None
            result = data.get('result',{})
            if result.get('status') == 'DONE':
                if result.get('file'):
                    return result.get('file')
                else:
                    print('Генерация завершена, но ссылки еще нет')
                    return None
            elif result.get('status') == 'FAILED':
                if result.get('subStatus'):
                    print(f'Ошибка при генерации отчета {result.get('status')} {result.get("subStatus")}')
                    return None
                else:
                    print('Ошибка при генерации отчета')
                    return None
            elif result.get('status') == 'PENDING' or result.get('status') == 'PROCESSING':
                print('Отчет генерируется')
                return None
            else:
                print('Неизвестный статус генерации отчета')
                return None
        except Exception as e:
            print(f'HTTP Error: {e}')
            return None



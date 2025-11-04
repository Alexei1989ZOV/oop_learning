import requests
import time
from datetime import datetime
from config import Config
from pathlib import Path


class YandexMarketApi():
    def __init__(self, timeout=300, wait_between=30, data_directory='data'):
        self.__api_key = Config.API_KEY
        self.__business_id = Config.BUSINESS_ID
        self.__campaign_id = Config.CAMPAIGN_ID
        self.timeout = timeout
        self.wait_between = wait_between
        self.data_directory = data_directory
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
        start_time = time.time()
        attempts = 0

        while time.time() - start_time < self.timeout:
            attempts += 1
            try:
                data = self._make_request('GET',f'reports/info/{report_id}')
                if not data:
                    print('Не удалось получить статус генерации отчета')
                    time.sleep(self.wait_between)
                    continue
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
                    time.sleep(self.wait_between)
                else:
                    print('Неизвестный статус генерации отчета')
                    time.sleep(self.wait_between)
            except Exception as e:
                print(f'HTTP Error: {e}')
                return None
        print(f'Превышено время ожидания генерации отчета: {self.timeout} сек')
        return None

    def download(self, file_url, report_type):
        archive_path = Path(f'{self.data_directory}/raw/{report_type}')
        archive_name = f'{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip'
        target_file = archive_path / archive_name
        try:
            response = self.__session.get(file_url)
            if response.status_code == 200:
                archive_path.mkdir(parents=True, exist_ok=True)
                with open(target_file, 'wb') as f:
                    f.write(response.content)
                if target_file.stat().st_size == 0:
                    print("Файл пустой")
                    target_file.unlink()
                    return None
            else:
                print(f'Ошибка HTTP: {response.status_code}')
                return None
            print(f'Архив сохранен: {target_file}')
            return target_file
        except Exception as e:
            print(f'Ошибка при скачивании отчета! {e}')
            return None








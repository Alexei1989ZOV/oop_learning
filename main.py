from src.api.base_client import YandexMarketApi
from src.database.session import engine
from sqlalchemy.orm import Session
from src.database.models import SalesReport


api = YandexMarketApi()
# 1. Генерация и скачивание
resp = api.generate_sales_report('2025-10-11', '2025-11-05')
report_id = resp['result']['reportId']
file_url = api.wait_for_generation(report_id)
api.get_report(file_url, 'sales')  # скачивает и распаковывает

# 2. Загрузка в БД (отдельно)
api.process_csv_to_db('sales')

# with Session(engine) as session:
#     test = session.query(SalesReport).limit(10).all()
#     for item in test:
#         print(item)




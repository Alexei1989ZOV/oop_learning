from src.api.base_client import YandexMarketApi

obj = YandexMarketApi()
resp = obj.generate_sales_report('2025-10-10', '2025-10-10')
print(resp)



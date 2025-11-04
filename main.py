from src.api.base_client import YandexMarketApi


sales = YandexMarketApi()
resp = sales.generate_sales_report('2025-10-10', '2025-10-10')
report_id =  resp['result']['reportId']
link = sales.wait_for_generation(report_id)
if link:
    sales.get_report(link, 'sales_report')
else:
    print('Что-то пошло не так')




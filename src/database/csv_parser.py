import pandas as pd
from pathlib import Path
from typing import List
from .models import SalesReport
from .session import SessionLocal


class SalesReportCSVParser:

    @staticmethod
    def parse_csv_to_models(csv_path: Path) -> List[SalesReport]:
        try:
            df = pd.read_csv(csv_path, na_values=['', 'NULL', 'null'], keep_default_na=False)
            df = df.replace('', None)

            # Парсим дату из формата "10-10-2025"
            date_parts = df['DAY'].str.split('-', expand=True)
            df['DAY'] = date_parts[0]
            df['MONTH'] = date_parts[1]
            df['YEAR'] = pd.to_numeric(date_parts[2], errors='coerce')

            # Конвертируем числовые колонки
            numeric_columns = ['SHOWS', 'SHOWS_WITH_PROMOTION', 'CLICKS', 'CLICKS_WITH_PROMOTION',
                               'TO_CART', 'TO_CART_WITH_PROMOTION', 'ORDER_ITEMS', 'ORDER_ITEMS_WITH_PROMOTION',
                               'ORDER_ITEMS_TOTAL_AMOUNT', 'ORDER_ITEMS_TOTAL_AMOUNT_WITH_PROMOTION']

            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # Конвертируем float колонки
            float_columns = ['SHOWS_SHARE', 'TO_CART_CONVERSION', 'TO_CART_SHARE',
                             'TO_ORDER_CONVERSION', 'ORDER_ITEMS_SHARE']

            for col in float_columns:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.replace(',', '.')
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # Конвертируем в модели
            models = []
            for _, row in df.iterrows():
                clean_row = {k: (v if pd.notna(v) else None) for k, v in row.items()}
                models.append(SalesReport(**clean_row))

            print(f"✅ Загружено {len(models)} записей из CSV")
            return models

        except Exception as e:
            print(f"❌ Ошибка парсинга CSV: {e}")
            return []

    @staticmethod
    def save_to_database(csv_path: Path, batch_size: int = 1000):
        models = SalesReportCSVParser.parse_csv_to_models(csv_path)
        if not models:
            return

        db = SessionLocal()
        try:
            total = len(models)
            for i in range(0, total, batch_size):
                batch = models[i:i + batch_size]
                db.add_all(batch)
                db.commit()
                print(f"✅ Сохранено {min(i + batch_size, total)}/{total} записей")

            print(f"🎉 Всего загружено {total} записей в БД")
        except Exception as e:
            db.rollback()
            print(f"❌ Ошибка при сохранении в БД: {e}")
        finally:
            db.close()
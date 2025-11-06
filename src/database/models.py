from sqlalchemy import create_engine, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from typing import Optional


class Base(DeclarativeBase):
    pass


class SalesReport(Base):
    __tablename__ = 'sales_report'

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Дата и время
    DAY: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # День
    MONTH: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # Месяц
    YEAR: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Год
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  # Когда запись добавлена

    # Товар и категория
    CATEGORY_NAME: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Категория
    BRAND_NAME: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Бренд
    OFFER_ID: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # Ваш SKU
    OFFER_NAME: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Название товара

    # Показы
    BY_MSKU_SHOWS: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Показы товаров всех продавцов, шт.
    VISIBILITY_INDEX: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # Индекс видимости, %
    SHOWS: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Показы моих товаров, шт.
    SHOWS_WITH_PROMOTION: Mapped[Optional[int]] = mapped_column(Integer,
                                                                nullable=True)  # Показы моих товаров с акциями, шт.
    SHOWS_SHARE: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Доля показов с бустом, %

    # Клики
    CLICKS: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Клики по товарам, шт.
    CLICKS_WITH_PROMOTION: Mapped[Optional[int]] = mapped_column(Integer,
                                                                 nullable=True)  # Клики по товарам с акциями, шт.

    # Корзина
    TO_CART_CONVERSION: Mapped[Optional[float]] = mapped_column(Float,
                                                                nullable=True)  # Конверсия из показа в корзину, %
    TO_CART: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Добавления в корзину, шт.
    TO_CART_WITH_PROMOTION: Mapped[Optional[int]] = mapped_column(Integer,
                                                                  nullable=True)  # Добавления в корзину по акциям, шт.
    TO_CART_SHARE: Mapped[Optional[float]] = mapped_column(Float,
                                                           nullable=True)  # Доля добавлений товаров с бустом в корзину, %

    # Заказы
    ORDER_ITEMS: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Заказанные товары, шт.
    ORDER_ITEMS_WITH_PROMOTION: Mapped[Optional[int]] = mapped_column(Integer,
                                                                      nullable=True)  # Заказанные товары по акциям, шт.
    ORDER_ITEMS_TOTAL_AMOUNT: Mapped[Optional[int]] = mapped_column(Integer,
                                                                    nullable=True)  # Заказано товаров на сумму, ₽
    ORDER_ITEMS_TOTAL_AMOUNT_WITH_PROMOTION: Mapped[Optional[int]] = mapped_column(Integer,
                                                                                   nullable=True)  # Заказано товаров с акциями на сумму, ₽
    TO_ORDER_CONVERSION: Mapped[Optional[float]] = mapped_column(Float,
                                                                 nullable=True)  # Конверсия из корзины в заказ, %
    ORDER_ITEMS_SHARE: Mapped[Optional[float]] = mapped_column(Float,
                                                               nullable=True)  # Доля заказанных товаров с бустом, %

    # Доставки
    ORDER_ITEMS_DELIVERED_COUNT: Mapped[Optional[int]] = mapped_column(Integer,
                                                                       nullable=True)  # Доставлено за период, шт.
    ORDER_ITEMS_DELIVERED_COUNT_WITH_PROMOTION: Mapped[Optional[str]] = mapped_column(String(50),
                                                                                      nullable=True)  # Доставлено за период по акциям, шт.
    ORDER_ITEMS_DELIVERED_TOTAL_AMOUNT: Mapped[Optional[int]] = mapped_column(Integer,
                                                                              nullable=True)  # Доставлено за период на сумму, ₽
    ORDER_ITEMS_DELIVERED_TOTAL_AMOUNT_WITH_PROMOTION: Mapped[Optional[int]] = mapped_column(Integer,
                                                                                             nullable=True)  # Доставлено за период по акциям на сумму, ₽

    # Доставки из заказанных
    ORDER_ITEMS_DELIVERED_FROM_ORDERED_COUNT: Mapped[Optional[int]] = mapped_column(Integer,
                                                                                    nullable=True)  # Доставлено из заказанных за период, шт.
    ORDER_ITEMS_DELIVERED_FROM_ORDERED_TOTAL_AMOUNT: Mapped[Optional[int]] = mapped_column(Integer,
                                                                                           nullable=True)  # Доставлено из заказанных на сумму за период, ₽
    ORDER_ITEMS_DELIVERED_FROM_ORDERED_TOTAL_AMOUNT_WITH_PROMOTION: Mapped[Optional[int]] = mapped_column(Integer,
                                                                                                          nullable=True)  # Доставлено из заказанных на сумму за период по акциям, ₽

    # Отмены и возвраты
    ORDER_ITEMS_CANCELED_COUNT: Mapped[Optional[int]] = mapped_column(Integer,
                                                                      nullable=True)  # Отмены и невыкупы за период, шт.
    ORDER_ITEMS_CANCELED_BY_CREATED_AT_COUNT: Mapped[Optional[int]] = mapped_column(Integer,
                                                                                    nullable=True)  # Отмены и невыкупы заказанного за период, шт.
    ORDER_ITEMS_RETURNED_COUNT: Mapped[Optional[int]] = mapped_column(Integer,
                                                                      nullable=True)  # Возвращённые товары за период, шт.
    ORDER_ITEMS_RETURNED_BY_CREATED_AT_COUNT: Mapped[Optional[int]] = mapped_column(Integer,
                                                                                    nullable=True)  # Возвраты заказанного за период, шт.

    def __repr__(self):
        return f"<SalesReport(offer_id={self.OFFER_ID}, date={self.YEAR}-{self.MONTH}-{self.DAY}, amount={self.ORDER_ITEMS_TOTAL_AMOUNT})>"
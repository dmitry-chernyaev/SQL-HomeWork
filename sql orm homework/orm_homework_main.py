import sqlalchemy
from sqlalchemy.orm import sessionmaker
from orm_homework_models import create_tables, Publisher, Book, Stock, Shop, Sale
import json
from pprint import pprint

DSN = 'postgresql://postgres:jNdL_2269@localhost:5432/orm_homework'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', encoding='utf-8') as f:
    json_data = json.load(f)
    for data in json_data:
        # print(data)
        if data['model'] == 'publisher':
            publisher = Publisher(id=data['pk'], name=data['fields']['name'])
            session.add(publisher)

        elif data['model'] == 'book':
            book = Book(id=data['pk'], title=data['fields']['title'], id_publisher=data['fields']['id_publisher'])
            session.add(book)

        elif data['model'] == 'stock':
            stock = Stock(id=data['pk'], id_shop=data['fields']['id_shop'], id_book=data['fields']['id_book'], count=data['fields']['count'])
            session.add(stock)

        elif data['model'] == 'shop':
            shop = Shop(id=data['pk'], name=data['fields']['name'])
            session.add(shop)

        elif data['model'] == 'sale':
            sale = Sale(id=data['pk'], price=data['fields']['price'], date_sale=data['fields']['date_sale'], id_stock=data['fields']['id_stock'], count=data['fields']['count'])
            session.add(sale)


session.commit()
def sales_by_publisher(publisher_name):
    # Сначала находим издателя по имени
    publisher = session.query(Publisher).filter(
        Publisher.name.ilike(f"%{publisher_name}%")).first()

    if not publisher:
        print(f"Издатель '{publisher_name}' не найден")
        return

    sales = session.query(
        Book.title,
        Shop.name,
        Sale.price,
        Sale.date_sale
    ).join(
        Stock, Book.id == Stock.id_book
    ).join(
        Shop, Stock.id_shop == Shop.id
    ).join(
        Sale, Stock.id == Sale.id_stock  # Исправлено _id_stock на id_stock
    ).filter(
        Book.id_publisher == publisher.id  # Исправлено Pablisher на publisher
    ).order_by(
        Sale.date_sale
    ).all()

    if not sales:
        print(f"Для издателя '{publisher.name}' не найдено продаж")
        return

    # Красиво выводим результаты
    print(f"\nПродажи книг издателя '{publisher.name}':")
    print("-" * 80)
    print(f"{'Название книги':<40} | {'Магазин':<15} | {'Стоимость':<10} | {'Дата покупки'}")
    print("-" * 80)

    for title, shop_name, price, date in sales:
        print(
            f"{title:<40} | {shop_name:<15} | {price:<10} | {date.strftime('%Y-%m-%d %H:%M')}")



publisher_input = input('Введите название автора (издателя): ').strip()
sales_by_publisher(publisher_input)
session.close()
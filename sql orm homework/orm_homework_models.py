import sqlalchemy as sq
from sqlalchemy.cyextension.collections import unique_list
from sqlalchemy.orm import declarative_base, relationship

# ЗАДАНИЕ 1 ---------------------------------------------------------------------------------------

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, autoincrement=True, primary_key=True)
    name = sq.Column(sq.String(40), nullable=False)

    # Отношение "один ко многим" (у издателя много книг)
    books = relationship('Book', back_populates='publisher')


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, autoincrement=False, primary_key=True)
    title = sq.Column(sq.String(100), unique=True, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    # Отношение "многие к одному" (книга принадлежит одному издателю)
    publisher = relationship('Publisher', back_populates='books')

    # Отношение "один ко многим" (у книги может быть несколько записей в stock)
    stocks = relationship('Stock', back_populates='book')

class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, autoincrement=False, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'))
    count = sq.Column(sq.Integer)

    # Отношения "многие к одному" (запись stock относится к одной книге и одному магазину)
    book = relationship('Book', back_populates='stocks')
    shop = relationship('Shop', back_populates='stocks')

    # Отношение "многие к одному" (для одного магазина может быть много продаж)
    sales = relationship('Sale', back_populates='stock')

class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, autoincrement=False, primary_key=True)
    name = sq.Column(sq.String(100), unique=True, nullable=False)

    # Отношение "один ко многим" (в магазине может быть несколько записей в stock)
    stocks = relationship('Stock', back_populates='shop')

class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, autoincrement=False, primary_key=True)
    price = sq.Column(sq.String(20), nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'))
    count = sq.Column(sq.Integer)

    # Отношение "многие к одному" (для одного магазина может быть много продаж)
    stock = relationship('Stock', back_populates='sales')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

# КОНЕЦ ЗАДАНИЯ 1 ---------------------------------------------------------------------------------


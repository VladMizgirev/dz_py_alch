import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
import json

login = str(input('Введите логин:'))
password = str(input('Введите пароль:'))
name_bd = str(input('Введите название базы данных:'))
DSN = f'postgresql+psycopg2://{login}:{password}@localhost:5432/{name_bd}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

def load_db():
    with open ('База данных json.json', 'r', encoding='cp1251') as f:
        data = json.load(f)
    
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()

load_db()

def search(publisher):
    for pub in session.query(Publisher).filter(Publisher.name == publisher):
        for bo in session.query(Book).filter(Book.id_publisher == pub.id):
            for q in session.query(Stock).filter(Stock.id_book == bo.id):
                for sh in session.query(Shop).filter(Shop.id == q.id_shop):
                    for sa in session.query(Sale).filter(Sale.id_stock == q.id):
                        print(bo.title, sh.name, sa.price, sa.date_sale)

publisher = str(input())
search(publisher)

session.close()
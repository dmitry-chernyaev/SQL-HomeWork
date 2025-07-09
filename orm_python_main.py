import sqlalchemy
from sqlalchemy.orm import sessionmaker
from orm_python_models import create_tables, Client, Telephone

DCN = 'postgresql://postgres:jNdL_2269@localhost:5432/homework'
engine = sqlalchemy.create_engine(DCN)

create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()

client_1 = Client(first_name='Дмитрий', last_name='Черняев', email='dimitr_ch@mail.ru')
client_2 = Client(first_name='Сергей', last_name='Мешков', email='sergey.meshkov@mail.ru')
client_3 = Client(first_name='Александра', last_name='Пенькова', email='alexandra.penkova@mail.ru')

session.add(client_1)
session.add(client_2)
session.add(client_3)

session.flush()

telephone_1 = Telephone(tel_number='+7 927 264 22 69', client_id=client_1.client_id)
telephone_2 = Telephone(tel_number='+7 927 200 12 09', client_id=client_2.client_id)
telephone_3 = Telephone(tel_number='+7 927 600 00 12', client_id=3)

session.add_all([telephone_1, telephone_2, telephone_3])

session.commit()

# for client in session.query(Client).all():
#     print(client)

# for telephone in session.query(Telephone).all():
#     print(telephone)

# for telephone in session.query(Telephone).filter(Telephone.client_id > 2).all():
#     print(telephone)

# for client in session.query(Client).filter(Client.last_name.like('Пень%')).all():
#     print(client)


# объединение таблиц
# for client in session.query(Client).join(Telephone.clients).filter(Telephone.tel_number == '+7 927 264 22 69').all():
#     print(client)
# print(session.query(Client).join(Telephone.clients).filter(Telephone.tel_number == '+7 927 264 22 69').all())

# обновление данных
session.query(Client).filter(Client.last_name == 'Чернявин').update({'last_name': 'Черняев'})
session.query(Telephone).filter(Telephone.client_id == 2).delete()
session.query(Client).filter(Client.first_name == 'Сергей').delete()
session.commit()

session.close()




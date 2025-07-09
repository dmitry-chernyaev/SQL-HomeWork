import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()
#__________________________________________________________________________________________________
class Client(Base):
    __tablename__ = 'clients'

    client_id = sq.Column(sq.Integer, autoincrement=True, primary_key=True)
    first_name = sq.Column(sq.String(40), nullable=False)
    last_name = sq.Column(sq.String(40), nullable=False)
    email = sq.Column(sq.String(40))

    # telephones = relationship('Telephone', back_populates='clients')
    def __str__(self):
        return f'Клиент с id={self.client_id}: {self.first_name} {self.last_name}'
#__________________________________________________________________________________________________
class Telephone(Base):
    __tablename__ = 'telephones'

    tel_id = sq.Column(sq.Integer, autoincrement=True, primary_key=True)
    tel_number = sq.Column(sq.String(40))
    client_id = sq.Column(sq.Integer, sq.ForeignKey('clients.client_id'), nullable=False)

    # clients = relationship('Client', back_populates='telephones')
    clients = relationship('Client', backref='telephones')

    def __str__(self):
        return f'Клиент с id={self.client_id} имеет телефонный номер {self.tel_number}'
#__________________________________________________________________________________________________
def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


#__________________________________________________________________________________________________
# переопределяем метод str


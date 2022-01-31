import config

import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship


db = f'postgresql://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'
engine = sqlalchemy.create_engine(db, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    goods = relationship("Goods", back_populates="user")

    print('good')
    def __repr__(self):
        return "<User(name='%s')>" % (self.name)

class Goods(Base):
    __tablename__ = 'goods'
    id = Column(Integer, primary_key=True)
    link = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="goods")

Base.metadata.create_all(engine)
import config
import sqlite3
import sqlalchemy.dialects.sqlite
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Float
from sqlalchemy.orm import sessionmaker, relationship
import os


# db = f'postgresql://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'
db = f'sqlite:///{os.getcwd()}/DB/database.db'
engine = sqlalchemy.create_engine(db, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    goods = relationship("Goods", back_populates="user")

    print('good')
    def __repr__(self):
        return "<User(name='%s')>" % (self.name)

class Goods(Base):
    __tablename__ = 'goods'
    id = Column(Integer, primary_key=True)
    link = Column(String)
    user_id = Column(BigInteger, ForeignKey('user.id'))
    user = relationship("User", back_populates="goods")
    price = Column(Float, nullable=False)

Base.metadata.create_all(engine)
# Base.metadata.drop_all(bind=engine, tables=[User.__table__, Goods.__table__] )
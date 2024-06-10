import re
from datetime import datetime

from sqlalchemy import (create_engine, Column, Integer, String, text, DateTime,
                        ForeignKey, Boolean, Table, func, Text, Float)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from config import Config


# 创建基类
Base = declarative_base()


# 设置数据库引擎
engine = create_engine(Config.get_database_uri())

# 设置会话
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


product_topic_association = Table('product_topic_association', Base.metadata,
    Column('product_id', Integer, ForeignKey('product.id')),
    Column('topic_id', Integer, ForeignKey('topic.id'))
)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    products = relationship('Product', back_populates='category')


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    url = Column(String(200), nullable=False)
    description = Column(String(200))
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    added_time = Column(DateTime,  default=func.now())
    topics = relationship('Topic', secondary=product_topic_association, back_populates='products')
    category = relationship('Category', back_populates='products')


class Topic(Base):
    __tablename__ = 'topic'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True, nullable=False)
    products = relationship('Product', secondary=product_topic_association, back_populates='topics')


def init_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
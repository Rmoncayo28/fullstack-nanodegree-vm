import sys
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'
    name = Column(
        String(80), nullable=False
    )
    id = Column(
        Integer, primary_key=True
    )


class Item(Base):
    __tablename__ = 'item'
    name = Column(
        String(80), nullable=False
    )
    id = Column(
        Integer, primary_key=True
    )
    category_id = Column(
        Integer, ForeignKey('category.id')
    )
    description = Column(
        String(250)
    )
    category = relationship(Category)


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)

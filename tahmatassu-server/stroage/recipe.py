from sqlalchemy import create_engine


from sqlalchemy.orm import mapper

from sqlalchemy import Column, String, Integer, Date, Numeric


engine = create_engine('postgresql://postgres:postgres@localhost:5432/') 

class Base:
  pass


class Recipe(Base):
    __tablename__ = 'recipes'
    id=Column(Integer, primary_key=True)
    name=Column('name', String(32))
    markdown=Column('markdown', String(100000))
    created=Column('quantity', Integer)
    updated=Column('price', Numeric)
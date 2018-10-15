from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
notherCat = Category(name="Movies")
# myFirstCategory = session.query(Category).all()[0]
# sport = Item(description="soccer team in madrid", name="madrid", category=myFirstCategory)
# sport2 = Item(description="soccer team in liverpool", name="liverpool", category=myFirstCategory)
# sport3 = Item(description="soccer team in manchester", name="manchester united", category=myFirstCategory)
# sport4 = Item(description="soccer team in brighton", name="brighton hove & albion", category=myFirstCategory)
# # session.add(myFirstCategory)
# session.add(sport)
# session.add(sport2)
# session.add(sport3)
# session.add(sport4)
session.add(notherCat)
session.commit()

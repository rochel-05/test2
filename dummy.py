import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table import *

engine = create_engine('sqlite:///usersDb.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User("admin","root")
session.add(user)

user = User("nantenaina","nantenaina201905")
session.add(user)

user = User("flask","flask2019")
session.add(user)

# commit the record the database
session.commit()

session.commit()
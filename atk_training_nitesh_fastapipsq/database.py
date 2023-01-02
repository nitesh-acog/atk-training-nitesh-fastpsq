# get all your database configurations ready in this module
# giving a command the database should be able to connect to any database with proper authentication
# ORM (Object relational Mapping)
# Queruing and manipulating table using object oriented paradigm
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# for any remote database connection
# proceed with the this format
#create_engine('postgres://username:password@localhost:1111/database')

Engine=create_engine('sqlite:///./queue.db',connect_args={'check_same_thread': False})
Base= declarative_base()
local_session=sessionmaker(bind=Engine,autocommit=False,autoflush=False)




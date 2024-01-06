from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import InnerPost
import dotenv
import os

dotenv.load_dotenv()

Base = declarative_base()

def create_session(inner = False):
    connection_string = os.getenv("DATABASE_URL")
    if inner:
        connection_string = 'sqlite:///main.db'
    engine = create_engine(connection_string, echo=True)
    if inner:
        InnerPost.__table__.create(bind=engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
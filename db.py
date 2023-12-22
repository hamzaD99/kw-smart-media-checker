from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv
import os

dotenv.load_dotenv()

Base = declarative_base()

def create_session(inner = False):
    connection_string = os.getenv("DATABASE_URL")
    if inner:
        connection_string = 'sqlite:///main.db'
    engine = create_engine(connection_string, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
def close_session(session):
    session.commit()
    session.close()
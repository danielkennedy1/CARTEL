from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

engine = create_engine("sqlite:///cartel.db", echo=True)
Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):

        self.name = name


def create_db(reset=False):
    if reset:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


create_db(reset=True)

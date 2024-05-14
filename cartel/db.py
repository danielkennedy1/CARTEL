from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///cartel.db", echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    public_key = Column(String)
    password_hash = Column(String)

    def __init__(self, name, public_key, password_hash):

        self.name = name
        self.public_key = public_key
        self.password_hash = password_hash

    __table_args__ = (UniqueConstraint("name"),)


class Message(Base):

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    sender = Column(Integer, ForeignKey("users.id"))
    recipient = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    signature = Column(String)
    passkey = Column(String)

    def __init__(self, sender, recipient, message, signature, passkey):

        self.sender = sender
        self.recipient = recipient
        self.message = message
        self.signature = signature
        self.passkey = passkey


def create_db(reset=False):
    if reset:
        print("Dropping all tables")
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

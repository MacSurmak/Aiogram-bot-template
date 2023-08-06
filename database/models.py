from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger

from database.base import Base


class User(Base):
    __tablename__ = 'Users'

    user_id: Column = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    connection_date: Column = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return self.user_id


class Key(Base):
    __tablename__ = 'Keys'

    id: Column = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    creation_date: Column = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return self.user_id

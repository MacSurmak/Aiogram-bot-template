from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger, Boolean

from database.base import Base


class User(Base):
    __tablename__ = 'Users'

    user_id: Column = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    connection_date: Column = Column(DateTime, default=datetime.now, nullable=False)
    username: Column = Column(String, default="None", nullable=False)
    name: Column = Column(String, default="None", nullable=False)
    receive_mail: Column = Column(Boolean, default=False, nullable=False)
    old_message: Column = Column(Integer, nullable=True)

    def __repr__(self):
        return self.user_id


# class Mail(Base):
#     __tablename__ = 'Mail'
#
#     id: Column = Column(Integer, primary_key=True, unique=True, autoincrement=True)
#     mail_id: Column = Column(Integer, nullable=False)
#     sent: Column = Column(Boolean, default=False, nullable=False)
#
#     def __repr__(self):
#         return self.id

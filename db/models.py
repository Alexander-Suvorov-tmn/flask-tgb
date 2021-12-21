import datetime
from .connected import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class Botkey(Base):
    __tablename__ = 'botkey'

    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=datetime.datetime.now())
    updated_on = Column(DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    is_removed = Column(Boolean, default=False)
    first_name = Column(String(255), nullable=False)
    second_name = Column(String(255), nullable=False)
    telegram_id = Column(Integer, nullable=False)
    key = Column(Integer, nullable=False)
    is_dissmissed = Column(Boolean, default=False)

    def __init__(self, first_name, second_name, telegram_id, key):
        self.first_name = first_name
        self.second_name = second_name
        self.telegram_id = telegram_id
        self.key = key

    def __repr__(self):
        return f"{self.id}: {self.first_name} {self.second_name}"

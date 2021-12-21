from sqlalchemy.sql.expression import table
from .connected import sess

from . import models


class TableWrapper:
    def __init__(self, table):
        self.table = table

    @property
    def keys(self):
        return [str(item).split('.')[-1] for item in self.table.__table__.columns]

    def _print_row(self, row):
        for key in self.keys:
            print(getattr(row, key), end=' | ')
        print()

    def put(self, data):
        sess.add(self.table(**data))
        sess.commit()

    def delete(self, id, val):
        sess.query(self.table).filter(getattr(self.table, id) == val).delete()
        sess.commit()

    def update(self, id, key):
        sess.query(self.table).filter(getattr(self.table, id) == id).update({key: key})
        sess.commit()

    def create(self, data):
        create = self.table(
            first_name=data['first_name'],
            second_name=data['second_name'],
            telegram_id=data['telegram_id'],
            key=data['key'],
        )
        sess.add(create)
        sess.commit()

    def creation_key(self, id, data):
        user = self.table.key_get(id)
        if user:
            self.table.update(id, data)
        else:
            self.table.create(id, data)

    def get(self, id, val):
        return sess.query(self.table).filter((self.table, id) == val).first()

    def _get_all(self):
        return sess.query(self.table).all()


class DataBase:
    t = {}

    def __init__(self):
        for attr_desc in dir(models):
            attr = getattr(models, attr_desc)
            if hasattr(attr, '__tablename__'):
                self.t[attr.__tablename__] = attr

    def __getattr__(self, attr):
        if attr in self.t:
            return TableWrapper(self.t[attr])
        else:
            raise AttributeError(f'Таблицы {attr} в базе данных не существует')

    @property
    def tables(self):
        return list(self.t.keys())
from curr_conv import db
from sqlalchemy.orm import validates
from dateutil.parser import parse
import datetime


class Order(db.Model):
    __tablename__ = "order_table"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, unique=True)
    usd = db.Column(db.Float)
    time = db.Column(db.Date)
    rub = db.Column(db.Float)

    @validates('order_id')
    def validate_order_id(self, key, value):
        if not value.isnumeric():
            return None
        else:
            return value

    @validates('usd')
    def validate_usd(self, key, value):
        if not value.isnumeric():
            return None
        else:
            return value

    @validates('time')
    def validate_time(self, key, value):
        try:
            day, month, year = value.split('.')
            datetime.datetime(int(year), int(month), int(day))
            return value
        except Exception:
            return None

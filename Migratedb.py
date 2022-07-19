from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from curr_conv.Config import config

app = Flask(__name__)
# укажите ваши авторизационные данные и имя database
app.config.from_object(config)
db = SQLAlchemy(app)
manage = Manager(app)
Migrate(app, db)
manage.add_command('db', MigrateCommand)


class Order(db.Model):
    __tablename__ = "order_table"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, unique=True)
    usd = db.Column(db.Float)
    time = db.Column(db.Date)
    rub = db.Column(db.Float)


if __name__ == '__main__':
    manage.run()

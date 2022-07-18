from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
# укажите ваши авторизационные данные и имя database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/orders'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manage = Manager(app)
Migrate(app, db)
manage.add_command('db', MigrateCommand)


class Order(db.Model):
    __tablename__ = "ordertable"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, unique=True)
    usd = db.Column(db.Float)
    time = db.Column(db.Date)
    rub = db.Column(db.Float)


if __name__ == '__main__':
    manage.run()

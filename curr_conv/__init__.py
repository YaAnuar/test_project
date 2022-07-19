from flask import Flask, Blueprint
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from curr_conv.Config import config

app = Flask(__name__)
CORS(app)
app.config.from_object(config)
db = SQLAlchemy(app)
ma = Marshmallow()
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')

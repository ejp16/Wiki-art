from flask import Flask
from routes.arts import arts
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.register_blueprint(arts)

app.secret_key = "chocolate"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/task'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = 'static/images/'


SQLAlchemy(app)


from flask import Flask
from db import db
from flask_login import LoginManager
import os
from jinja2 import ChoiceLoader, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.jinja_loader = ChoiceLoader([
    FileSystemLoader(os.path.join(BASE_DIR, 'templates')),
    FileSystemLoader(os.path.join(BASE_DIR, '..', 'frontend'))
])
app.secret_key = 'RotaDoFeirante'
lm = LoginManager(app)
lm.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dados.db"
db.init_app(app)

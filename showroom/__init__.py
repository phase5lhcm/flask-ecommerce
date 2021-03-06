from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from flask_wtf.csrf import CSRFProtect
# from flask_session import Session

app = Flask(__name__)
SESSION_TYPE = "filesystem"
db = SQLAlchemy(app)
# csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SECRET_KEY'] = 'dac006798475eab19b3a7901'
app.config.from_object(__name__)
# Session(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from showroom import routes
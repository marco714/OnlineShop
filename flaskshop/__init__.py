from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_session import Session
from flask_mail import Mail
from os import environ

# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd58f9c32c7e1cf3d8264765f31e54f73'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onlineshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = "filesystem"

app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = environ.get('EMAIL_PASS')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
Session(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'You Need To Log In To Access This Page!'
from flaskshop import routes

# migrate = Migrate(app, db)
# manager = Manager(app)

# manager.add_command('db', MigrateCommand)
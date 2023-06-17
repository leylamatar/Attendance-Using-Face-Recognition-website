from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
    
app= Flask(__name__)

#create database
db = SQLAlchemy()
bcrypt = Bcrypt(app)
DB_NAME = "database.db"
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['SECRET_KEY'] = '746fjghk87thfk9595jdld8r9r9'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

db.init_app(app)
@app.before_first_request
def create_tables():
    db.create_all()

   


from website import routes    
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)

#create database
db = SQLAlchemy()
DB_NAME = "database.db"
app.config['SECRET_KEY'] = '746fjghk87thfk9595jdld8r9r9'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)
with app.app_context():
        db.create_all()

   


from website import routes        
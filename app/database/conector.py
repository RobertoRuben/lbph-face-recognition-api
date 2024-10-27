from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 

db = SQLAlchemy()
ma = Marshmallow()

class DatabaseConector:
    def __init__(self, app: Flask):
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:contraseña@host:puerto/db_namw'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

        db.init_app(self.app)
        ma.init_app(self.app)

    def get_db(self):
        return db

    def get_ma(self):
        return ma

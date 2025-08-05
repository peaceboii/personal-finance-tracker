from flask_login import UserMixin
from datetime import datetime

from app import db

class User(db.Model,UserMixin):
    __tablename__='users'

    id = db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)
    role = db.Column(db.String)
    description = db.Column(db.String)

    budget = db.relationship('Budget', backref='user', uselist=False)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def get_id(self):
        return (self.id)

class Budget(db.Model):
    __tablename__='budget'

    bid = db.Column(db.Integer,primary_key=True)
    amount = db.Column(db.Float,nullable=False)
    month = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Transaction(db.Model):
    __tablename__='transaction'

    tid = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String)
    amount= db.Column(db.Float)
    description =db.Column(db.String)
    timestamp = db.Column(db.DateTime,default = datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

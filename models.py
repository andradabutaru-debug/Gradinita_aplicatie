from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Educator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Copil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100), nullable=False)

class Parinte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    copil_id = db.Column(db.Integer, db.ForeignKey('copil.id'))

class Meniu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    mic_dejun = db.Column(db.String(200))
    pranz = db.Column(db.String(200))
    gustare = db.Column(db.String(200))

class ConsumatieCopil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    copil_id = db.Column(db.Integer, db.ForeignKey('copil.id'))
    meniu_id = db.Column(db.Integer, db.ForeignKey('meniu.id'))
    a_mancat_mic_dejun = db.Column(db.Integer, default=0)   # procent
    a_mancat_pranz = db.Column(db.Integer, default=0)
    a_mancat_gustare = db.Column(db.Integer, default=0)
    lipseste = db.Column(db.Boolean, default=False)


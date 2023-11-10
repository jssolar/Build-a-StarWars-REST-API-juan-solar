from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "username": self.username
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_character = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    user_planet = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    user = db.relationship(User)

    def to_dict(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "user_character": self.user_character,
            "user_planet": self.user_planet
        }
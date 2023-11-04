from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
  
    favoritoPlanets = db.relationship("FavoritoPlanets", backref="user")

    favoritoPeoples = db.relationship("FavoritoPeoples", backref="user")

    def __repr__(self):
        return f"User with email {self.email} and id {self.id}"

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    terrain = db.Column(db.String(50), unique=False, nullable=False)
    rotation_period = db.Column(db.Integer, unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    favoritoPlanets = db.relationship("FavoritoPlanets", backref="planets")
    def __repr__(self):
        return f"Planet {self.name} with ID {self.id}"
    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "terrain": self.terrain,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter
        }
class FavoritoPlanets(db.Model):
    __tablename__ = "favoritoPlanets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planets_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    def __repr__(self):
        return '<FavoritoPlanets %r>' % self.id
    def serialize(self):
        return {
            "planets": self.planets.serialize(),
        }

class FavoritoPeoples(db.Model):
    __tablename__ = "favoritoPeoles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    peoples_id = db.Column(db.Integer, db.ForeignKey("peoples.id"))
    def __repr__(self):
        return '<FavoritoPeoples %r>' % self.id
    def serialize(self):
        return {
            "peoples": self.peoples.serialize()
        }
    
class Peoples(db.Model):
    __tablename__ = 'peoples'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    hair_color = db.Column(db.String(50), unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    mass = db.Column(db.Integer, unique=False, nullable=False)
    favoritoPeoples = db.relationship("FavoritoPeoples", backref="peoples")
    def __repr__(self):
        return f"Peoples {self.name} with ID {self.id}"
    def serialize(self):
        return {
            "id" : self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass
        }


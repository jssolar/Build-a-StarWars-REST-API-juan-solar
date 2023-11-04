"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Peoples,FavoritoPeoples,FavoritoPlanets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route("/people", methods= ['GET'])
def get_all_people():
    people = Peoples.query.all()
    people_serialized = list(map(lambda x: x.serialize(), people))
    return jsonify({"msg": "Completed", "people": people_serialized})


@app.route('/people/<int:people_id>', methods=['GET'])
def handle_people(people_id):
    single_people = Peoples.query.get(people_id)
    if single_people is None:
       raise APIException(f"No existe la persona con el ID {people_id}", status_code=400)
    
    response_body = {
        "msg": "Hello, this is your GET /people response ",
        "people_id": people_id,
        "people_info": single_people.serialize()
    }

    return jsonify(response_body), 200


@app.route("/planets", methods= ['GET'])
def get_all_planets():
    planets = Planets.query.all()
    planets_serialized = list(map(lambda x: x.serialize(), planets))
    return jsonify({"msg": "Completed", "planets": planets_serialized})


@app.route('/planets/<int:planets_id>', methods=['GET'])
def handle_planets(planets_id):
    single_planets = Planets.query.get(planets_id)
    if single_planets is None:
       raise APIException(f"No existe la persona con el ID {planets_id}", status_code=400)
    
    response_body = {
        "msg": "Hello, this is your GET /planets response ",
        "planets_id": planets_id,
        "planets_info": single_planets.serialize()
    }

    return jsonify(response_body), 200

@app.route("/users", methods= ['GET'])
def get_all_users():
    users = User.query.all()
    users_serialized = list(map(lambda x: x.serialize(), users))
    return jsonify({"msg": "Completed", "users": users_serialized})


@app.route('/users/<int:users_id>', methods=['GET'])
def handle_users(users_id):
    single_users = User.query.get(users_id)
    if single_users is None:
       raise APIException(f"No existe la persona con el ID {users_id}", status_code=400)
    
    response_body = {
        "msg": "Hello, this is your GET /users response ",
        "users_id": users_id,
        "users_info": single_users.serialize()
    }

    return jsonify(response_body), 200

@app.route('/users/favorites/<int:users_id>', methods=['GET'])
def user_favotites(users_id):

    planet_favorite = FavoritoPlanets.query.filter_by(user_id = users_id)
    planet = [planets.serialize() for planets in planet_favorite]

    people_favorite = FavoritoPeoples.query.filter_by(user_id = users_id)
    people = [peoples.serialize() for peoples in people_favorite]

    return jsonify("Favorites", planet, people ), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
    select_planet= Planets.query.get(planet_id)
    body =  request.json
    id_user = body.get("id_user")
    actual_user = User.query.get(id_user)

    favorito_planet = FavoritoPlanets(
        user = actual_user,
        planets = select_planet
    )

    try:
        db.session.add(favorito_planet)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "ERROR INTERNO",
            "error": error.args
        })
    return jsonify({}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    delete_planet = FavoritoPlanets.query.get(planet_id)
    try:
        db.session.delete(delete_planet)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "ERROR INTERNO",
            "error": error.args
        })
    return jsonify({}), 200

@app.route('/favorite/people/<int:peoples_id>', methods=['POST'])
def add_fav_people(peoples_id):
    select_people = Peoples.query.get(peoples_id)
    body = request.json
    id_user = body.get("id_user")
    actual_user = User. query.get(id_user)

    favorito_people = FavoritoPeoples(
        user = actual_user,
        peoples = select_people
    )
    try:
        db.session.add(favorito_people)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "ERROR INTERNO",
            "error": error.args
        })
    return jsonify({}), 200

@app.route('/favorite/people/<int:peoples_id>', methods=['DELETE'])
def delete_fav_people(peoples_id):
    delete_people = FavoritoPeoples.query.get(peoples_id)
    try:
        db.session.delete(delete_people)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "ERROR INTERNO",
            "error": error.args
        })
    return jsonify({}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
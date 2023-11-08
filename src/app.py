"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
# from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite 

app = Flask(__name__)

app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
    
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
MIGRATE = Migrate(app, db)
db.init_app(app)


CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')

def sitemap():
    return generate_sitemap(app)




# @app.route("/api/people", methods= ['GET'])
# def get_all_people():
#     people = People.query.all()
#     people_serialized = list(map(lambda x: x.serialize(), people))
#     return jsonify({"msg": "Hola, Gente!!!", "people": people_serialized})


# @app.route('/api/people/<int:people_id>', methods=['GET'])
# def handle_people(people_id):
#     single_people = People.query.get(people_id)
#     if single_people is None:
#        raise APIException(f"No existe la persona con el ID {people_id}", status_code=400)
    
#     response_body = {
#         "msg": "Hello, this is your GET /people response ",
#         "people_id": people_id,
#         "people_info": single_people.serialize()
#     }

#     return jsonify(response_body), 200


# @app.route("/api/planets", methods= ['GET'])
# def get_all_planets():
#     planets = Planet.query.all()
#     planets_serialized = list(map(lambda x: x.serialize(), planets))
#     return jsonify({"msg": "Completed", "planets": planets_serialized})


# @app.route('/api/planets/<int:planets_id>', methods=['GET'])
# def handle_planets(planets_id):
#     single_planets = Planet.query.get(planets_id)
#     if single_planets is None:
#        raise APIException(f"No existe la persona con el ID {planets_id}", status_code=400)
    
#     response_body = {
#         "msg": "Hello, this is your GET /planets response ",
#         "planets_id": planets_id,
#         "planets_info": single_planets.serialize()
#     }

#     return jsonify(response_body), 200



# #-----< todos los usuarios >--------------------------------------------------------->
# @app.route("/api/users", methods= ['GET'])
# def get_all_users():
#     users = User.query.all()
#     users_serialized = list(map(lambda usuarios: usuarios.serialize(), users))
#     return jsonify({"msg": "Todos los Usuarios!!", "users": users_serialized})


# #-----< un usuario >--------------------------------------------------------->
# @app.route('/api/users/<int:users_id>', methods=['GET'])
# def handle_users(users_id):
#     single_users = User.query.get(users_id)
#     if single_users is None:
#        raise APIException(f"No existe el user con el ID {users_id}", status_code=400)
    
#     response_body = {
#         "msg": "Hola, user! ",
#         "users_id": users_id,
#         "users_info": single_users.serialize()
#     }

#     return jsonify(response_body), 200

# #-----< todos los favoritos de un  usuario >--------------------------------------------------------->
# @app.route('/api/users/favorites/<int:users_id>', methods=['GET'])
# def user_favotites(users_id):

#     planet_favorite = Favorite_planet.query.filter_by(user_id = users_id)
#     planet = [planets.serialize() for planets in planet_favorite]

#     people_favorite = Favorite_people.query.filter_by(user_id = users_id)
#     people = [people.serialize() for people in people_favorite]

#     return jsonify(" Todos los Favoritos", planet, people ), 200


# #-----< agregar un planeta a un usuario >--------------------------------------------------------->
# # @app.route('/api/favorite/planet/<int:planet_id>', methods=['POST'])
# @app.route('/api/favorite/planet/<int:planet_id>', method=['POST'])
# def add_planet_to_favorite(planet_id):
#     # print('add_planet_to_favorite')
#     try:
#       data = request.json
#       new_favorite_planet = Favorite_planet(data["name"], data["description"])
#       db.session.add(new_favorite_planet)
#       db.session.commit()
#       return jsonify({'message': 'Planeta Agregado al Favorito!'}), 201
#     except Exception as e:
#       return {"error": str(e)}, 500
  

  




# # def add_fav_planet(planet_id):
    
# #     select_planet= Planet.query.get(planet_id)
# #     body =  request.get_json()
# #     user_id = body.get_json(user_id)
# #     actual_user = User.query.get(user_id)

# #     favorite_planet = Favorite_planet(
# #         user = actual_user,
# #         planets = select_planet
# #     )

# #     try:
# #         db.session.add(favorite_planet)
# #         db.session.commit()
# #     except Exception as error:
# #         db.session.rollback()
# #         return jsonify({
# #             "message": "ERROR INTERNO",
# #             "error": error.args
# #         })
# #     return jsonify({}), 200

# #-----< eliminar planeta de un usuario >--------------------------------------------------------->

# @app.route('/api/favorite/planet/<int:planet_id>', methods=['DELETE'])
# def delete_fav_planet(planet_id):
#     delete_planet = Favorite_planet.query.get(planet_id)
#     try:
#         db.session.delete(delete_planet)
#         db.session.commit()
#     except Exception as error:
#         db.session.rollback()
#         return jsonify({
#             "message": "ERROR INTERNO",
#             "error": error.args
#         })
#     return jsonify({}), 200

# #-----< agregar un personaje-favorito de un usuario >--------------------------------------------------------->

# @app.route('/api/favorite/people/<int:people_id>', methods=['POST'])
# def add_fav_people(people_id):
#     select_people = People.query.get(people_id)
#     body =  request.get_json()
#     id_user = body.get("id_user")
#     actual_user = User. query.get(id_user)

#     favorite_people = Favorite_people(
#         user = actual_user,
#         peoples = select_people
#     )
#     try:
#         db.session.add(favorite_people)
#         db.session.commit()
#     except Exception as error:
#         db.session.rollback()
#         return jsonify({
#             "message": "ERROR INTERNO",
#             "error": error.args
#         })
#     return jsonify({}), 200


# #-----< eliminar un personaje-favorito de un usuario >--------------------------------------------------------->
# @app.route('/api/favorite/people/<int:people_id>', methods=['DELETE'])
# def delete_fav_people(people_id):
#     delete_people = Favorite_people.query.get(people_id)
#     try:
#         db.session.delete(delete_people)
#         db.session.commit()
#     except Exception as error:
#         db.session.rollback()
#         return jsonify({
#             "message": "ERROR INTERNO",
#             "error": error.args
#         })
#     return jsonify({}), 200

@app.route('/user', methods=['GET', "POST"])
def handle_user():
    if request.method == 'GET':
        users = User.query.all()
        users = list(map(lambda user: user.to_dict(), users))

        return jsonify({
            "data": users
        }), 200
    elif request.method == 'POST':
        user = User()
        data = request.get_json()
        user.name = data["name"]
        user.username = data["username"]
        user.password = data["password"]

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "msg": "user created"
        }), 200

@app.route("/user/<int:id>", methods=["GET","PUT", "DELETE"])
def update_user(id):
    if request.method == 'GET':
        user_id = id
        user = User.query.get(id)
        data = user.to_dict()

        return data, 200
    elif request.method == 'PUT':
        user = User.query.get(id)
        if user is not None:
            data = request.get_json()
            user.name = data["name"]
            user.username = data["username"]
            db.session.commit()
            return jsonify({
                "msg":"user updated"
            }),200
        else:
            return jsonify({
                "msg": "user not found"
            }), 404
    elif request.method == 'DELETE':
        user = User.query.get(id)
        if user is not None:
            db.session.delete(user)
            db.session.commit()

            return jsonify({
                "msg":"user deleted"
            }),202
        else:
            return jsonify({
                "msg":"user not found"
            }), 404

@app.route('/character', methods=['GET', "POST"])
def handle_character():
    if request.method == 'GET':
        characters = Character.query.all()
        characters = list(map(lambda character: character.to_dict(), characters))

        return jsonify({
            "data": characters
        }), 200
    elif request.method == 'POST':
        character = Character()
        data = request.get_json()
        character.name = data["name"]

        db.session.add(character)
        db.session.commit()

        return jsonify({
            "msg": "character created"
        }), 200

@app.route("/character/<int:id>", methods=["PUT", "DELETE"])
def update_character(id):
    if request.method == 'PUT':
        character = Character.query.get(id)
        if character is not None:
            data = request.get_json()
            character.name = data["name"]
            db.session.commit()
            return jsonify({
                "msg":"character updated"
            }),200
        else:
            return jsonify({
                "msg": "character not found"
            }), 404
    elif request.method == 'DELETE':
        character = Character.query.get(id)
        if character is not None:
            db.session.delete(character)
            db.session.commit()

            return jsonify({
                "msg":"character deleted"
            }),202
        else:
            return jsonify({
                "msg":"character not found"
            }), 404

@app.route('/planet', methods=['GET', "POST"])
def handle_planet():
    if request.method == 'GET':
        planets = Planet.query.all()
        planets = list(map(lambda planet: planet.to_dict(), planets))

        return jsonify({
            "data": planets
        }), 200
    elif request.method == 'POST':
        planet = Planet()
        data = request.get_json()
        planet.name = data["name"]

        db.session.add(planet)
        db.session.commit()

        return jsonify({
            "msg": "planet created"
        }), 200

@app.route("/planet/<int:id>", methods=["PUT", "DELETE"])
def update_planet(id):
    if request.method == 'PUT':
        planet = Planet.query.get(id)
        if planet is not None:
            data = request.get_json()
            planet.name = data["name"]
            db.session.commit()
            return jsonify({
                "msg":"planet updated"
            }),200
        else:
            return jsonify({
                "msg": "planet not found"
            }), 404
    elif request.method == 'DELETE':
        planet = Planet.query.get(id)
        if planet is not None:
            db.session.delete(planet)
            db.session.commit()

            return jsonify({
                "msg":"planet deleted"
            }),202
        else:
            return jsonify({
                "msg":"planet not found"
            }), 404

@app.route('/user/<int:id>/favorite', methods=['GET'])
def handle_favorite(id):
    user_id = id
    favorites = Favorite.query.filter_by(user_id=user_id)
    favorites = list(map(lambda favorite: favorite.to_dict(), favorites))

    return jsonify({
        "data": favorites
    }), 200
    
@app.route('/favorite', methods=["POST"])
def create_favorite():
    favorite = Favorite()
    data = request.get_json()
    user_id = data["user_id"]
    if data["character_id"] is None:
        character_id = "0"
    character_id = data["character_id"]
    if data["planet_id"] is None:
        planet_id = "0"
    planet_id = data["planet_id"]
    

    user_filter = User.query.filter_by(id=user_id)
    character_filter = Character.query.filter_by(id=character_id)
    planet_filter = Planet.query.filter_by(id=planet_id)

    if user_filter is not None and character_filter is not None:
        favorite.user_id = data["user_id"]
        favorite.user_character = data["character_id"]
        favorite.planet_id = data["planet_id"]
        db.session.add(favorite)
        db.session.commit()

        return jsonify({
        "msg": "favorite created"
        }), 200

    elif user_filter is not None and planet_filter is not None:
        favorite.user_id = data["user_id"]
        favorite.user_planet = data["planet_id"]
        db.session.add(favorite)
        db.session.commit()

        return jsonify({
        "msg": "favorite created"
        }), 200

    else:
        return jsonify({
                "msg":"favorite could not be create, make sure user, character or planet exists"
            }), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
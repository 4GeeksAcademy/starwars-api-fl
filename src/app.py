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
from models import db, User, Planets, Favorites, Character
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

# recuperar todos los personajes

@app.route('/character', methods=['GET'])
def get_all_character():
    query_results_characters= Character.query.all()
    results = list(map(lambda item: item.serialize(),query_results_characters))
    
    if results == []:
        return jsonify({"msg": "No hay personajes"}), 404
    
    response_body = {
        "msg": "ok",
        "results": results
    }

    return jsonify(response_body), 200



# recuperar un solo personaje por su id

@app.route('/character/<int:character_id>', methods=['GET'])
def get_one_character(character_id):
    query_result_one_character= Character.query.filter_by(id=character_id).first()
    
    print(query_result_one_character)
    
    if query_result_one_character is None:
        return jsonify({"msg": "El personaje no existe"}), 404
    
    response_body = {
        "msg": "ok",
        "results": query_result_one_character.serialize()
    }

    return jsonify(response_body), 200



# recuperar todos los planetas

@app.route('/planets', methods=['GET'])
def get_all_planets():
    query_results_planets= Planets.query.all()
    results = list(map(lambda item: item.serialize(),query_results_planets))
    
    if results == []:
        return jsonify({"msg": "No hay planetas"}), 404
    
    response_body = {
        "msg": "ok",
        "results": results
    }

    return jsonify(response_body), 200



# recuperar un solo planeta por su id

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    query_result_one_planet= Planets.query.filter_by(id=planet_id).first()
    
    print(query_result_one_planet)
    
    if query_result_one_planet is None:
        return jsonify({"msg": "El planeta no existe"}), 404
    
    response_body = {
        "msg": "ok",
        "results": query_result_one_planet.serialize()
    }

    return jsonify(response_body), 200

# recuperar todos los usuarios del blog

@app.route('/users', methods=['GET'])
def get_all_users():
    query_results_users= User.query.all()
    results = list(map(lambda item: item.serialize(),query_results_users))
    
    if results == []:
        return jsonify({"msg": "No hay usuarios"}), 404
    
    response_body = {
        "msg": "ok",
        "results": results
    }

    return jsonify(response_body), 200

# Listar todos los favoritos que pertenecen al usuario actual.
# falta esta tarea aqui===>



# Añadir un nuevo planeta favorito al usuario actual con el id = planet_id

@app.route('/favorites/planets/<int:planet_id>', methods=['POST'])
def create_planet_favorite(planet_id):
    data_Favorites = request.json
    print(data_Favorites)
    # query_result= Planets.query.filter.by(planet_id=data_Favorites["planet_id"]).firts()
    # if query_result is None:
    
    new_Planet_favorite=Planets(name=data_Favorites["name"],population=data_Favorites["population"],
                                climate=data_Favorites["climate"],orbital_period =data_Favorites["orbital_period "],
                         rotation_period=data_Favorites["rotation_period"],diametro=data_Favorites["diametro"],
                         birth_year=data_Favorites["birth_year"])
    db.session.add(new_Planet_favorite)
    db.session.commit()
   

    response_body = {
        "msg": "EL planeta se agregado con exito ",
        }
    return jsonify(response_body), 200 

    # else:
    #  return jsonify({"msg": "El planeta ya existe"}), 404


# @app.route('/favorites/planets/<int:planet_id>', methods=['POST'])
# def create_planet_favorite(planet_id):
#     data_Favorites = request.json
#     print(data_Favorites)
#     new_Planet_favorite= Favorites(user_id=data_Favorites["user_id"],character_id=data_Favorites["character_id"],
#     planets_id=data_Favorites["planets_id"],startships_id=data_Favorites["startships_id"])
#     db.session.add(new_Planet_favorite)
#     db.session.commit()

#     response_body = {
#         "msg": "EL planeta se agregado con exito a Favorites",
#         }
#     return jsonify(response_body), 200 

# Añade un nuevo Character favorito al usuario actual con el id = character_id.

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def create_character_favorite(character_id):
    data_character_favorite = request.json
    print(data_character_favorite)
    new_character_favorite= Character(name=data_character_favorite["name"], height=data_character_favorite["height"],
    mass=data_character_favorite["mass"], hair_color=data_character_favorite["hair_color"], eye_color=data_character_favorite["eye_color"],
    gender = data_character_favorite["gender"],birth_year = data_character_favorite["birth_year"])
    
    db.session.add(new_character_favorite)
    db.session.commit()

    response_body = {
        "message": "Character favorite added successfully"
    }
    return jsonify(response_body), 200
   
#  Elimina un planet favorito con el id = planet_id

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    planet_to_delete = Planets.query.get(planet_id)

    if planet_to_delete:
        db.session.delete(planet_to_delete)
        db.session.commit()
        response_body = {
            "msg": "El planeta se ha eliminado con éxito."
        }
        return jsonify(response_body), 200
    else:
        response_body = {
            "msg": "No se encontró el planeta con el ID proporcionado."
        }
        return jsonify(response_body), 404

#  Elimina un character favorito con el id = character_id.
    
@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    character_to_delete = Character.query.get(character_id)

    if character_to_delete:
        db.session.delete(character_to_delete)
        db.session.commit()
        response_body = {
            "msg": "El personaje se ha eliminado con éxito."
        }
        return jsonify(response_body), 200
    else:
        response_body = {
            "msg": "No se encontró el personaje con el ID proporcionado."
        }
        return jsonify(response_body), 404
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

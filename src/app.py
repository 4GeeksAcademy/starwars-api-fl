"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_jwt_extended import JWTManager,create_access_token, get_jwt_identity, jwt_required
from flask_migrate import Migrate
from flask_swagger import swagger 
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Favorites, Character
import random
import string
import logging
from flask import request, jsonify
import datetime



# from .models import Favorite  # Importa el modelo de Favorito

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')  # Cambiar por una clave secreta adecuada
jwt = JWTManager(app)

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




def generar_id_unico():
    while True:
        # Genera un número aleatorio de 9 dígitos
        id_aleatorio = ''.join(random.choices(string.digits, k=9))
        
        # Verifica si el número ya existe en la base de datos
        if not User.query.get(id_aleatorio):
            return id_aleatorio
        



#  recuperar todos los personajes 
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


@app.route('/add-favorite', methods=['POST'])
@jwt_required()  # Requiere autenticación JWT
def add_favorite():
    current_user_id = get_jwt_identity()  # Obtiene el ID del usuario actual del token JWT
    data = request.json  # Obtén los datos del favorito desde la solicitud JSON

    # Asegúrate de que los datos necesarios estén presentes en la solicitud
    if "user_id" not in data or ("character_id" not in data and "planets_id" not in data and "starships_id" not in data):
        return jsonify({"msg": "User ID and either character_id, planets_id, or starships_id are required"}), 400

    # Crea un nuevo favorito con los datos proporcionados
    new_favorite = Favorites(
        user_id=current_user_id,
        character_id=data.get("character_id"),
        planets_id=data.get("planets_id"),
        startships_id=data.get("starships_id")
    )

    # Agrega el nuevo favorito a la base de datos y confirma los cambios
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({
        "msg": "New favorite successfully added",
        "favorite_id": new_favorite.id
    }), 200


# Añadir un nuevo planeta favorito al usuario actual con el id = planet_id

@app.route('/favorites/planets/<int:planet_id>', methods=['POST'])
@jwt_required()
def create_planet_favorite(planet_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "El planeta no existe"}), 404
    
    favorite = Favorites(user_id=user.id, planet_id=planet.id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({"msg": "El planeta se ha agregado como favorito"}), 200

# Añadir un nuevo character favorito al usuario actual con el id = character_id
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
    
# @app.route("/login", methods=["POST"])
# def login():
#     email = request.json.get("email", None)
#     password = request.json.get("password", None)

#     user = User.query.filter_by(email=email).first()

#     if user is None:
#         return jsonify({"msg": "Bad Request"}), 404

#     if email == user.email and password == user.password:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
    
#     else: 
#         return jsonify({"msg": "Bad email or password. I am sorry"}), 401

@app.route('/login', methods=['POST'])
def login():
    email= request.json.get("email", None)
    password= request.json.get("password", None)
    queryResult = User.query.filter_by(email=email).first()
    if queryResult is None:
        return jsonify({"msg": "Bad email or password"}), 404
    if email != queryResult.email or password != queryResult.password:
        return jsonify({"msg": "Bad email or password"}), 401
    
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


@app.route("/valid-token", methods=["GET"])
@jwt_required()
def valid_token():
    current_user = get_jwt_identity()

    user = User.query.filter_by(email=current_user).first()

    if user is None:
        return jsonify({"msg": "user does not exist"
                        }), 404
     
    return jsonify({"is_logged": True}), 200

@app.route('/', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({
        "msg": "Access to protected route"
    }), 200

# @app.route('/create-user', methods=['POST'])
# def create_user():
#     data = request.json
#     user_exists = User.query.filter_by(email=data["email"]).first()
#     if user_exists is None: 
#         new_user_data = {
#             "userName": data["userName"],
#             "email": data["email"],
#             "password": data["password"],
#             "age": data["age"]
#         }

#         new_user = User(**new_user_data)
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify({
#             "msg": "new user successfully created"
#         }), 200
#     else: 
#         return jsonify({
#             "msg": "this email is already used by a user"
#         }), 400

@app.route('/create-user', methods=['POST'])
def create_user():
    data = request.json
    user_exists = User.query.filter_by(email=data["email"]).first()
    if user_exists is None: 
        new_user_data = {
            "userName": data["userName"],
            "email": data["email"],
            "password": data["password"],
            "age": data["age"]
        }

        new_user = User(**new_user_data)
        db.session.add(new_user)
        db.session.commit()

        # Generar el token
        access_token = create_access_token(identity=new_user.id, expires_delta=datetime.timedelta(hours=24))

        return jsonify({
            "msg": "new user successfully created",
            "token": access_token
        }), 200
    else: 
        return jsonify({
            "msg": "this email is already used by a user"
        }), 400
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

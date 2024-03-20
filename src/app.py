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
from models import db, User, Planet ,  FavoriteCharacter, FavoritePlanet, FavoriteVehicles, Character , Vehicle

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

@app.route('/users' , methods=['GET'])
def get_users():
    all_users= User.query.all()
    if all_users is None:
        return jsonify({'Error': 'user not found'}), 404
    
    serialized_all_users = [user.serialize() for user in all_users]
    return jsonify({'users': serialized_all_users})


@app.route('/users/<int:user_id>/favorites' , methods=['GET'])
def get_favorites(user_id):
   user= User.query.get(user_id)
   if user is None:
        return jsonify({'Error': 'User not found'}), 404
    
   all_user_character_favorites= FavoriteCharacter.query.filter_by(user_id=user_id).all()
   all_user_vehicles_favorites= FavoriteVehicles.query.filter_by(user_id=user_id).all()
   all_user_Planet_favorites= FavoritePlanet.query.filter_by(user_id=user_id).all()
   
   all_user_favorites = all_user_character_favorites + all_user_vehicles_favorites + all_user_Planet_favorites
   
   if not all_user_favorites:
        return jsonify({'Error': 'favorites not found for this user'}), 404
   
   serialized_all_user_favorites = [favorito.serialize() for favorito in all_user_favorites]
   return jsonify({'favorites': serialized_all_user_favorites})

   

@app.route('/people' , methods=['GET'])
def get_people():
    all_people= Character.query.all()
    if all_people is None:
        return jsonify({'Error': 'user not found'}), 404
    
    serialized_all_people = [people.serialize() for people in all_people]
    return jsonify({'people': serialized_all_people})


@app.route('/people/<int:id>' , methods= ['GET'])
def get_person(id):
   person= Character.query.filter_by(id=id).all()
   if person is None:
       return jsonify({'Error': 'user not found'}), 400
   
   serilized_person= [persona.serialize() for persona in person]
   return jsonify({'people': serilized_person})




@app.route('/planets' , methods=['GET'])
def get_planets():
    all_planets= Planet.query.all()
    if all_planets is None:
        return jsonify({'Error': 'planet not found'}), 404
    
    serialized_all_planets = [planet.serialize() for planet in all_planets]
    return jsonify({'planets': serialized_all_planets})


@app.route('/planets/<int:id>' , methods= ['GET'])
def get_planet(id):
   planet= Planet.query.filter_by(id=id).all()
   if planet is None:
       return jsonify({'Error': 'planet not found'}), 400
   
   serilized_planet= [planeta.serialize() for planeta in planet]
   return jsonify({'people': serilized_planet})


@app.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['POST'])
def create_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'Error': 'User not found'}), 404
    
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'Error': 'Planet not found'}), 404

    # favorite_planet = FavoritePlanet.query.filter_by(planet_id.like(planet_id), user_id.like(user_id)).first()
    # if favorite_planet is None:
    #     return jsonify({'Error': 'Planet already in your favorites'}), 404

    new_favorite = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    try:
        db.session.commit()
        return jsonify({
            'Message': 'Planet added to favorites successfully',
            'planet_name': planet.planet_name,
            'planet_description': planet.planet_description
        }), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({'Error': 'Failed to add planet to favorites'}), 500

@app.route('/favorite/people/<int:user_id>/<int:character_id>', methods=['POST'])
def create_favorite_people(user_id, character_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'Error': 'User not found'}), 404

    character = Character.query.get(character_id)
    if character is None:
        return jsonify({'Error': 'Character not found'}), 404

    new_favorite = Favorite(user_id=user_id, character_id=character_id)
    db.session.add(new_favorite)
    try:
        db.session.commit()
        return jsonify({
            'Message': 'Character added to favorites successfully',
            'character_name': character.character_name,
            'character_description': character.character_description
        }), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({'Error': 'Failed to add character to favorites'}), 500










@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
     favorite_planet = FavoritePlanet.query.filter_by(planet_id=planet_id).first()
     if favorite_planet is None:
        return jsonify({'Error': 'Favorite planet not found'}), 404
     
     db.session.delete(favorite_planet)
     try:
        db.session.commit()
        return jsonify({'Message': 'Favorite planet deleted'}), 200
     except Exception as error:
        db.session.rollback()
        return jsonify({'Error': 'Failed to delete favorite planet'}), 500


@app.route('/favorite/people/<int:character_id>' , methods =['DELETE'])
def delete_favorite_people(character_id):
    favorite_people = FavoriteCharacter.query.filter_by(character_id=character_id).first()
    if favorite_people is None:
        return jsonify({'Error': 'Favorite people not found'}), 404
    
    db.session.delete(favorite_people)
    try:
        db.session.commit()
        return jsonify({'Message' : 'Favorite people deleted'}), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({'Error': 'failed to delete favorite people'}), 500











# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

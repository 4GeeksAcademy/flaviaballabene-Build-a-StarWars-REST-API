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
from models import db, User, Favourites, Characters, Planets, Vehicles
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
def get_all_users():

    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200

# [GET] /characters Get a list of all the characters in the database.

@app.route('/characters', methods=['GET'])
def get_all_characters():

    characters = Characters.query.all()
    all_characters = list(map(lambda x: x.serialize(), characters))

    return jsonify(all_characters), 200

# [GET] /characters/<int:characters_id> Get one single person's information.

@app.route('/characters/<int:characters_id>', methods=['GET'])
def get_character(characters_id):

    character = Characters.query.get(characters_id)
    one_character = character.serialize()

    return jsonify(one_character), 200

# [GET] /planets Get a list of all the planets in the database.

@app.route('/planets', methods=['GET'])
def get_all_planets():

    planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))

    return jsonify(all_planets), 200

# [GET] /planets/<int:planets_id> Get one single planet's information.

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planet(planets_id):

    planet = Planets.query.get(planets_id)
    one_planet = planet.serialize()

    return jsonify(one_planet), 200

# [GET] /vehicles Get a list of all the vehicles in the database.

@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():

    vehicles = Vehicles.query.all()
    all_vehicles = list(map(lambda x: x.serialize(), vehicles))

    return jsonify(all_vehicles), 200

# [GET] /vehicles/<int:vehicles_id> Get one single vehicle's information.

@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_vehicle(vehicles_id):

    vehicle = Vehicles.query.get(vehicles_id)
    one_vehicle = vehicle.serialize()

    return jsonify(one_vehicle), 200

# [GET] /users/favorites Get all the favorites that belong to the current user.

@app.route('/<int:user_id>/favourites', methods=['GET'])
def get_user_favourites(user_id):

    user = User.query.get(user_id)
    favourites = user.favourites  

    all_favourites = list(map(lambda x: x.serialize(), favourites))

    return jsonify(all_favourites), 200

# [POST] /favorite/planet/<int:planet_id> Add a new favorite planet to the current user with the planet id = planet_id.

@app.route('/favourite/planet/<int:planets_id>', methods=['POST'])
def add_favorite_planet(planets_id):

    user_id = request.headers.get('user_id')
    user = User.query.get(user_id)

    planet = Planets.query.get(planets_id)

    favourite_planet = Favourites(user_id=user.id, planet_id=planet.id)

    user.favourites.append(favourite_planet)

    db.session.commit()

    return jsonify({'message': 'Favorite planet added successfully'}), 200

# [POST] /favorite/people/<int:people_id> Add new favorite people to the current user with the people id = people_id.

@app.route('/favourite/characters/<int:characters_id>', methods=['POST'])
def add_favorite_character(characters_id):

    user_id = request.headers.get('user_id')
    user = User.query.get(user_id)

    character = Characters.query.get(characters_id)

    favourite_character= Favourites(user_id=user.id, character_id=character.id)

    user.favourites.append(favourite_character)

    db.session.commit()

    return jsonify({'message': 'Favorite character added successfully'}), 200

# [DELETE] /favorite/planet/<int:planet_id> Delete a favorite planet with the id = planet_id.

@app.route('/favorite/planet/<int:planets_id>', methods=['DELETE'])
def delete_favorite_planet(planets_id):
    
    favorite_planet = Favourites.query.filter_by(planet_id=planets_id).first()

    db.session.delete(favorite_planet)
    db.session.commit()
    return jsonify({'message': 'Favorite planet deleted successfully'}), 200

# [DELETE] /favorite/people/<int:people_id> Delete a favorite people with the id = people_id.

@app.route('/favorite/characters/<int:characters_id>', methods=['DELETE'])
def delete_favorite_character(characters_id):
    
    favorite_character = Favourites.query.filter_by(character_id=characters_id).first()

    db.session.delete(favorite_character)
    db.session.commit()
    return jsonify({'message': 'Favorite character deleted successfully'}), 200


# Create also endpoints to add (POST), update (PUT), and delete (DELETE) planets and characters

@app.route('/characters', methods=['POST'])
def post_characters():

    data = request.json

    name = data.get('name')
    height = data.get('height')
    mass = data.get('mass')
    hair_color = data.get('hair_color')
    skin_color = data.get('skin_color')
    eye_color = data.get('eye_color')
    birth_year = data.get('birth_year')
    gender = data.get('gender')
    homeworld = data.get('homeworld')
    films = data.get('films')
    species = data.get('species')
    vehicles = data.get('vehicles')
    starships = data.get('starships')
    url = data.get('url')


    new_character = Characters(
        name=name,
        height=height,
        mass=mass,
        hair_color=hair_color,
        skin_color=skin_color,
        eye_color=eye_color,
        birth_year=birth_year,
        gender=gender,
        homeworld=homeworld,
        films=films,
        species=species,
        vehicles=vehicles,
        starships=starships,
        url=url
    )

    db.session.add(new_character)
    db.session.commit()

    return jsonify({'message': 'Character created successfully'}), 201
    
@app.route('/planets', methods=['POST'])
def post_planets():

    data = request.json

    name = data.get('name')
    rotation_period = data.get('rotation_period')
    orbital_period = data.get('orbital_period')
    diameter = data.get('diameter')
    climate = data.get('climate')
    gravity = data.get('gravity')
    terrain = data.get('terrain')
    surface_water = data.get('surface_water')
    population = data.get('population')
    residents = data.get('residents')
    films = data.get('films')
    url = data.get('url')


    new_planet = Planets(
        name=name,
        rotation_period=rotation_period,
        orbital_period=orbital_period,
        diameter=diameter,
        climate=climate,
        gravity=gravity,
        terrain=terrain,
        surface_water=surface_water,
        population=population,
        residents=residents,
        films=films,
        url=url
    )

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({'message': 'Planet created successfully'}), 201
    
@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    
    planet = Planets.query.get(planet_id)
    
    data = request.json
    planet.name = data.get('name', planet.name)
    planet.rotation_period = data.get('rotation_period', planet.rotation_period)
    planet.orbital_period = data.get('orbital_period', planet.orbital_period)
    planet.diameter = data.get('diameter', planet.diameter)
    planet.climate = data.get('climate', planet.climate)
    planet.gravity = data.get('gravity', planet.gravity)
    planet.terrain = data.get('terrain', planet.terrain)
    planet.surface_water = data.get('surface_water', planet.surface_water)
    planet.population = data.get('population', planet.population)
    planet.residents = data.get('residents', planet.residents)
    planet.films = data.get('films', planet.films)
    planet.url = data.get('url', planet.url)


    db.session.commit()
    return jsonify({'message': 'Planet updated successfully'}), 200
    

@app.route('/characters/<int:character_id>', methods=['PUT'])
def update_character(character_id):

    character = Characters.query.get(character_id)

    data = request.json
    character.name = data.get('name', character.name)
    character.height = data.get('height', character.height)
    character.mass = data.get('mass', character.mass)
    character.hair_color = data.get('hair_color', character.hair_color)
    character.skin_color = data.get('skin_color', character.skin_color)
    character.eye_color = data.get('eye_color', character.eye_color)
    character.birth_year = data.get('birth_year', character.birth_year)
    character.gender = data.get('gender', character.gender)
    character.homeworld = data.get('homeworld', character.homeworld)
    character.films = data.get('films', character.films)
    character.species = data.get('species', character.species)
    character.vehicles = data.get('vehicles', character.vehicles)
    character.starships = data.get('starships', character.starships)
    character.url = data.get('url', character.url)


    db.session.commit()
    return jsonify({'message': 'Character updated successfully'}), 200


@app.route('/characters', methods=['DELETE'])
def delete_all_characters():

    Characters.query.delete()
    db.session.commit()
    return jsonify({'message': 'All characters deleted successfully'}), 200

@app.route('/planets', methods=['DELETE'])
def delete_all_planets():

    Planets.query.delete()
    db.session.commit()
    return jsonify({'message': 'All planets deleted successfully'}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
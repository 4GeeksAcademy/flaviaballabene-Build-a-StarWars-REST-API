from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    favourites = db.relationship("Favourites", uselist=False, lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    
class Favourites(db.Model):
    __tablename__ = 'favourites'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id),nullable=False)
    user = db.relationship("User", back_populates="favourites")
    characters = db.relationship("Characters", lazy=True)
    planets = db.relationship("Planets", lazy=True)
    vehicles = db.relationship("Vehicles", lazy=True)
    

    def serialize(self):
        return {
            "id": self.id,
        }
    
class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    mass = db.Column(db.Integer, unique=False, nullable=False)
    hair_color = db.Column(db.String(20), unique=False, nullable=False)
    skin_color = db.Column(db.String(20), unique=False, nullable=False)
    eye_color = db.Column(db.String(20), unique=False, nullable=False)
    birth_year = db.Column(db.String(20), unique=False, nullable=False)
    gender = db.Column(db.String(20), unique=False, nullable=False)
    homeworld = db.Column(db.String(20), unique=False, nullable=False)
    films = db.Column(db.String(200), unique=False, nullable=False)
    species = db.Column(db.String(200), unique=False, nullable=False)
    vehicles = db.Column(db.String(200), unique=False, nullable=False)
    starships = db.Column(db.String(200), unique=False, nullable=False)
    url = db.Column(db.String(200), unique=False, nullable=False)
    favourite_id = db.Column(db.Integer, db.ForeignKey('favourites.id'),nullable=True)
    favourite = db.relationship('Favourites', back_populates = 'characters')




    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld,
            "films": self.films,
            "species": self.species,
            "vehicles": self.vehicles,
            "starships": self.starships,
            "url": self.url,
            "favourite_id": self.favourite_id,              
        }



class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    rotation_period = db.Column(db.String(20), unique=False, nullable=False)
    orbital_period = db.Column(db.String(20), unique=False, nullable=False)
    diameter = db.Column(db.Float, unique=False, nullable=False)
    climate = db.Column(db.String(20), unique=False, nullable=False)
    gravity = db.Column(db.String(20), unique=False, nullable=False)
    terrain = db.Column(db.String(20), unique=False, nullable=False)
    surface_water = db.Column(db.String(20), unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    residents = db.Column(db.String, unique=False, nullable=False)
    films = db.Column(db.String(200), unique=False, nullable=False)
    url = db.Column(db.String(200), unique=False, nullable=False)
    favourite_id = db.Column(db.Integer, db.ForeignKey('favourites.id'),nullable=True)
    favourite = db.relationship('Favourites', back_populates = 'planets')



    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population,
            "residents": self.residents,
            "films": self.films,
            "favourite_id": self.favourite_id,              
        }
    


class Vehicles (db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    model = db.Column(db.String(20), unique=False, nullable=False)
    manufacturer = db.Column(db.String(20), unique=False, nullable=False)
    cost_in_credits = db.Column(db.Float, unique=False, nullable=False)
    length = db.Column(db.Float, unique=False, nullable=False)
    max_atmosphering_speed = db.Column(db.Float, unique=False, nullable=False)
    crew = db.Column(db.Float, unique=False, nullable=False)
    passengers = db.Column(db.Integer, unique=False, nullable=False)
    cargo_capacity = db.Column(db.Float, unique=False, nullable=False)
    consumables = db.Column(db.String(20), unique=False, nullable=False)
    vehicle_class = db.Column(db.String(20), unique=False, nullable=False)
    pilots = db.Column(db.String(200), unique=False, nullable=False)        
    films = db.Column(db.String(200), unique=False, nullable=False)
    url = db.Column(db.String(200), unique=False, nullable=False)
    favourite_id = db.Column(db.Integer, db.ForeignKey('favourites.id'),nullable=True)
    favourite = db.relationship('Favourites', back_populates = 'vehicles')


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "vehicle_class": self.vehicle_class,
            "pilots": self.pilots,
            "films": self.films,
            "url": self.url,
            "favourite_id": self.favourite_id,              
        }


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
           
            # do not serialize the password, its a security breach
        }
    

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(250))
    planet_description = db.Column(db.String(250))
    image_url = db.Column (db.String (150), nullable = True)
    



    def serialize(self):
        return {
            "id": self.id,
            "planet_name": self.planet_name,
            "planet_description": self.planet_description,
            "image_url": self.image_url,
           

        }

class FavoritePlanet(db.Model):
     __tablename__ = 'favoriteplanet'
     id = db.Column(db.Integer, primary_key=True)
     planet_id = db.Column (db.Integer, db.ForeignKey('planet.id'), nullable= True)
     planet = db.relationship('Planet', backref='favoriteplanet')
     user_id = db.Column (db.Integer, db.ForeignKey('user.id'), nullable= False)
     user_favorite = relationship ('User', backref='favoriteplanet')



     def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "planet_name": self.planet.planet_name,  
            "planet_description": self.planet.planet_description,
            "user_id": self.user_id,
           

        }


class FavoriteCharacter(db.Model):
     __tablename__ = 'favoritecharacter'
     id = db.Column(db.Integer, primary_key=True)
    
     character_id = db.Column (db.Integer, db.ForeignKey('character.id'), nullable= True)
     character = db.relationship('Character', backref='favoritecharacter')
     
     user_id = db.Column (db.Integer, db.ForeignKey('user.id'), nullable= False)
     user_favorite = relationship ('User', backref='favoritecharacter')



     def serialize(self):
        return {
            "id": self.id,
            "character_id": self.character_id,
            "character_name": self.character.character_name,  
            "character_description": self.character.character_description,
            "user_id": self.user_id,
            

        }
     
class FavoriteVehicles(db.Model):
     __tablename__ = 'favoritevehicles'
     id = db.Column(db.Integer, primary_key=True)
     
     vehicle_id = db.Column (db.Integer, db.ForeignKey('vehicle.id'), nullable= True)
     vehicle = db.relationship('Vehicle', backref='favoritevehicles')
     user_id = db.Column (db.Integer, db.ForeignKey('user.id'), nullable= False)
     user_favorite = relationship ('User', backref='favoritevehicles')



     def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle_id": self.vehicle_id,
            "vehicle_name": self.vehicle.vehicle_name,  
            "vehicle_description": self.vehicle.vehicle_description,

        }



class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(250))
    character_description = db.Column(db.String(250))
    image_url = db.Column (db.String (150), nullable = True)
    
    
    
    
    def serialize(self):
        return {
            "id": self.id,
            "character_name": self.character_name,
            "character_description": self.character_description,
            "image_url": self.image_url,
            

        }



class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_name = db.Column(db.String(250))
    vehicle_description = db.Column(db.String(250))
    image_url = db.Column (db.String (150), nullable = True)
   


    def serialize(self):
        return {
            "id": self.id,
            "vehicle_name": self.vehicle_name,
            "vehicle_description": self.vehicle_description,
            "image_url": self.image_url,
            

        }
    


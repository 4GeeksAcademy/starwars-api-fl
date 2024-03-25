from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey("user.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
    planets_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    startships_id = db.Column(db.Integer, db.ForeignKey("starships.id"))


    def __repr__(self):
        return '<Favorites %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planets_id": self.planets_id,
            "startships_id ": self.startships_id,
            }



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    age= db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.userName

    def serialize(self):
        return { 
            "id": self.id,
            "userName": self.userName,
            "email": self.email,
            "password" : self.password ,
            "age": self.age,
            
        }
    
class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(120), unique=True, nullable=False)
    height= db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    hair_color= db.Column(db.String(120), unique=False, nullable=False)
    eye_color = db.Column(db.String(120), unique=False, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=False)
    birth_year = db.Column(db.String(120), unique=False, nullable=False)
    Character_favorites = db.relationship(Favorites)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color ": self.hair_color,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "birth_year": self.birth_year,
            }


class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(80), unique=False, nullable=False)
    climate = db.Column(db.String(250), unique=False, nullable=False)
    orbital_period = db.Column(db.BigInteger, unique=False, nullable=False)
    rotation_period = db.Column(db.BigInteger, unique=False, nullable=False)
    diametro = db.Column(db.BigInteger, unique=False, nullable=False)
    birth_year= db.Column(db.String(250), unique=False, nullable=False)
    Planets_favorites = db.relationship(Favorites)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "orbital_period ": self.orbital_period ,
            "rotation_period": self.rotation_period,
            "diametro": self.diametro,
            "birth_year": self.birth_year,
            
        }

class Starships(db.Model):
    __tablename__ = 'starships'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(250), nullable=False)
    crew = db.Column(db.String(250), nullable=False)
    passengers = db.Column(db.String(250), nullable=False)
    consumables = db.Column(db.String(250), nullable=False)
    const_in_credits = db.Column(db.String(250), nullable=False)
    Starships_favorites = db.relationship(Favorites) 

    def __repr__(self):
        return '<Starships %r>' % self.model

    def serialize(self):
        return {
            "id": self.id,
            "model": self.model,
            "crew": self.crew,
            "passengers": self.passengers,
            "consumables": self.consumables,
            "const_in_credits": self.const_in_credits,
            
        }
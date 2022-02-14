# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from create_data import Movie, Director, Genre


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)
api = Api(app)

movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.String()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        movies_schema = MovieSchema(many=True)
        dir_id = request.args.get('director_id')
        gen_id = request.args.get('genre_id')
        if dir_id and gen_id:
            movies = Movie.query.filter(Movie.director_id == dir_id, Movie.genre_id == gen_id).all()
        elif dir_id:
            movies = Movie.query.filter(Movie.director_id == dir_id).all()
        elif gen_id:
            movies = Movie.query.filter(Movie.genre_id == gen_id).all()
        else:
            movies = Movie.query.all()
        if movies:
            return movies_schema.dump(movies), 200
        return "", 404

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
            db.session.commit()
            return "", 201


@movie_ns.route('/<int:mov_id>')
class MovieView(Resource):
    def get(self, mov_id: int):
        movie_schema = MovieSchema()
        try:
            movie = Movie.query.get(mov_id)
            return movie_schema.dump(movie), 200
        except Exception as e:
            return "", 404

    def put(self, mov_id: int):
        movie = Movie.query.get(mov_id)
        if movie:
            req_json = request.json
            movie.title = req_json.get('title')
            movie.description = req_json.get('description')
            movie.trailer = req_json.get('trailer')
            movie.year = req_json.get('year')
            movie.rating = req_json.get('rating')
            movie.genre_id = req_json.get('genre_id')
            movie.director_id = req_json.get('director_id')
            db.session.add(movie)
            db.session.commit()
            return "", 200
        return "", 404

    def delete(self, mov_id: int):
        movie = Movie.query.get(mov_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return "", 200
        return "", 404


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors_schema = DirectorSchema(many=True)
        directors = Director.query.all()
        if directors:
            return directors_schema.dump(directors), 200
        return "", 404

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
            db.session.commit()
            return "", 201


@director_ns.route('/<int:dir_id>')
class DirectorView(Resource):
    def get(self, dir_id: int):
        director_schema = DirectorSchema()
        try:
            director = Director.query.get(dir_id)
            return director_schema.dump(director), 200
        except Exception as e:
            return "", 404

    def put(self, dir_id: int):
        director = Director.query.get(dir_id)
        if director:
            req_json = request.json
            director.name = req_json.get('name')
            db.session.add(director)
            db.session.commit()
            return "", 200
        return "", 404

    def delete(self, dir_id: int):
        director = Director.query.get(dir_id)
        if director:
            db.session.delete(director)
            db.session.commit()
            return "", 200
        return "", 404


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres_schema = GenreSchema(many=True)
        genres = Genre.query.all()
        if genres:
            return genres_schema.dump(genres), 200
        return "", 404

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
            db.session.commit()
            return "", 201


@genre_ns.route('/<int:gen_id>')
class GenreView(Resource):
    def get(self, gen_id: int):
        genre_schema = GenreSchema()
        try:
            genre = Genre.query.get(gen_id)
            return genre_schema.dump(genre), 200
        except Exception as e:
            return "", 404

    def put(self, gen_id: int):
        genre = Genre.query.get(gen_id)
        if genre:
            req_json = request.json
            genre.name = req_json.get('name')
            db.session.add(genre)
            db.session.commit()
            return "", 200
        return "", 404

    def delete(self, gen_id: int):
        genre = Genre.query.get(gen_id)
        if genre:
            db.session.delete(genre)
            db.session.commit()
            return "", 200
        return "", 404


if __name__ == '__main__':
    app.run(debug=True)

import os
from flask import Flask, jsonify, request, abort
from flask.wrappers import Request
from models import *
from flask_cors import CORS

# from .auth.authnew import AuthError, requires_auth
from auth.authnew import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers',
          'Content-Type, Authorization')
        response.headers.add(
          'Access-Control-Allow-Methods',
          'GET,POST,DELETE,PATCH')
        return response


    @app.route('/')
    def get_greeting():
        # excited = os.environ['EXCITED']
        greeting = "Hello" 
        # if excited == 'true': 
        #     greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"
    
    
    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='post:actor')
    def add_actor(payload):
        body = request.get_json()
        try:
            # new_name = body.get("name", None)
            # new_gender = body.get("gender", None)
            # new_movie = body.get("movie_id", None)
            # movies = [new_movie]

            # actor = Actor(name=new_name, gender=new_gender, movies=movies)
            name=body['name'],
            gender=body['gender']
            movies = body["movie_id"]
            movies = Movie.query.filter(Movie.id == body['movie_id']).one_or_none()
            new_movie = [movies]

            actor = Actor(name=name, gender=gender, movies=new_movie)
            #actor.movies = [movies]
            actor.insert()
            return jsonify({
              'success': True
            })
           
        except Exception as e:
            print(e)
            abort(404)
    

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth(permission='update:actor')
    def update_Actors(payload, id):
        '''
        This endpoint updates an actor info given his id
        '''
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            db.session.rollback()
            abort(404)
        
        body = request.get_json()
        if 'name' or 'gender' not in body:
            abort(422)

        try:
          
            # body = request.get_json()
            if 'name' in body:
                actor.name = body['name']
            if 'gender' in body:
                actor.gender = body['gender']
            actor.update()
            return jsonify({
                'success': True,
            })
        except Exception as e:
            print(e)
            abort(404)


    @app.route('/actors', methods=['GET'])
    @requires_auth(permission='read:actors')
    def get_actors(jwt):
        actors = Actor.query.order_by(Actor.id).all()

        actors_formatted = [actor.format() for actor in actors]

        if len(actors) > 0:
            return jsonify({
                            'success': True,
                            'actors': actors_formatted
                            })
        else:
            return jsonify({
                            'success': True,
                            'actors': 'Actors do not available'
                            })
        # return "hello king"


    
    @app.route("/actors/<int:id>", methods=["DELETE"])
    @requires_auth(permission="delete:actor")
    def delete_actor(payload, id):
        actor = Actor.query.get(id)
        if actor is None:
            db.session.rollback()
            abort(400)
        
        actor.delete()

        return jsonify({
            "success": True,
            "deleted": id,
        })


   #---------Movies Enpoint----------------#
    @app.route('/movies', methods=['GET'])
    @requires_auth(permission='read:movies')
    def get_movies(jwt):
        movies = Movie.query.order_by(Movie.id).all()

        movies_formatted = [movie.format() for movie in movies]

        if len(movies) > 0:
            return jsonify({
                            'success': True,
                            'actors': movies_formatted
                            })
        else:
            return jsonify({
                            'success': True,
                            'actors': 'Movies are not available'
                            })


    @app.route('/movie', methods=['POST'])
    @requires_auth(permission='post:movie')
    def add_movie(payload):
        '''
        This endpoint insert Movie information
        '''
        body = request.get_json()
        if body is None:
            abort(422)
        try:
            title=body['title'],
            length=body['length'],
            release_date=body['release_date']
            # actors = Actor.query.filter(Actor.id == body['actor_id']).one_or_none()
            # actors = [actors]
            movie = Movie(title=title, length=length, release_date=release_date)
            movie.insert()
            return jsonify({
              'success': True
            })
        except Exception as e:
            print(e)
            abort(400)



    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth(permission='update:movie')
    def update_movie(payload, id):
        '''
        This endpoint updates an actor info given his id
        '''
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            db.session.rollback()
            abort(404)

        try:
          
            body = request.get_json()
            if 'title' in body:
                movie.title = body['title']
            if 'length' in body:
                movie.length = body['length']
            if 'release_date' in body:
                movie.release_date = body['release_date']
            movie.update()
            return jsonify({
                'success': True,
            })
        except Exception as e:
            print(e)
            abort(404)

    

    @app.route("/movies/<int:id>", methods=["DELETE"])
    @requires_auth(permission='delete:movie')
    def delete_movie(payload, id):
        movie = Movie.query.get(id)
        if movie is None:
            db.session.rollback()
            abort(422)
        
        movie.delete()

        return jsonify({
            "success": True,
            "deleted": id,
        })
    

    #-------------Error Handlers--------------#
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                "success": False, 
                "error": 404,
                "message": "Not found"
                }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request"
            }), 400

    app.errorhandler(500)
    def not_found(error):
        return jsonify({
                "success": False, 
                "error": 500,
                "message": "Internal server error"
                }), 500


    @app.errorhandler(422)
    def unproccesable(error):
        return jsonify({
                "success": False, 
                "error": 422,
                "message": "unproccessable"
                }), 422

    @app.errorhandler(AuthError)
    def autherror(error):
        return jsonify({
            "success":False,
            "error":error.status_code,
            "message":error.error
        }),error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()

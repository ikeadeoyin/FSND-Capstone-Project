import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *


from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_TEST = os.getenv("DB_DEV")

class CapstoneCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.token_assistant = os.getenv("assistant_token")
        self.token_director = os.getenv("director_token")
        self.token_producer = os.getenv("producer_token")
        self.fake_producer_token = os.getenv("fake_producer_token")
        self.app = create_app()
        self.client = self.app.test_client
        
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            DB_USER, DB_PASSWORD, DB_HOST, DB_TEST
        )
        setup_db(self.app, self.database_path)

        self.new_actor = {
            "name":"Chan Liu",
            "gender": "Male",
            "movie_id": "2"
        }
        self.fail_actor = {
            "name":"Chan Liu",
            "gender": "Male",
            "movie_id": "two"
        }
        self.update_actor_failure = {
            "country":"Dubai67"
            }
        self.update_actor = {
            "name":"Megan Lang"
            }
        self.new_movie={
             "title": "A month to Xmas",
             "length": "140",
             "release_date": "2018-12-24"}

        self.new_movie_failure={"country": "Zimbabwe"}

        self.update_movie={
            "length":"176"
        }

        self.update_movie_failure={
            "length":"50 minutes"
        }



        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
    def test_get_actors(self):
        res = self.client().get('/actors', headers={
            "Authorization": 'Bearer ' + self.token_assistant })
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
    
    def test_get_actors_failure(self):
        res = self.client().get('/actor', headers={
            "Authorization": 'Bearer ' + self.token_assistant })
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)
    
    def test_post_actor(self):
        res = self.client().post('/actors', headers={
            "Authorization": 'Bearer '+ self.token_producer }, json=self.new_actor)
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        
    
    def test_post_actor_failure(self):
        res = self.client().post('/actors', headers={
            "Authorization": 'Bearer ' + self.token_director }, json=self.fail_actor)
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)
    
    


    def test_update_actor(self):
        res = self.client().patch('/actors/6', headers={
            "Authorization": 'Bearer '+ self.token_director }, json=self.update_actor)
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
    

    def test_update_actor_failure(self):
        res = self.client().patch('/actors/3', headers={
            "Authorization": 'Bearer '+ self.token_director }, json=self.update_actor_failure)
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(body['success'], False)
    
    
    def test_delete_actor(self):
        res = self.client().delete('/actors/3', headers={
            "Authorization": 'Bearer '+ self.token_director })
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['deleted'], 3)

    def test_delete_actor_failure(self):
        res = self.client().delete('/actors/50', headers={
            "Authorization": 'Bearer '+ self.token_director })
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(body['success'], False)
    
        
        

    def test_get_movies(self):
        res = self.client().get('/movies', headers={
            "Authorization": 'Bearer ' + self.token_assistant })
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
    
    def test_get_movies_failure(self):
        res = self.client().get('/move', headers={
            "Authorization": 'Bearer ' + self.token_assistant })
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)    


    def test_post_movie(self):
        res = self.client().post('/movie', headers={
            "Authorization": 'Bearer '  + self.token_producer}, json=self.new_movie)
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
    
    
    

    def test_post_movie_failure(self):
        res = self.client().post('/movie', headers={
            "Authorization": 'Bearer ' + self.token_producer }, json=self.new_movie_failure)
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(body['success'], False)
    

    def test_update_movie(self):
        res = self.client().patch('/movies/2', headers={
            "Authorization": 'Bearer ' + self.token_director }, json=self.update_movie)
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_update_movie_failure(self):
        res = self.client().patch('/movies/2', headers={
            "Authorization": 'Bearer ' + self.token_director }, json=self.update_movie_failure)
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    

    def test_delete_movie(self):
        res = self.client().delete('/movies/2', headers={
            "Authorization": 'Bearer '+ self.token_producer })
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['deleted'], 2)

    def test_delete_movie_failure(self):
        res = self.client().delete('/movies/50', headers={
            "Authorization": 'Bearer '+ self.token_producer })
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(body['success'], False)

    '''

    #---RBAC Tests-----#
    #----Casting Assistant----#
    def get_actors_without_token(self):
        res = self.client().get("/actors")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_delete_movie_unauthorised(self):
        res = self.client().delete('/movies/50', headers={
            "Authorization": 'Bearer '+ self.token_assistant })
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)


    #-----Casting Director-----#


    def test_post_movie_unauthorised(self):
        res = self.client().post('/movie', headers={
            "Authorization": 'Bearer '  + self.token_director}, json=self.new_movie)
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)
    

    def test_delete_movie_unauthorised(self):
        res = self.client().delete('/movies/5', headers={
            "Authorization": 'Bearer '+ self.token_director })
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    
    #-----Executive Producer-----#

    def test_update_movie_rbac(self):
        res = self.client().patch('/movies/2', headers={
            "Authorizationn":  self.token_producer }, json=self.update_movie)
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    
    def test_delete_movie_wrong_token(self):
        res = self.client().delete('/movies/5', headers={
            "Authorization": 'Bearer '+ self.token_producer })
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(body['success'], False)







# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

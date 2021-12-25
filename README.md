## Project Motivation
This project is the final work for the Udacity Full stack Debeloper Nanodegree. For this project, I am to develop an API that covers:
- Database Design and Schema
- API Development and Documentation
- Unit testing
- Authentication and Authorization 
- Deployment 

## Project Link
You can access the [project](https://capsproject.herokuapp.com/)

## Starting the Project
Fork this repository
[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository](https://github.com/ikeadeoyin/FSND-Capstone-Project) and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository

## Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.
 - [Flask-migrate]() is a package to manage database migrations and changes 


## Database Setup

For this project, we are using PostgresQL as the relational database. You should store databasee variables in a .env file or set them in the terminal.
```bash
DATABASE_URL = 'postgresql://<user>:<password>@localhost:5432/<db_name>'
```

Connect with the database
```
psql -h localhost -U <user> <db_name> 
```

Flask-Migrate is a package to manage our databse.
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```


## Running the Project
Run the following commands in the terminal
```
set FLASK_APP=app
set FLASK_DEBUG=true
flask run
```

## Authentication and Authorization

The Authentication and authorisation was configured through a third party site Auth0. The site allows for a login facility to create a JWT with approval claims which can then be used by the application once configured. The Authentication and authorisation config is setup in auth.py and is then utilised in app.py using @requires_auth() and the payload passed into the function representing each API endpoint. The project involves 3 separate authorisation levels (roles). 

To get token for each role, you can login with these details

Login Link: https://capsproject.us.auth0.com/authorize?scope=SCOPE&audience=https://agency/api&response_type=tokenclient_id=Ljsr2PmWjQ2aObCKDp4zhHfcZrtHzIbm&redirect_uri=https://127.0.0.1:5000/


### Casting Assistant
- Can view actors and movies
- Email: jalebi@gmail.com
- Password:#Bibi000
```
"permissions": [
"get:actors",
"get:movies"
]
```
### Casting Director
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies
- Email: jaleba@gmail.com
- Password:#Bibi000
```
"permissions": [
"delete:actors",
"get:actors",
"get:movies",
"patch:actors",
"patch:movies",
"post:actors"
]
```
### Executive Producer
- All permissions a Casting Director has and…
- Add or delete a movie from the database
- Email: jalebu@gmail.com
- Password:#Bibi000
```
"permissions": [
"delete:actors",
"delete:movies",
"get:actors",
"get:movies",
"patch:actors",
"patch:movies",
"post:actors",
"post:movies"
]
```

## API Reference

### GET /actors
Gets all the actors in the databse
Request parameter: None

Sample Response:
```
{
    "actors": [
        {
            "gender": "Male",
            "id": 7,
            "movies": [
                "A month to Xmas"
            ],
            "name": "Mark Alex"
        },
        {
            "gender": "Female",
            "id": 10,
            "movies": [
                "first time in yankee"
            ],
            "name": "Viola Davis"
        }
    ],
    "success": true
}
```
### POST /actors
Adds a new actor to the database
Request Parameter:
```
new_actor = {
            "name":"Chan Liu",
            "gender": "Male",
            "movie_id": "2"
        }
```

Sample Response:
```
{
   "success": true
}
```

### PATCH /actors/<int:id>
Updates a actor's info
Query Parameter: id
Request body:
```
new_actor = {          
            "gender": "Male"
        }
```

Sample Response:
```
{
   "success": true
}
```

### DELETE /actors/<int:id>
Deletes a actor from the database
- Request arguments: _id:int
- Example response:
```
{
  "deleted": "28", 
  "success": true
}
```

### GET /movies
Gets all the movies in the databse
Request parameter: None

Sample Response:
```
{
    "actors": [
        {
            "actors": [],
            "id": 1,
            "length": 120,
            "release_date": "Sun, 02 Dec 2018 23:00:00 GMT",
            "title": "Money Heist"
        },
        {
            "actors": [
                "Viola Davis"
            ],
            "id": 3,
            "length": 200,
            "release_date": "Tue, 10 Dec 2019 23:00:00 GMT",
            "title": "first time in yankee"
        },
        {
            "actors": [
                "Chila Mags"
            ],
            "id": 4,
            "length": 100,
            "release_date": "Fri, 23 Dec 2011 23:00:00 GMT",
            "title": "A day to Xmas"
        }
    ],
    "success": true
}
```

### POST /movies
Adds a new movie to the database
Request Parameter:

```
new_movie={
    "title": "Boys Before Flowers",
    "length": "140",
    "release_date": "2016-09-14"}
```

Sample Response:
```
{
   "success": true
}
```

### PATCH /moviess/<int:id>
Updates a movie's info
Query Parameter: id
Request body:
```
new_actor = {          
            "length": "135"
        }
```

Sample Response:
```
{
   "success": true
}
```

### DELETE /movies/<int:id>
Deletes a movie from the database
- Request arguments: _id:int
- Example response:
```
{
  "deleted": "8", 
  "success": true
}
```

## Running Tests
``` python test_app.py ```

## Authors
Oyin Olatunji

## Acknowledgement
Thanks to the Udacity team for the strctured course.
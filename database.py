import os
import datetime
import psycopg2

from dotenv import load_dotenv

load_dotenv()

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    name TEXT,
    release_timestamp REAL
);"""

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
);"""

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY(user_username) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);"""

INSERT_MOVIE = "INSERT INTO movies (name, release_timestamp) VALUES (%s, %s)"

SELECT_ALL_MOVIES = "SELECT * FROM movies;"

SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"

INSERT_USER = "INSERT INTO users (username) VALUES (%s)"

SELECT_WATCHED_MOVIES = """
SELECT movies.*
FROM users
JOIN watched ON users.username = watched.user_username
JOIN movies ON watched.movie_id = movies.id
WHERE users.username = %s;"""

SET_MOVIE_WATCHED = "UPDATE movies set watched = 1 WHERE title = %s;"

INSERT_WATCHED_MOVIE = "INSERT INTO  watched (user_username, movie_id) VALUES (%s, %s)"

DELETE_MOVIE = "DELETE FROM movies WHERE title = %s;"

SEARCH_MOVIES = """SELECT * FROM movies WHERE name LIKE %s;"""

CREATE_RELEASE_INDEX = (
    "CREATE INDEX IF NOT EXISTS idx_movies_release ON movies(release_timestamp)"
)

SELECT_FAVORITE_MOVIES = """
SELECT movies.favorite
FROM movies
WHERE users.username = %s;"""


connection = psycopg2.connect(os.environ["DATABASE_URL"])


def create_tables():
    """
    Create the database tables including:
    Movies, Users, Watched, and also create release date index
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_WATCHED_TABLE)
            cursor.execute(CREATE_RELEASE_INDEX)


def add_user(username):
    """
    Add a user to the database
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username,))


def add_movie(title, release_timestamp):
    """
    Add movie to database
    Movie will default to "not watched"
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIE, (title, release_timestamp))


def get_movies(upcoming=False):
    """
    Get all movies 
    """
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                today_timestamp = datetime.datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
            else:
                cursor.execute(SELECT_ALL_MOVIES)
            return cursor.fetchall()


def search_movies(search_term):
    """
    Search all movies using a specific search term
    """
    with connection:
        cursor = connection.cursor()
        cursor.execute(SEARCH_MOVIES, (f"%{search_term}%",))
        return cursor.fetchall()


def watch_movie(username, movie_id):
    """
    Set a movie to watched
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_WATCHED_MOVIE, (username, movie_id))


def get_watched_movies(username):
    """
    Get all movies that are marked as watched
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_WATCHED_MOVIES, (username,))
            return cursor.fetchall()


def get_favorite_movies(username):
    """
    Get all movies that are marked as favorites
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_FAVORITE_MOVIES, (username,))
            return cursor.fetchall()

import datetime
import sqlite3

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    title TEXT,
    release_timestamp REAL,
    watched INTEGER
); """

INSERT_MOVIES = (
    "INSERT INTO movies (title, release_timestamp, watched) VALUES (?, ?, 0);"
)

SELECT_ALL_MOVIES = "SELECT * FROM movies;"

SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"

SELECT_WATCHED_MOVIES = "SELECT * FROM movies WHERE watched = 1;"

connection = sqlite3.connect("data.db")


def create_tables():
    """
    Create the database tables
    """
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)


def add_movie(title, release_timestamp):
    """
    Add movie to database
    Movie will default to "not watched"
    """
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))


def get_movies(upcoming=False):
    """
    Get all movies 
    """
    with connection:
        # Using cursor to get results
        cursor = connection.cursor()
        cursor.execute(SELECT_ALL_MOVIES)
        return cursor.fetchall()

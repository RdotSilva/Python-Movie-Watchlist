import datetime
import sqlite3

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    title TEXT,
    release_timestamp REAL
);"""

CREATE_WATCHLIST_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    watcher_name TEXT,
    title TEXT
);"""

INSERT_MOVIE = "INSERT INTO movies (title, release_timestamp) VALUES (?, ?, 0);"

SELECT_ALL_MOVIES = "SELECT * FROM movies;"

SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"

SELECT_WATCHED_MOVIES = "SELECT * FROM watched WHERE watcher_name = ?;"

SET_MOVIE_WATCHED = "UPDATE movies set watched = 1 WHERE title = ?;"

INSERT_WATCHED_MOVIE = "INSERT INTO  watched (watcher_name, title) VALUES (?, ?)"

DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"

connection = sqlite3.connect("data.db")


def create_tables():
    """
    Create the database tables
    """
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_WATCHLIST_TABLE)


def add_movie(title, release_timestamp):
    """
    Add movie to database
    Movie will default to "not watched"
    """
    with connection:
        connection.execute(INSERT_MOVIE, (title, release_timestamp))


def get_movies(upcoming=False):
    """
    Get all movies 
    """
    with connection:
        # Using cursor to get results
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_MOVIES)
        return cursor.fetchall()


def watch_movie(title):
    """
    Set a movie to watched
    """
    with connection:
        connection.execute(SET_MOVIE_WATCHED, (title,))


def get_watched_movies():
    """
    Get all movies that are marked as watched
    """
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES)
        return cursor.fetchall()

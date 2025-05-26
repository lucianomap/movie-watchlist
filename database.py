import datetime
import os
import time

import psycopg2
from dotenv import load_dotenv

load_dotenv()

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
    );"""

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
    );"""

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_username TEXT,
    movie_id INTEGER, 
    FOREIGN KEY(user_username) REFERENCES users(username), 
    FOREIGN KEY (movie_id) REFERENCES movies(id)
    );"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (%s, %s);"
INSERT_USER = "INSERT INTO users (username) VALUES (%s);"
INSERT_WATCHED_MOVIES = "INSERT INTO watched (user_username, movie_id) VALUES (%s, %s);"

SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"
SELECT_WATCHED_MOVIES = """SELECT movies.* FROM movies
JOIN watched ON movies.id = watched.movie_id
JOIN users ON users.username = watched.user_username
WHERE users.username = %s
;"""

SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = %s;"
SEARCH_MOVIES = "SELECT * FROM movies WHERE title LIKE %s;"
CREATE_RELEASE_INDEX = (
    "CREATE INDEX IF NOT EXISTS idx_movies_release ON movies(release_timestamp);"
)


def connect_to_postgres(host, database, user, password, max_retries=3, retry_delay=3):
    # Connects to a PostgreSQL database with retry logic. You can also use a Docker container.

    # Args:
    #     host (str): The hostname or IP address of the PostgreSQL server.
    #     database (str): The name of the database to connect to.
    #     user (str): The username for authentication.
    #     password (str): The password for authentication.
    #     max_retries (int, optional): The maximum number of connection attempts. Defaults to 5.
    #     retry_delay (int, optional): The delay in seconds between retries. Defaults to 5.

    for attempt in range(max_retries):
        try:
            connection = psycopg2.connect(
                host=host, database=database, user=user, password=password
            )
            print("Successfully connected to PostgreSQL!")
            return connection, 0
        except psycopg2.OperationalError as e:
            print(f"Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                print(
                    "Max connection attempts reached. Unable to connect to PostgreSQL server."
                )
                return 1


host = os.environ["HOST"]
database = os.environ["DATABASE_NAME"]
user = os.environ["USER"]
password = os.environ["PASSWORD"]

connection = connect_to_postgres(host, database, user, password)


def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_WATCHED_TABLE)
            cursor.execute(CREATE_RELEASE_INDEX)


def add_movie(title, release_timestamp):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIES, (title, release_timestamp))


def add_user(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username,))


def get_movies(upcoming=False):
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                today_timestamp = datetime.datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
            else:
                cursor.execute(SELECT_ALL_MOVIES)
            return cursor.fetchall()


def search_movies(search_term):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_MOVIES, (f"%{search_term}%",))
            return cursor.fetchall()


def watch_movie(username, movie_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_WATCHED_MOVIES, (username, movie_id))


def get_watched_movie(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_WATCHED_MOVIES, (username,))
            return cursor.fetchall()

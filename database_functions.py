import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection, cursor
from imports import get_cursor


def get_connection() -> connection:
    """Sets up connection"""
    return psycopg2.connect(
        "dbname=movie_database user=joel host=localhost")


def get_movies() -> list[dict]:
    """Gets all movies from table"""
    conn = get_connection()
    curs = get_cursor(conn)

    query = "SELECT * FROM movie;"

    curs.execute(query)
    data = curs.fetchall()
    curs.close()

    return data

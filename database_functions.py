import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection, cursor
from imports import get_cursor


def get_connection() -> connection:
    """Sets up connection"""
    return psycopg2.connect(
        "dbname=movie_database user=joel host=localhost")

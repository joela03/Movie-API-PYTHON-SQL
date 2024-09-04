import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection, cursor
from imports import get_cursor


def get_connection() -> connection:
    """Sets up connection"""
    return psycopg2.connect(
        "dbname=movies user=joel host=localhost")


def get_movies(search: str = None, sort_by: str = None, sort_order: str = None,) -> list[dict]:
    """Gets all movies from table"""
    conn = get_connection()
    curs = get_cursor(conn)

    query = "SELECT * FROM movie"

    if search:
        search = '%'+search+'%'
        query += " WHERE title ILIKE %s"

    if sort_by:
        query += " ORDER BY " + sort_by
        if sort_order:
            if sort_order == "ascending":
                query += sort_order

    curs.execute(query, (search,))
    data = curs.fetchall()
    curs.close()

    return data

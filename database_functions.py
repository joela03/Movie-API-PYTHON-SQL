import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection, cursor
from imports import get_cursor
from datetime import date
from imports import get_country_key, get_language_key


def get_connection() -> connection:
    """Sets up connection"""
    return psycopg2.connect(
        "dbname=movies user=joel host=localhost")


def validate_sort_by(sort_by: str) -> bool:
    """Checks if we are sorting by a valid parameter"""
    if sort_by and sort_by not in ["title", "release_date", "genre", "revenue", "budget", "score"]:
        return False

    return True


def validate_sort_order(sort_order: str) -> bool:
    """Checks if we are ordering by a valid parameter"""
    if sort_order and sort_order not in ["asc", "desc"]:
        return False

    return True


def get_movies(search: str = None, sort_by: str = None, sort_order: str = None) -> list[dict]:
    """Gets all movies from table"""
    conn = get_connection()
    curs = get_cursor(conn)

    query = "SELECT * FROM movie"
    params = []

    if search:
        search = '%'+search+'%'
        query += " WHERE title ILIKE %s"
        params.append(search)

    if sort_by:
        query += " ORDER BY " + sort_by
        if sort_order:
            query += " " + sort_order

    print(query)
    curs.execute(query, tuple(params) if params else None)
    data = curs.fetchall()
    curs.close()

    return data


def add_movie(title: str, release_date: date, score: int,
              overview: str, orig_title: str, orig_lang: str,
              budget: int, revenue: int, country: str) -> dict:
    """Add's movie to table"""
    conn = get_connection()
    curs = get_cursor(conn)

    # Converting language and country key to their ID's to fit schema
    country_key = get_country_key(country)
    language_key = get_language_key(orig_lang)

    curs.execute("""INSERT INTO movie (title, release_date, score,
                overview, orig_title, orig_lang, budget,
                revenue, country)
                 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *;""",
                 (title, release_date, score, overview, orig_title,
                  language_key, budget, revenue, country_key))

    data = curs.fetchall()
    curs.close()
    return data


def get_genre(genre_id: int) -> dict:
    """Gets genre name given the genre id"""
    conn = get_connection()
    curs = get_cursor(conn)
    curs.execute("SELECT genre_name FROM genre WHERE id = %s;",
                 (genre_id,))
    data = curs.fetchone()
    curs.close()

    return data


def get_movies_by_genre(genre_id: int) -> list[dict]:
    """Gets movies by genre"""
    conn = get_connection()
    curs = get_cursor(conn)
    curs.execute("""SELECT m.title, g.genre_name
                FROM movie as m
                JOIN movie_genres as mg ON mg.movie_id = m.movie_id
                JOIN genre as g ON mg.genre_id = g.id
                WHERE g.id = %s;""",
                 (genre_id,))
    data = curs.fetchall()
    curs.close()

    return data

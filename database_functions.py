"""Functions that query the database"""

from datetime import date
import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection
from imports import get_cursor, get_country_key, get_language_key


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
                revenue, country_id)
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
    curs.execute("SELECT genre_name FROM genre WHERE genre_id = %s;",
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
                JOIN genre as g ON mg.genre_id = g.genre_id
                WHERE g.genre_id = %s;""",
                 (genre_id,))
    data = curs.fetchall()
    curs.close()

    return data


def get_genres() -> list[dict[str, str]]:
    """Gets all possible genre of movies"""
    conn = get_connection()
    curs = get_cursor(conn)

    curs.execute("SELECT genre_name FROM genre;")

    data = curs.fetchall()
    curs.close()

    return data


def get_country_key(country_code: str) -> int:
    conn = get_connection()
    curs = get_cursor(conn)

    curs.execute("SELECT country_id from country where country_name ILIKE %s",
                 (country_code,))

    data = curs.fetchone()
    curs.close()

    return data["country_id"]


def get_movies_by_country(country_id: int, sort_by: str = None,
                          sort_order: str = None) -> list[dict]:
    """Gets all movies from a given country"""
    conn = get_connection()
    curs = get_cursor(conn)

    query = "SELECT * FROM movie WHERE country_id = %s"

    if sort_by:
        query += " ORDER BY " + sort_by
        if sort_order:
            query += " " + sort_order

    curs.execute(query, (country_id,))
    data = curs.fetchall()
    curs.close()

    return data


def get_movie_by_id(movie_id: int) -> list[dict]:
    """Gets a movie from it's id"""
    conn = get_connection()
    curs = get_cursor(conn)

    query = "SELECT * FROM movie WHERE movie_id = %s"

    curs.execute(query, (movie_id,))
    data = curs.fetchone()
    curs.close()

    return data

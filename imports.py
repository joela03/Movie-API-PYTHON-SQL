"""The purpose of this script is to create function's that load the csv into our psql movies database"""

import csv
import psycopg2
import psycopg2.extras


conn = psycopg2.connect(host='localhost', user='joel',
                        dbname='movies', port=5432)


def get_cursor(connection: psycopg2.extensions.connection) -> psycopg2.extensions.cursor:
    """Sets up cursor"""
    return connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def load_to_csv(filename: str) -> list[dict]:
    with open(filename, encoding="utf-8") as f:
        data = []
        for line in csv.DictReader(f):
            data.append(line)
    return data


def get_genre_key(genre: str) -> int:
    """Gets genre key"""
    curs = get_cursor(conn)
    curs.execute("""SELECT id
                   FROM genre
                   WHERE genre_name LIKE %s;""",
                 (genre,))
    data = curs.fetchone()
    curs.close()
    if data:
        return data["id"]

    return 20


def get_language_key(language: str) -> int:
    """Gets language key"""
    curs = get_cursor(conn)
    curs.execute("""SELECT id
                   FROM languages
                   WHERE language_name LIKE %s
                 ;""",
                 (language.strip(),))
    data = curs.fetchone()
    curs.close()
    if data:
        return data.get("id")
    return 32


if __name__ == "__main__":
    movies = load_to_csv("imdb_movies.csv")

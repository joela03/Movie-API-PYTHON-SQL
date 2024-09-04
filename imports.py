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
    curs.execute("""SELECT genre_id
                   FROM genre
                   WHERE genre_name LIKE %s;""",
                 (genre,))
    data = curs.fetchone()
    curs.close()
    if data:
        return data["genre_id"]

    return 20


def get_language_key(language: str) -> int:
    """Gets language key"""
    curs = get_cursor(conn)
    curs.execute("""SELECT language_id
                   FROM languages
                   WHERE language_name LIKE %s
                 ;""",
                 (language.strip(),))
    data = curs.fetchone()
    curs.close()
    if data:
        return data["language_id"]
    return 32


def get_country_key(country_code: str) -> int:
    """"Gets country key"""
    curs = get_cursor(conn)
    curs.execute("""SELECT country_id
                   FROM country
                   WHERE country_name LIKE %s;""",
                 (country_code,))
    data = curs.fetchone()
    curs.close()
    if data:
        return data["country_id"]
    return 61


def import_movies_to_database(movies_list: list[dict]) -> None:
    """Import movies to database"""
    curs = get_cursor(conn)
    for row in movies_list:
        genre_list = row.get('genre').split(', ')
        language_key = get_language_key(row.get('orig_lang', 'No language'))
        country_key = get_country_key(row.get('country'))
        curs.execute("""INSERT INTO movie(title, release_date, score,
                     overview, orig_title, orig_lang, budget, revenue,
                     country_id)
                     VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                     RETURNING movie_id;""",
                     (row['names'], row['date_x'].strip(), row['score'],
                      row['overview'], row['orig_title'], language_key,
                      row['budget_x'], row['revenue'], country_key))
        movie_id = curs.fetchone().get('movie_id')
        conn.commit()

        for genre in genre_list:
            genre_id = get_genre_key(genre)
            curs.execute("""INSERT INTO movie_genres(movie_id, genre_id)
                         VALUES (%s, %s);"""
                         (movie_id, genre_id))
            conn.commit()


if __name__ == "__main__":
    movies = load_to_csv("imdb_movies.csv")
    import_movies_to_database(movies)

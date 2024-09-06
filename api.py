"""API that connects to a movie_database"""

from datetime import datetime
from flask import Flask, jsonify, request
from database_functions import (get_movies, validate_sort_by, validate_sort_order,
                                add_movie, get_genre, get_movies_by_genre, get_genres,
                                get_country_key, get_movies_by_country, get_movie_by_id,
                                delete_movie, validate_data_types)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def endpoint_index():
    """Sets up index route"""
    return jsonify({"message": "Welcome to the Movie API"})


@app.route("/movies", methods=["GET", "POST"])
def endpoint_get_movies():
    """Route returns all movies or adds movie to database"""
    # Adding parameter's to movies route
    if request.method == "GET":
        search = request.args.get("search")
        sort_by = request.args.get("sort_by")
        sort_order = request.args.get("sort_order")

        if not validate_sort_by(sort_by):
            return jsonify({"error": "Invalid sort_by parameter"}), 400

        if not validate_sort_order(sort_order):
            return jsonify({"error": "Invalid sort_order parameter"}), 400

        movies = get_movies(search, sort_by, sort_order)

        if movies == []:
            return {"error": "Movies not found"}, 404

        return jsonify(movies), 200

    else:
        try:
            data = request.json
            title = data["title"]
            release_date = data["release_date"]
            score = float(data["score"])
            orig_title = data["orig_title"]
            orig_lang = data["orig_lang"]
            overview = data["overview"]
            budget = float(data["budget"])
            revenue = float(data["revenue"])
            country = data["country"]

        except KeyError:
            return jsonify({"error": "Missing required fields, ensure data has the following columns: title, release_date, score, overview, orig_title, orig_lang, budget, revenue, country"}), 400
        except ValueError:
            return jsonify({"error": "Post request has invalid data types, ensure budget,revenue and score values are floats and the other values are strings"}), 400

        str_params = [title, release_date, orig_title,
                      orig_lang, overview, country]
        float_params = [score, budget, revenue]

        if not validate_data_types(str_params, str):
            return jsonify({"error": "Post request has invalid data types, ensure budget,revenue and score values are floats and the other values are strings"}), 400

        if not validate_data_types(float_params, float):
            return jsonify({"error": "Post request has invalid data types, ensure budget,revenue and score values are floats and the other values are strings"}), 400

        try:
            datetime.strptime(release_date, "%m/%d/%Y")
        except ValueError:
            return jsonify({"error": "Invalid release_date format. Please use MM/DD/YYYY"}), 400

        try:
            movie = add_movie(title, release_date, score, overview,
                              orig_title, orig_lang, budget, revenue, country)
            return jsonify({'success': movie}), 201
        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500


@app.route("/genres/<int:genre_id>/movies", methods=["GET"])
def endpoint_movies_by_genre(genre_id: int):
    """Get list of movie details by genre"""

    if not get_genre(genre_id):
        return jsonify({"error": "Genre not found"}), 404

    movies = get_movies_by_genre(genre_id)

    if not movies:
        return jsonify({"error": "No movies found for this genre"}), 404

    return jsonify(movies), 200


@app.route("/movies/<int:movie_id>", methods=["GET", "DELETE", "PATCH"])
def endpoint_get_movie(movie_id: int):

    if request.method == "GET":
        movie = get_movie_by_id(movie_id)

        if movie:
            return jsonify(movie), 200
        else:
            return jsonify({"error": "Movie not found"}), 404

    elif request.method == "DELETE":
        success = delete_movie(movie_id)

        if not success:
            return jsonify({"error": "Movie could not be deleted"}), 404

        return jsonify({"message": "Movie deleted"}), 200

    else:
        data = request.json
        title = data["title"]
        release_date = data["release_date"]
        score = data["score"]
        overview = data["overview"]
        orig_title = data["orig_title"]
        orig_lang = data["orig_lang"]
        budget = data["budget"]
        revenue = data["revenue"]
        country = data["country"]

        try:
            for param in [title, release_date, score,
                          overview, orig_title, orig_lang,
                          budget, revenue, country]:
                if not param:
                    raise Exception("Missing required values")
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/genres", methods=["GET"])
def endpoint_get_genres():
    """Get a list of all genres"""
    genres = get_genres()

    if not genres:
        return jsonify({"error": "No genres found"}), 404

    return jsonify(genres)


@app.route("/countries/<string:country_code>", methods=["GET"])
def endpoint_get_movies_by_country(country_code: str):
    """Get a list of movie details by country. Results can be sorted 
    by a specific field in ascending or descending order."""

    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order")

    if not validate_sort_by(sort_by):
        return jsonify({"error": "Invalid sort_by parameter"}), 400

    if not validate_sort_order(sort_order):
        return jsonify({"error": "Invalid sort_order parameter"}), 400

    country_id = get_country_key(country_code)

    if not country_id:
        return jsonify({"error": "Unable to find country with given country code"}), 404

    movies = get_movies_by_country(country_id, sort_by, sort_order)

    if not movies:
        return jsonify({"error": "No movies found for this country"}), 404

    return jsonify(movies), 200


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(debug=True, host="0.0.0.0", port=5000)

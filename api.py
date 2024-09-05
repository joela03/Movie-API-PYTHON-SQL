"""API that connects to a movie_database"""

from datetime import datetime
from flask import Flask, jsonify, request
from database_functions import get_movies, validate_sort_by, validate_sort_order, add_movie, get_genre, get_movies_by_genre

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
            title = str(data["title"])
            release_date = str(data["release_date"])
            score = float(data["score"])
            orig_title = str(data["orig_title"])
            orig_lang = str(data["orig_lang"])
            overview = str(data["overview"])
            budget = float(data["budget"])
            revenue = float(data["revenue"])
            country = float(data["country"])
        except ValueError:
            return jsonify({"error": "Post request has invalid data types, ensure budget,revenue and score values are floats and the other values are strings"}), 400
        except KeyError:
            return jsonify({"error": "Missing required fields, ensure data has the following columns: title, release_date, score, overview, orig_title, orig_lang, budget, revenue, country"}), 400

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

    return jsonify(movies)


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(debug=True, host="0.0.0.0", port=5000)

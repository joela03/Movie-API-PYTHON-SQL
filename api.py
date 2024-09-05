"""API that connects to a movie_database"""

from flask import Flask, jsonify, request
from database_functions import get_movies, validate_sort_by, validate_sort_order

app = Flask(__name__)


@app.route("/", methods=["GET"])
def endpoint_index():
    """Sets up index route"""
    return jsonify({"message": "Welcome to the Movie API"})


@app.route("/movies", methods=["GET"])
def endpoint_get_movies():
    """Route returns all movies or adds movie to database"""
    # Adding parameter's to movies route
    search = request.args.get("search")
    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order")

    if sort_by and sort_by not in ["title", "release_date", "genre", "revenue", "budget", "score"]:
        return jsonify({"error": "Invalid sort_by parameter"}), 400

    if sort_order and sort_order not in ["asc", "desc"]:
        return jsonify({"error": "Invalid sort_order parameter"}), 400

    movies = get_movies(search, sort_by, sort_order)
    if movies == []:
        return {"error": True, "message": "Movies not found"}, 404

    return jsonify(movies), 200


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(debug=True, host="0.0.0.0", port=5000)

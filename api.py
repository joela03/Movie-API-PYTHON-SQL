"""API that connects to a movie_database"""

from flask import Flask, jsonify, request
from database_functions import get_movies

app = Flask(__name__)


@app.route("/", methods=["GET"])
def endpoint_index():
    """Sets up index route"""
    return jsonify({"message": "Welcome to the Movie API"})


@app.route("/movies", methods=["GET"])
def endpoint_get_movies():
    """Route returns all movies or adds movie to database"""
    # Adding search parameter to movies route
    search = request.args.get("search")

    movies = get_movies(search)
    if movies == []:
        return {"error": True, "message": "Movies not found"}, 404

    return jsonify(movies), 200


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(debug=True, host="0.0.0.0", port=5000)

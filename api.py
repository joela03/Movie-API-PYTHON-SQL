"""API that connects to a movie_database"""

from flask import Flask, jsonify, request
from database_functions import get_movies, validate_sort_by, validate_sort_order

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
            return {"error": True, "message": "Movies not found"}, 404

        return jsonify(movies), 200
    else:
        try:
            data = request.json
            title = data["title"]
            release_date = data["release_date"]
            score = data["score"]
            orig_title = data["orig_title"]
            orig_lang = data["orig_lang"]
            overview: str = data.get("overview", "")
            budget: int = data.get("budget", 0)
            revenue: int = data.get("revenue", 0)
            country = data["country"]
        except KeyError:
            return jsonify({"error": """Missing required fields, ensure data has
                            the following columns: title, release_date, score, overview,
                            orig_title, orig_lang, budget, revenue, country"""}), 400


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(debug=True, host="0.0.0.0", port=5000)

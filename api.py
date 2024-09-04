"""API that connects to a movie_database"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def endpoint_index():
    """Sets up index route"""
    return jsonify({"message": "Welcome to the Movie API"})


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(debug=True, host="0.0.0.0", port=5000)

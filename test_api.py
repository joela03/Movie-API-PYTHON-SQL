import pytest
from flask import Flask
# Import your Flask app from the file where it is defined
from api import app
from unittest.mock import patch


@pytest.fixture
def client():
    """Fixture to set up the test client."""
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Test the index route."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the Movie API"}


@patch('api.get_movies')
def test_get_movies_success(mock_get_movies, client):
    """Test the /movies GET route."""
    mock_movies = [
        {"movie_id": 1, "title": "Movie 1", "release_date": "2022-01-01"},
        {"movie_id": 2, "title": "Movie 2", "release_date": "2023-02-02"}
    ]
    mock_get_movies.return_value = mock_movies

    response = client.get("/movies")

    assert response.status_code == 200
    assert response.json == mock_movies
    mock_get_movies.assert_called_once()


@patch('api.get_movies')
def test_get_movies_empty(mock_get_movies, client):
    """Test the /movies GET route with an empty movie list."""
    mock_get_movies.return_value = []

    response = client.get("/movies")

    assert response.status_code == 404
    assert response.json == {"error": True, "message": "Movies not found"}
    mock_get_movies.assert_called_once()

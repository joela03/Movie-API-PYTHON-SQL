import pytest
from flask import Flask
from api import app
from unittest.mock import patch, MagicMock
from database_functions import get_movies


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


@patch('api.get_movies')
def test_get_movies_with_search_success(mock_get_movies, client):
    """Test /movies GET route with a search term."""
    mock_movies = [
        {"movie_id": 3, "title": "Test Movie", "release_date": "2024-01-01"}
    ]
    mock_get_movies.return_value = mock_movies

    response = client.get("/movies?search=Test")

    assert response.status_code == 200
    assert response.json == mock_movies
    mock_get_movies.assert_called_once


@patch('api.get_movies')
def test_get_movies_with_search_failure(mock_get_movies, client):
    """Test /movies GET route with a search term."""
    mock_get_movies.return_value = []

    response = client.get("/movies?search=Invalid")

    assert response.status_code == 404
    assert response.json == {"error": True, "message": "Movies not found"}
    mock_get_movies.assert_called_once()

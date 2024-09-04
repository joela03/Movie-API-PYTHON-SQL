from unittest.mock import patch
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


@pytest.mark.parametrize("sort_by,sort_order,expected_movies", [
    ("names", "asc", ["Inception", "Interstellar"]),
    ("names", "desc", ["Interstellar", "Inception"]),
    ("date_x", "asc", ["Inception", "Interstellar"]),
    ("date_x", "desc", ["Interstellar", "Inception"]),
    ("genre", "asc", ["Interstellar", "Inception"]),
    ("genre", "desc", ["Inception", "Interstellar"]),
    ("revenue", "asc", ["Interstellar", "Inception"]),
    ("revenue", "desc", ["Inception", "Interstellar"]),
    ("budget_x", "asc", ["Inception", "Interstellar"]),
    ("budget_x", "desc", ["Interstellar", "Inception"]),
    ("score", "asc", ["Interstellar", "Inception"]),
    ("score", "desc", ["Inception", "Interstellar"]),
])
@patch('api.get_movies')
def test_movies_sort_order(mock_get_movies, client, sort_by, sort_order, expected_movies):
    movie_1 = {
        "names": "Inception",
        "date_x": "2010-07-16",
        "score": 8.8,
        "genre": "Science Fiction",
        "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.",
        "orig_title": "Inception",
        "status": "Released",
        "orig_lang": "English",
        "budget_x": 160000000,
        "revenue": 829895144,
        "country": "USA"
    }
    movie_2 = {
        "names": "Interstellar",
        "date_x": "2014-11-07",
        "score": 8.6,
        "genre": "Adventure, Drama, Science Fiction",
        "overview": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "orig_title": "Interstellar",
        "status": "Released",
        "orig_lang": "English",
        "budget_x": 165000000,
        "revenue": 677471339,
        "country": "USA"
    }

    mock_movies = [movie_1, movie_2]

    def get_sorted_movies(sort_by, sort_order):
        if sort_by == "names":
            return mock_movies if sort_order == "asc" else mock_movies[::-1]
        if sort_by == "date_x":
            return [movie_1, movie_2] if sort_order == "asc" else [movie_2, movie_1]
        if sort_by == "genre":
            return [movie_2, movie_1] if sort_order == "asc" else [movie_1, movie_2]
        if sort_by == "revenue":
            return [movie_2, movie_1] if sort_order == "asc" else [movie_1, movie_2]
        if sort_by == "budget_x":
            return [movie_1, movie_2] if sort_order == "asc" else [movie_2, movie_1]
        if sort_by == "score":
            return [movie_2, movie_1] if sort_order == "asc" else [movie_1, movie_2]
        return mock_movies

    mock_get_movies.side_effect = lambda search, sort_by, sort_order: get_sorted_movies(
        sort_by, sort_order)

    response = client.get(f'/movies?sort_by={sort_by}&sort_order={sort_order}')
    assert response.status_code == 200
    movies = response.get_json()

    returned_movie_titles = [movie["names"] for movie in movies]

    assert returned_movie_titles == expected_movies

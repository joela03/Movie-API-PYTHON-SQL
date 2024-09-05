from unittest.mock import patch
import pytest
from api import app


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
    assert response.json == {"error": "Movies not found"}
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
    assert response.json == {"error": "Movies not found"}
    mock_get_movies.assert_called_once()


@pytest.mark.parametrize("sort_by,sort_order,expected_movies", [
    ("title", "asc", ["Inception", "Interstellar"]),
    ("title", "desc", ["Interstellar", "Inception"]),
    ("release_date", "asc", ["Inception", "Interstellar"]),
    ("release_date", "desc", ["Interstellar", "Inception"]),
    ("genre", "asc", ["Interstellar", "Inception"]),
    ("genre", "desc", ["Inception", "Interstellar"]),
    ("revenue", "asc", ["Interstellar", "Inception"]),
    ("revenue", "desc", ["Inception", "Interstellar"]),
    ("budget", "asc", ["Inception", "Interstellar"]),
    ("budget", "desc", ["Interstellar", "Inception"]),
    ("score", "asc", ["Interstellar", "Inception"]),
    ("score", "desc", ["Inception", "Interstellar"]),
])
@patch('api.get_movies')
def test_movies_sort_order(mock_get_movies, client, sort_by, sort_order, expected_movies):
    """Tests that movies are sorted correctly"""
    movie_1 = {
        "title": "Inception",
        "release_date": "2010-07-16",
        "score": 8.8,
        "genre": "Science Fiction",
        "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.",
        "orig_title": "Inception",
        "status": "Released",
        "orig_lang": "English",
        "budget": 160000000,
        "revenue": 829895144,
        "country": "USA"
    }
    movie_2 = {
        "title": "Interstellar",
        "release_date": "2014-11-07",
        "score": 8.6,
        "genre": "Adventure, Drama, Science Fiction",
        "overview": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "orig_title": "Interstellar",
        "status": "Released",
        "orig_lang": "English",
        "budget": 165000000,
        "revenue": 677471339,
        "country": "USA"
    }

    def get_sorted_movies(sort_by, sort_order):
        if sort_by == "title":
            return [movie_1, movie_2] if sort_order == "asc" else [movie_2, movie_1]
        if sort_by == "release_date":
            return [movie_1, movie_2] if sort_order == "asc" else [movie_2, movie_1]
        if sort_by == "genre":
            return [movie_2, movie_1] if sort_order == "asc" else [movie_1, movie_2]
        if sort_by == "revenue":
            return [movie_2, movie_1] if sort_order == "asc" else [movie_1, movie_2]
        if sort_by == "budget":
            return [movie_1, movie_2] if sort_order == "asc" else [movie_2, movie_1]
        if sort_by == "score":
            return [movie_2, movie_1] if sort_order == "asc" else [movie_1, movie_2]
        return [movie_1, movie_2]

    mock_get_movies.side_effect = lambda search, sort_by, sort_order: get_sorted_movies(
        sort_by, sort_order)

    response = client.get(f'/movies?sort_by={sort_by}&sort_order={sort_order}')
    assert response.status_code == 200
    movies = response.get_json()

    returned_movie_titles = [movie["title"] for movie in movies]

    assert returned_movie_titles == expected_movies


@patch('api.get_movies')
def test_endpoint_invalid_sort_by(mock_get_movies, client):
    """Test's that it returns error if invalid parameter is passed through"""
    mock_get_movies.return_value = []

    response = client.get('/movies?sort_by=invalid_field')
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid sort_by parameter"}


@pytest.mark.parametrize("missing_field", [
    "title",
    "release_date",
    "score",
    "orig_title",
    "orig_lang",
    "country"
])
def test_post_movie_missing_required_fields(client, missing_field):
    """Test's that it ensures all fields are present when posting"""
    movie_data = {
        "title": "Inception",
        "release_date": "2010-07-16",
        "score": 8.8,
        "orig_title": "Inception",
        "orig_lang": "English",
        "overview": "A mind-bending thriller",
        "budget": 160000000,
        "revenue": 829895144,
        "country": "USA"
    }

    movie_data.pop(missing_field)
    print(movie_data)

    response = client.post("/movies", json=movie_data)

    assert response.status_code == 400
    assert response.get_json() == {
        "error": """Missing required fields, ensure data has the following columns: title, release_date, score, overview, orig_title, orig_lang, budget, revenue, country"""}


@pytest.mark.parametrize("field, invalid_value", [
    ("title", 123),
    ("release_date", 20210101),
    ("score", "high"),
    ("orig_title", 456),

    ("orig_lang", 789),
    ("overview", 101112),
    ("budget", "a lot"),
    ("revenue", "lots"),
    ("country", 131415),
])
def test_post_movie_invalid_data_types(client, field, invalid_value):
    """Test's that route only accepts valid data types"""
    movie_data = {
        "title": "Inception",
        "release_date": "07/16/2010",
        "score": 8.8,
        "orig_title": "Inception",
        "orig_lang": "English",
        "overview": "A mind-bending thriller",
        "budget": 160000000,
        "revenue": 829895144,
        "country": "USA"
    }

    movie_data[field] = invalid_value

    response = client.post("/movies", json=movie_data)

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Post request has invalid data types, ensure budget,revenue and score values are floats and the other values are strings"}


@pytest.mark.parametrize("data, expected_status_code, expected_response", [
    (
        {
            "title": "Inception",
            "release_date": "07/16/2010",
            "score": 8.8,
            "orig_title": "Inception",
            "orig_lang": "English",
            "overview": "A mind-bending thriller",
            "budget": 160000000.1,
            "revenue": 829895144.1,
            "country": "USA"
        },
        201,
        {"success": "mock_movie_data"}
    )
])
@patch('api.add_movie')
def test_post_movie_success(mock_add_movie, client, data, expected_status_code, expected_response):
    """Test's that movie get's posted successfully"""
    mock_add_movie.return_value = "mock_movie_data"

    response = client.post("/movies", json=data)

    assert response.status_code == expected_status_code
    assert response.get_json() == expected_response

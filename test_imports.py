import pytest
from imports import load_to_csv


def test_load_to_csv():
    filename = "test_movies.csv"
    expected_output = [
        {"names": "Movie1", "date_x": "2021-01-01"},
        {"names": "Movie2", "date_x": "2022-02-02"}
    ]
    assert load_to_csv(filename) == expected_output

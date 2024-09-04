import pytest
from flask import Flask
# Import your Flask app from the file where it is defined
from api import app


@pytest.fixture
def client():
    """Fixture to set up the test client."""
    with app.test_client() as client:
        yield client

"""
This module will conduct test for testing smooth operation of Flask Application
"""

# import flask app object from python file containing it
from app import app
import pytest

@pytest.fixture # <-- Hardcoded, do not change
def client():
    return app.test_client() # <-- Hardcoded, do not change

def test_home(client):
    response=client.get('/')
    assert response.status_code == 200

def test_pearson(client):
    response=client.get('/get_subcategories')
    assert response.status_code == 200
import pytest

def test_index(client):
    """Test the root '/' endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Hello, World!"}

def test_404_handler(client):
    """Test the custom 404 error handler."""
    response = client.get('/nonexistent-endpoint')
    assert response.status_code == 404
    assert response.json == {"error": "Page not found"}

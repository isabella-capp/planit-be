import pytest

@pytest.mark.parametrize(
    "endpoint,method,status_code,expected_key",
    [
        ("/db/", "GET", 200, "message"),
        ("/db/animals", "GET", 200, "animals"),
        ("/db/animals/1", "GET", 200, "animal"),
        ("/db/animals/carnivore", "GET", 200, "animals"),
    ]
)
def test_get_requests(client, endpoint, method, status_code, expected_key):
    """ Test GET requests to the specified endpoints """
    response = client.open(endpoint, method=method)
    assert response.status_code == status_code
    assert expected_key in response.json

@pytest.mark.parametrize(
    "payload,status_code,expected_message",
    [
        ({"name": "lion", "habitat": "savannah", "diet": "carnivore"}, 200, "Animal created"),
        ({}, 400, "Missing required fields"),
    ]
)
def test_create_animal(client, payload, status_code, expected_message):
    """ Test POST request to create a new animal """
    response = client.post("/db/animals", json=payload)
    assert response.status_code == status_code
    assert expected_message in response.json.get("error", "") or response.json.get("message", "")

@pytest.mark.parametrize(
    "animal_id,payload,status_code,expected_message",
    [
        (1, {"name": "cat", "diet": "carnivore"}, 200, "updated"),
        (9999, {"name": "Tiger", "diet": "Carnivore"}, 404, "Animal with id 9999 not found"),
        (1, {}, 400, "Missing required fields"),
    ]
)
def test_update_animal(client, animal_id, payload, status_code, expected_message):
    """ Test PUT request to update an existing animal """
    response = client.put(f"/db/animals/{animal_id}", json=payload)
    assert response.status_code == status_code
    assert expected_message in response.json.get("error", "") or response.json.get("message", "")

@pytest.mark.parametrize(
    "animal_id,status_code,expected_message",
    [
        (1, 200, "deleted"),
        (9999, 404, "Animal with id 9999 not found"),
    ]
)
def test_delete_animal(client, animal_id, status_code, expected_message):
    """ Test DELETE request to delete an existing animal """
    response = client.delete(f"/db/animals/{animal_id}")
    assert response.status_code == status_code
    assert expected_message in response.json.get("error", "") or response.json.get("message", "")
import pytest
from app import app
from unittest.mock import patch

@pytest.fixture
def test_client():
    # Setup the Flask test client
    with app.test_client() as client:
        yield client

# Test 1: Check if inventory is empty at the start
def test_initial_empty_list(test_client):
    response = test_client.get('/inventory')
    assert response.status_code == 200
    assert response.get_json() == []

# Test 2: Mock the external API to test adding an item (Task 4)
@patch('app.fetch_product_from_open_food_facts')
def test_add_item_logic(mock_api, test_client):
    # We define what the 'fake' API returns
    mock_api.return_value = {
        "product_name": "Junior Dev Snack",
        "brands": "Coding Co.",
        "details": "High in logic"
    }
    
    # Act: Send a POST request
    response = test_client.post('/inventory', json={"barcode": "000123"})
    
    # Assert: Check if it added correctly
    assert response.status_code == 201
    assert response.get_json()["product_name"] == "Junior Dev Snack"
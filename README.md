# OpenFood-IMS
🍎 Food Inventory REST API System
This project is a full-stack Python application consisting of a Flask REST API and a Command Line Interface (CLI). It allows users to manage a food inventory by fetching real-world data from the OpenFoodFacts API.

📋 Features & Rubric Requirements
Flask Routing: Full implementation of RESTful routes (GET, POST, PATCH, DELETE).

CRUD: Capability to Create, Read, Update, and Delete inventory items.

External API: Real-time integration with OpenFoodFacts using barcodes.

Mock Database: Data is managed in a temporary Python array (simulated storage).

Unit Testing: Comprehensive testing suite using pytest and unittest.mock.

🛠️ Setup and Installation
1. Install Dependencies
Open your terminal and run the following command to install the required libraries:

Bash
pip install flask requests pytest
2. File Setup
Create a folder named food_project and create these three files inside it:

app.py

cli_app.py

test_app.py

💾 File Contents
1. The Backend (app.py)
This file runs the server and handles the database logic.

Python
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Mock database - Simple list to store food items
inventory_list = []

def fetch_from_open_food_facts(barcode):
    """Connects to the real OpenFoodFacts database."""
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:
                p = data["product"]
                return {
                    "name": p.get("product_name", "Unknown"),
                    "brand": p.get("brands", "Generic"),
                    "info": p.get("ingredients_text", "N/A")
                }
    except:
        return None
    return None

# --- ROUTES ---

@app.route('/inventory', methods=['GET'])
def get_all():
    return jsonify(inventory_list), 200

@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.get_json()
    barcode = data.get("barcode")
    api_data = fetch_from_open_food_facts(barcode)
    
    if not api_data:
        return jsonify({"error": "Product not found"}), 404
        
    new_item = {
        "id": len(inventory_list) + 1,
        "name": api_data["name"],
        "brand": api_data["brand"],
        "price": 0.0,
        "stock": 0
    }
    inventory_list.append(new_item)
    return jsonify(new_item), 201

@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    data = request.get_json()
    for item in inventory_list:
        if item['id'] == item_id:
            if 'price' in data: item['price'] = data['price']
            if 'stock' in data: item['stock'] = data['stock']
            return jsonify(item), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory_list
    inventory_list = [i for i in inventory_list if i['id'] != item_id]
    return jsonify({"message": "Deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
2. The UI (cli_app.py)
The menu for interacting with the inventory.

Python
import requests

URL = "http://127.0.0.1:5000/inventory"

def menu():
    while True:
        print("\n--- MENU: 1.View | 2.Add | 3.Update | 4.Delete | 5.Exit ---")
        choice = input("Select an option: ")

        if choice == '1':
            res = requests.get(URL).json()
            for i in res:
                print(f"ID:{i['id']} | {i['name']} | ${i['price']} | Stock:{i['stock']}")
        elif choice == '2':
            barcode = input("Enter Barcode: ")
            print(requests.post(URL, json={"barcode": barcode}).json())
        elif choice == '3':
            item_id = input("ID to update: ")
            price = float(input("New Price: "))
            requests.patch(f"{URL}/{item_id}", json={"price": price})
            print("Update complete.")
        elif choice == '4':
            item_id = input("ID to delete: ")
            requests.delete(f"{URL}/{item_id}")
            print("Deleted.")
        elif choice == '5':
            break

if __name__ == '__main__':
    menu()
3. The Tests (test_app.py)
Verifies the code is working correctly.

Python
import pytest
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_pantry_empty(client):
    res = client.get('/inventory')
    assert res.status_code == 200
    assert res.json == []

@patch('app.fetch_from_open_food_facts')
def test_add_product(mock_api, client):
    mock_api.return_value = {"name": "Test Milk", "brand": "Test Brand"}
    res = client.post('/inventory', json={"barcode": "12345"})
    assert res.status_code == 201
    assert res.json["name"] == "Test Milk"
🚀 Execution Guide
Start the API: Open a terminal and run python app.py.

Open the Menu: Open a second terminal and run python cli_app.py.

Run Tests: In a third terminal, run pytest test_app.py.

📝 Debugging Tips
Ensure Terminal 1 is always running while using the CLI.

If you get an error saying Port 5000 is in use, close all Python processes or restart your computer.

The tests use Mocks; this means they simulate an internet connection to ensure your logic is perfect even if the API is down.

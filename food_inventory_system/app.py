from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

inventory_list = []


def fetch_product_from_open_food_facts(barcode):
   
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:
                product = data["product"]
               
                return {
                    "product_name": product.get("product_name", "Unknown Product"),
                    "brands": product.get("brands", "Generic Brand"),
                    "details": product.get("ingredients_text", "No details available")
                }
    except Exception as e:
        print(f"Connection Error: {e}")
    return None


@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory_list), 200


@app.route('/inventory', methods=['POST'])
def add_item():
    incoming_data = request.get_json()
    if not incoming_data or "barcode" not in incoming_data:
        return jsonify({"error": "Request must include a barcode"}), 400

    barcode = incoming_data.get("barcode")
    
    product_data = fetch_product_from_open_food_facts(barcode)
    
    if product_data is None:
        return jsonify({"error": "Product not found in OpenFoodFacts"}), 404

    
    new_item = {
        "id": len(inventory_list) + 1,
        "product_name": product_data["product_name"],
        "brands": product_data["brands"],
        "details": product_data["details"],
        "price": 0.0,
        "stock": 0
    }
    
    inventory_list.append(new_item)
    return jsonify(new_item), 201

# 3. UPDATE (Patch Item)
@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    update_values = request.get_json()
    
    # Loop through our list to find the item
    for item in inventory_list:
        if item["id"] == item_id:
            if "price" in update_values:
                item["price"] = update_values["price"]
            if "stock" in update_values:
                item["stock"] = update_values["stock"]
            return jsonify(item), 200
            
    return jsonify({"error": "Item not found"}), 404

# 4. DELETE (Remove Item)
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    for item in inventory_list:
        if item["id"] == item_id:
            inventory_list.remove(item)
            return jsonify({"message": "Successfully deleted"}), 200
            
    return jsonify({"error": "Item not found"}), 404

if __name__ == "__main__":
    # Debug mode helps junior devs see errors easily
    app.run(debug=True, port=5000)
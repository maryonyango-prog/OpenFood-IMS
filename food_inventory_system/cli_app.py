import requests

SERVER_URL = "http://127.0.0.1:5000/inventory"

def show_menu():
    print("\n--- JUNIOR FOOD MANAGER ---")
    print("1. View My Inventory")
    print("2. Add New Food (Barcode)")
    print("3. Update Price/Stock")
    print("4. Delete a Product")
    print("5. Quit")
    return input("Choose an action (1-5): ")

def run_application():
    while True:
        user_choice = show_menu()
        
        if user_choice == "1":
            # READ
            response = requests.get(SERVER_URL)
            items = response.json()
            print("\nYOUR PANTRY:")
            for i in items:
                print(f"[{i['id']}] {i['product_name']} | Brand: {i['brands']} | ${i['price']} | Stock: {i['stock']}")
        
        elif user_choice == "2":
            # CREATE
            barcode = input("Enter the barcode (e.g., 5449000000996): ")
            response = requests.post(SERVER_URL, json={"barcode": barcode})
            if response.status_code == 201:
                print("Success! Product added to list.")
            else:
                print("Error: Could not find that barcode.")

        elif user_choice == "3":
            # UPDATE
            item_id = input("Enter ID of product to update: ")
            new_price = float(input("New Price: "))
            new_stock = int(input("New Stock Level: "))
            requests.patch(f"{SERVER_URL}/{item_id}", json={"price": new_price, "stock": new_stock})
            print("Item updated successfully!")

        elif user_choice == "4":
            # DELETE
            item_id = input("Enter ID of product to remove: ")
            requests.delete(f"{SERVER_URL}/{item_id}")
            print("Item deleted.")

        elif user_choice == "5":
            print("Shutting down...")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    run_application()
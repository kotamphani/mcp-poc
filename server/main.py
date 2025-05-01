from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Initialize an empty cart dictionary
# Structure: {user_id: [items]}
cart = {}

@app.route('/', methods=['POST', 'GET'])
def index():
    return "Welcome to the API!"

@app.route('/products', methods=['POST', 'GET'])
def products():
    # Get the path to the products.json file
    file_path = os.path.join(os.path.dirname(__file__), 'products.json')
    try:
        # Open and read the JSON file
        with open(file_path, 'r') as file:
            products_data = json.load(file)
        return jsonify(products_data)
    except FileNotFoundError:
        return jsonify({"error": "Products file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in products file"}), 500

@app.route('/plans', methods=['POST', 'GET'])
def plans():
    # Get the path to the plans.json file
    file_path = os.path.join(os.path.dirname(__file__), 'plans.json')
    try:
        # Open and read the JSON file
        with open(file_path, 'r') as file:
            plans_data = json.load(file)
        return jsonify(plans_data)
    except FileNotFoundError:
        return jsonify({"error": "Plans file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in plans file"}), 500

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    try:
        # Get JSON data from request
        item_data = request.get_json()
        
        # Validate required fields
        if not item_data or 'product_id' not in item_data:
            return jsonify({"error": "Missing required field: product_id"}), 400
        
        product_id = str(item_data['product_id'])
    
        # Initialize cart for user if it doesn't exist
        if product_id not in cart:
            cart[product_id] = item_data
            cart[product_id]['quantity'] = 1
        else:
            cart[product_id]['quantity'] += 1
        
        return jsonify({
            "success": True,
            "message": "Item added to cart",
            "cart": cart[product_id]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cart', methods=['GET'])
def view_cart():
    # Return the current cart contents
    return jsonify(cart)

if __name__ == '__main__':
    app.run(debug=True)

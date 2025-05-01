from mcp.server.fastmcp import FastMCP
import requests
from typing import TypedDict

mcp = FastMCP("test-tool")


@mcp.tool()
def fetchAPI(url: str) -> dict:
    """
    Fetches the content from the given URL.
    """
    try:
        response = requests.get(url)
    
    # Check if the request was successful
        if response.status_code == 200:
            # Print the JSON response
            data = response.json()
            return data
        else:
            return f"Error: API returned status code {response.status_code}"

    except Exception as e:
        return f"Error making API request: {str(e)}"

@mcp.tool()
def api_lookup(url: str = "api.txt") -> str:
    """
    Returns the contents of api.txt as a reference for available APIs.
    This function acts as a lookup table to help LLMs understand which APIs are available to use.
    
    Returns:
        str: Content of the api.txt file listing available APIs and their usage
    """
    try:
        with open(url, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "Error: api.txt file not found. Please create this file with API documentation."
    except Exception as e:
        return f"Error reading API reference file: {str(e)}"

class Item(TypedDict):
    product_id: str
    name: str
    price: float
    quantity: int

@mcp.tool()
def add_to_cart(item: Item) -> str:
    """
    Adds an item to the cart.

    args:
        item (Item): The item to add to the cart. 
        A dictionary with the the following fields:     
            product_id: str
            name: str
            price: float
            quantity: int
        example: item = {"product_id": "A123", "name": "Samsung Z", "price": 999.99, "quantity": 1}
        
    """
    # Simulate adding to cart
    url = 'http://127.0.0.1:5000/cart/add'
    try:
        # Assuming the API accepts a JSON payload
        response = requests.post(url, json=item)
        if response.status_code == 200:
            return f"Added to cart: {item['name']}, Price: {item['price']}, Quantity: {item['quantity']}"
        else:
            return f"Error: API returned status code {response.status_code}"
    except Exception as e:
        return f"Error parsing item: {str(e)}"
    

if __name__ == "__main__":
    mcp.run(transport='stdio')


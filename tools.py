from typing import Any, List, Dict
import uuid
from fastmcp import FastMCP

from infers import OrdersModel 

mcp: Any = FastMCP("shop", debug=True, log_level="INFO")

from helper_functions import cancel_order, get_users, find_user, find_product, list_products,  all_orders, find_product_by_name, place_user_order, reset_data, to_dict

@mcp.tool()
def users() -> list[Dict]:
    """Return a list of all users."""
    return to_dict(get_users())

@mcp.tool()
def orders() -> list[Dict]:
    """Return a list of all orders."""
    return to_dict(all_orders)

@mcp.tool()
def login_user(email: str, pin: str) -> str:
    """Authenticate a user using email and 4-digit PIN."""
    user = find_user(email)
    print("================ Login Attempt =================")
    print(f"Email: {email}, User found: {bool(user)}")
    print("================ Email Attempt =================")
    
    if not user:
        return "User not found."

    if user.pin != pin:
        return "Invalid PIN."

    return f"Login successful for {email}"


@mcp.tool()
def search_products(query: str) -> List[Dict]:
    """Search products by name."""
    results = find_product_by_name(query)

    return (to_dict(results) if results else [])

@mcp.tool()
def list_available_products() -> List[Dict]:
    """List all available products."""
    products = list_products()

    return (to_dict(products) if products else []) 

@mcp.tool()
def search_products_by_sku(sku: str) -> List[Dict]:
    """Search products by SKU."""
    product = find_product(sku)

    return (to_dict([product]) if product else []) 

@mcp.tool()
def place_order(user_email: str, sku: str, quantity: int) -> str:
    """Place an order for a product."""

    # validate user
    user = find_user(user_email)
    if not user:
        return "User not found."

    # validate product
    product = find_product(sku)
    if not product:
        return "Product not found."

    # check stock
    if product.stock_left < quantity:
        return f"Not enough stock. Only {product.stock_left} left."

    # update stock
    product.stock_left -= quantity

    # create order
    order = {
        "order_id": str(uuid.uuid4())[:8],
        "user_email": user_email,
        "sku": sku,
        "product_name": product.product_name,
        "quantity": quantity,
        "total_price": round(product.price * quantity, 2),
        "status": "confirmed"
    }

    place_user_order(OrdersModel(**order))

    return f"Order placed successfully. Order ID: {order['order_id']}"

@mcp.tool()
def cancel_user_order(order_id: str) -> str:
    """Cancel an order by its ID."""
    return cancel_order(order_id)

@mcp.tool()
def get_user_orders(user_email: str) -> List[OrdersModel]:
    """Retrieve all orders for a user after authentication which the user can view their order history."""
    user = find_user(user_email)

    if not user:
        return []

    user_orders = [o for o in all_orders if o.user_email == user_email]

    return user_orders


@mcp.tool()
def check_inventory(sku: str) -> str:
    """Check remaining stock for a product."""
    product = find_product(sku)

    if not product:
        return "Product not found."

    return f"{product.product_name} has {product.stock_left} items left."


@mcp.tool()
def reset_inventory(phrase: str) -> str:
    """Reset inventory for all products to initial stock levels. and require a command phrase to prevent accidental resets."""
    if phrase != "ido":
        return "Invalid command phrase."
    reset_data()
    return "Inventory, orders reset to initial stock levels and orders."


 


import json
from typing import Any, List
import os

from infers import OrdersModel, InventoryModel, UserModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
users: List[UserModel] = []
products: List[InventoryModel] = []
all_orders: List[OrdersModel] = [] 

def load_data():
    """Load users, products, and orders data from JSON files."""
    global users, products, all_orders
    
    with open(os.path.join(BASE_DIR, "resources/users.json"), "r") as f:
        users = [UserModel(**u) for u in json.load(f)]
    
    with open(os.path.join(BASE_DIR, "resources/products.json"), "r") as f:
        products = [InventoryModel(**p) for p in json.load(f)]

def find_user(email: str):
    """Find a user by email."""
    return next((u for u in users if u.email == email), None) 

def find_product(sku: str):
    """Find a product by SKU."""
    return next((p for p in products if p.sku == sku), None)

def find_orders_by_user(email: str) -> List[OrdersModel]:
    """Find all orders placed by a user."""
    return [o for o in all_orders if o.user_email == email]

def find_order_by_id(order_id: str) -> OrdersModel | None:
    """Find an order by its ID."""
    return next((o for o in all_orders if o.order_id == order_id), None)

def find_product_by_name(name: str) -> List[InventoryModel]:
    """Find products that match a name query."""
    return [p for p in products if name.lower() in p.product_name.lower()]

def place_user_order(order: OrdersModel) -> None:
    all_orders.append(order) 
    update_product_stock(order.sku, order.quantity)
        
def update_product_stock(sku: str, quantity: int) -> None:
    product = find_product(sku)
    if product:
        product.stock_left -= quantity
        
def cancel_order(order_id: str) -> str:
    """Cancel an order by its ID."""
    order = find_order_by_id(order_id)
    if not order:
        return "Order not found."
    
    if order.status == "cancelled":
        return "Order is already cancelled."
    
    order.status = "cancelled"
    update_product_stock(order.sku, -order.quantity)  # Restock the product
    return f"Order {order_id} has been cancelled."
            
def reset_data() -> None:
    """Reset orders and product stock to initial state."""
    users.clear()
    products.clear()
    all_orders.clear()
    load_data() 

def to_dict(data: Any):
    if isinstance(data, list):
        return [
            item.model_dump() if hasattr(item, "model_dump")
            else item.dict() if hasattr(item, "dict")
            else item
            for item in data
        ]

    if hasattr(data, "model_dump"):
        return data.model_dump()

    if hasattr(data, "dict"):
        return data.dict()

    return data
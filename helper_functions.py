

import json
from typing import Any, List
import os
from infers import OrdersModel, InventoryModel, UserModel, logger
from resources.infos import BASE_DIR, users, products, all_orders
 
def load_data():
    """Load users, products, and orders data from JSON files."""
    global users, products, all_orders
    logger.info("Loading data from JSON files...")

    with open(os.path.join(BASE_DIR, "users.json"), "r") as f:
        if not os.path.exists(os.path.join(BASE_DIR, "users.json")):
            logger.warning(f"File {os.path.join(BASE_DIR, 'users.json')} not found. No users loaded.")
            users.clear()
        else:
            users_data = [UserModel(**u) for u in json.load(f)]
            users.clear()
            users.extend(users_data)

    with open(os.path.join(BASE_DIR, "products.json"), "r") as f:
        if not os.path.exists(os.path.join(BASE_DIR, "products.json")):
            logger.warning(f"File {os.path.join(BASE_DIR, 'products.json')} not found. No products loaded.")
            products.clear()
        else:
            products_data = [InventoryModel(**p) for p in json.load(f)]
            products.clear()
            products.extend(products_data)

    # Optionally clear all_orders if you want to reset orders as well
    all_orders.clear()
    logger.info("Data loading complete.")

    return users, products, all_orders

def get_users() -> List[UserModel]:
    """Return a list of all users."""
    return users

def orders() -> List[OrdersModel]:
    """Return a list of all orders."""
    return all_orders

def find_user(email: str):
    """Find a user by email."""
    user = [u for u in users if u.email == email]
    user = user[0] if user else None
    print("================ Login Attempt =================")
    print(f"Email: {email}, User found: {bool(user)}")
    print("================ Email Attempt =================")
    return user

def find_product(sku: str):
    """Find a product by SKU."""
    product = [p for p in products if p.sku == sku]
    return product[0] if product else None

def list_products() -> List[InventoryModel]:
    """List all products."""
    return products

def place_user_order(order: OrdersModel) -> None:
    all_orders.append(order) 
    update_product_stock(order.sku, order.quantity)
    
def find_orders_by_user(email: str) -> List[OrdersModel]:
    """Find all orders placed by a user."""
    return [o for o in all_orders if o.user_email == email]

def find_order_by_id(order_id: str) -> OrdersModel | None:
    """Find an order by its ID."""
    return next((o for o in all_orders if o.order_id == order_id), None)

def find_product_by_name(name: str) -> List[InventoryModel]:
    """Find products that match a name query."""
    return [p for p in products if name.lower() in p.product_name.lower()]
        
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


# if __name__ == "__main__":
#     load_data()
#     # finduser = find_user("user1@example.com")
#     # print(finduser)
#     # prod = find_product("0001")
#     # print(prod)
#     # listprod = list_products()
#     # print(listprod)
#     place = place_user_order(OrdersModel(
#         order_id="test1234",
#         user_email="user1@example.com",
#         sku="0001", 
#         quantity=1, 
#         total_price=25.99, 
#         status="confirmed"
#     ))
#     print(place)
#     findOrderId = find_order_by_id('test1234')
#     print( findOrderId)
#     findOrder = find_orders_by_user("user1@example.com")
#     print(findOrder)
#     findProdByName = find_product_by_name("Mouse")
#     print(findProdByName)
#     cancel = cancel_order('test1234')
#     print(cancel)
#     findOrderId = find_order_by_id('test1234')
#     print( findOrderId)
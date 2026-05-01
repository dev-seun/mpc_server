import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from tools import login_user, search_products, search_products_by_sku, place_order, cancel_user_order, get_user_orders, check_inventory, reset_inventory
from helper_functions import reset_data, all_orders

@pytest.fixture(autouse=True)
def setup_data():
    reset_data()
    yield
    reset_data()

def test_login_user_success():
    assert login_user("user1@example.com", "1023") == "Login successful for user1@example.com"

def test_login_user_invalid_pin():
    assert login_user("user1@example.com", "0000") == "Invalid PIN."

def test_login_user_not_found():
    assert login_user("nouser@example.com", "1234") == "User not found."

def test_search_products_found():
    results = search_products("Mouse")
    assert any("Mouse" in p["product_name"] for p in results)

def test_search_products_not_found():
    assert search_products("Nonexistent") == []

def test_search_products_by_sku_found():
    results = search_products_by_sku("0001")
    assert results and results[0]["sku"] == "0001"

def test_search_products_by_sku_not_found():
    assert search_products_by_sku("9999") == []

def test_place_order_success():
    msg = place_order("user1@example.com", "0001", 1)
    assert "Order placed successfully" in msg
    assert len(all_orders) == 1

def test_place_order_user_not_found():
    msg = place_order("nouser@example.com", "0001", 1)
    assert msg == "User not found."

def test_place_order_product_not_found():
    msg = place_order("user1@example.com", "9999", 1)
    assert msg == "Product not found."

def test_place_order_not_enough_stock():
    msg = place_order("user1@example.com", "0001", 9999)
    assert "Not enough stock" in msg

def test_cancel_user_order():
    msg = place_order("user1@example.com", "0001", 1)
    order_id = all_orders[0].order_id
    assert cancel_user_order(order_id) == f"Order {order_id} has been cancelled."

def test_get_user_orders():
    place_order("user1@example.com", "0001", 1)
    orders = get_user_orders("user1@example.com")
    assert len(orders) == 1

def test_check_inventory_found():
    assert "has" in check_inventory("0001")

def test_check_inventory_not_found():
    assert check_inventory("9999") == "Product not found."

def test_reset_inventory_invalid_phrase():
    assert reset_inventory("wrong") == "Invalid command phrase."

def test_reset_inventory_success():
    assert reset_inventory("ido").startswith("Inventory, orders reset")

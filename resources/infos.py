
import os

from infers import UserModel, InventoryModel, OrdersModel, logger
from typing import Any, Dict, List


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
users: List[UserModel] = []
products: List[InventoryModel] = []
all_orders: List[OrdersModel] = [
    # OrdersModel(
    #     order_id="test1234",
    #     user_email="user1@example.com",
    #     sku="0001", 
    #     quantity=1, 
    #     total_price=25.99, 
    #     status="confirmed"
    # )
] 
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("server.log", mode="w"),
        logging.StreamHandler()
    ]
)

class OrdersModel(BaseModel):
    order_id: str
    user_email: str
    sku: str
    quantity: int
    total_price: float
    status: str
    
    
class InventoryModel(BaseModel):
    id: int
    sku: str
    product_name: str 
    category: str
    price: float
    currency: str
    stock_left: int
    availability: str
    description: str
    brand: str
    rating: float
    
class UserModel(BaseModel):
    email: str
    pin: str
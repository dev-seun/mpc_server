from pydantic import BaseModel


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
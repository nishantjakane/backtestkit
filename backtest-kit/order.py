from enum import Enum

class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(Enum):
    LIMIT = "LIMIT" 
    MARKET = "MARKET"

class OrderStatus(Enum):
    FILLED = "FILLED"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"

class Order():
    def __init__(self,order_id,side,order_type,price,qty,status,timestamp):
        self.order_id = order_id
        self.side = side
        self.order_type= order_type 
        self.price = price
        self.qty = qty
        self.status = status
        self.timestamp = timestamp


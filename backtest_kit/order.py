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

    def __init__(self,order_id,side,order_type,price,qty,take_profit,stop_loss,timestamp):
        self.order_id = order_id
        self.side = side
        self.order_type= order_type 
        self.price = price
        self.qty = qty  
        self.take_profit=take_profit
        self.stop_loss=stop_loss
        self.status = OrderStatus.PENDING
        self.timestamp = timestamp
        self.executed_timestamp = None 
    
    def execute(self,candle):
        self.status = OrderStatus.FILLED
        self.executed_timestamp = candle.datetime

    def cancelOrder(self):
        self.status=OrderStatus.CANCELLED


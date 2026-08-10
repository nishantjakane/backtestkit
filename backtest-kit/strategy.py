from order import Order,OrderStatus,OrderType,Side

class Strategy():
    def __init__(self):
        self.order_count =0
        self.history = []
        self.current_candle = None

    def init(self):
        pass

    def on_bar(self,candle):
        return None

    def generate_order_id(self):
        self.order_count+=1
        return self.order_count

    def createOrder(self,side,order_type,price,qty) -> Order:
        return Order(
            self.generate_order_id(),
            side,
            order_type,
            price,
            qty,
            OrderStatus.PENDING,
            timestamp
        )
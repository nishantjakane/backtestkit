from order import Order,OrderStatus,OrderType,Side

class Strategy():
    def __init__(self,engine):
        self.order_count =0
        self.position_count =0
        self.trade_count=0
        self.history = []
        self.current_candle = None
        self.engine = engine

    def init(self):
        pass

    def on_bar(self,candle):
        pass

    def generate_order_id(self):
        self.order_count+=1
        return self.order_count

    def generate_position_id(self):
        self.position_count+=1
        return self.position_count

    def generate_trade_id(self):
        self.trade_count+=1
        return self.trade_count

    def createOrder(self,side,order_type,price,qty) -> Order:
        order = Order(
            self.generate_order_id(),
            side,
            order_type,
            price,
            qty,
            self.current_candle.datetime
        )

        self.engine.submit_order(order)
        
        return order
from data import load_data,Candle,row_to_candle
from order import Side , OrderStatus, OrderType

class Engine:
    def __init__(self,file_path,strategy):
        self.file_path = file_path
        self.strategy = strategy(self)

        self.data = load_data(file_path)
        self.orders = []


    def run(self):
        self.strategy.init()

        for index,row in self.data.iterrows():
            candle = row_to_candle(row)
            
            self.strategy.current_candle = candle
            self.strategy.on_bar(candle)
            self.strategy.history.append(candle)
    
    def submit_order(self,order):
        self.orders.append(order)

    def process_orders(self,candle):
        open = candle.open
        high = candle.high
        low = candle.low
        close = candle.close
        datetime = candle.datetime

        for order in self.orders:
            if order.order_type == OrderType.LIMIT:
                if order.side == Side.BUY:
                    if high >= order.price and low <=order.price:
                        order.status = OrderStatus.FILLED
                if order.side == Side.SELL:
                    if high >= order.price and low <=order.price:
                        order.status = OrderStatus.FILLED
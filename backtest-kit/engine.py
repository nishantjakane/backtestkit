from data import load_data,Candle,row_to_candle
from order import Side , OrderStatus, OrderType
from trade import Trade,Position,ExitType
from enum import Enum

class IntrabarPriority(Enum):
    TP_FIRST="TP_FIRST"
    SL_FIRST="SL_FIRST"

class Engine:
    def __init__(self,file_path,strategy,intrabarpriority=IntrabarPriority.SL_FIRST):
        self.file_path = file_path
        self.strategy = strategy(self)
        self.intrabarpriority=intrabarpriority # TP_FIRST means if in the same candle tp and sl both are triggered this assumes tp is executed first if SL_FIRST then it assumes sl is executed first
        self.data = load_data(file_path)
        self.orders = [] # current active orders
        self.positions = [] # current open positions
        self.trades = [] # completed trades


    def run(self):
        self.strategy.init()

        for index,row in self.data.iterrows():
            candle = row_to_candle(row)
            
            self.process_positions(candle)
            self.process_orders(candle)


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

        orders_to_remove =[]

        for order in self.orders:
            if order.order_type == OrderType.LIMIT:
                if order.side == Side.BUY:
                    if high >= order.price and low <=order.price:
                        order.execute(candle)
                        self.submit_position(order,order.price,datetime)
                        orders_to_remove.append(order)
                elif order.side == Side.SELL:
                    if high >= order.price and low <=order.price:
                        order.execute(candle)
                        self.submit_position(order,order.price,datetime)
                        orders_to_remove.append(order)
        
        for order in orders_to_remove:
            self.orders.remove(order)

    def process_positions(self,candle):
        open = candle.open
        high = candle.high
        low = candle.low
        close = candle.close
        datetime = candle.datetime

        positions_to_remove =[]

        for position in self.positions:
            tp = position.take_profit
            sl = position.stop_loss
            tp_triggered = tp <= high and tp >=low # this triggers only when the price in range of candle
            sl_triggered = sl <= high and sl >=low
            if(not tp_triggered and not sl_triggered):
                continue
                
            if(tp_triggered and sl_triggered):
                if self.intrabarpriority==IntrabarPriority.TP_FIRST:
                    self.submit_trade(position,tp,datetime,ExitType.TP)
                    positions_to_remove.append(position)
                elif self.intrabarpriority==IntrabarPriority.SL_FIRST:
                    self.submit_trade(position,sl,datetime,ExitType.SL)
                    positions_to_remove.append(position)
                continue

            if(tp_triggered):
                self.submit_trade(position,tp,datetime,ExitType.TP)
                positions_to_remove.append(position)
            elif(sl_triggered):
                self.submit_trade(position,sl,datetime,ExitType.SL)
                positions_to_remove.append(position)

        for position in positions_to_remove:
            self.positions.remove(position)


    def submit_position(self,order,entry_price,entry_time):
        position = Position(
            self.strategy.generate_position_id(),
            order,
            entry_price,
            entry_time
        )

        self.positions.append(position)

    def submit_trade(self,position,exit_price,exit_time,exit_type):
        trade = Trade(
            self.strategy.generate_trade_id(),
            position,
            exit_price,
            exit_time,
            exit_type
        )

        self.trades.append(trade)
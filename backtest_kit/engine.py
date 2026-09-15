from backtest_kit.data import load_data,Candle,row_to_candle
from backtest_kit.order import Side , OrderStatus, OrderType
from backtest_kit.trade import Trade,Position,ExitType
from enum import Enum
import pandas as pd

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
        self.market_orders=[] # current market orders


    def run(self):
        self.strategy.init()

        for index,row in self.data.iterrows():
            candle = row_to_candle(row)
            
            self.process_market_orders(candle)
            self.process_positions(candle)
            self.process_orders(candle)


            self.strategy.current_candle = candle
            self.strategy.on_bar(candle)
            self.strategy.history.append(candle)

        return self.trades
    
    def submit_order(self,order):
        if order.order_type == OrderType.LIMIT:
            self.orders.append(order)
        elif order.order_type == OrderType.MARKET:
            order.price = None
            self.market_orders.append(order)

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


    def process_market_orders(self,candle):
        market_order_to_remove =[]
        for order in self.market_orders:
            order.execute(candle)
            self.submit_position(order,candle.open,candle.datetime)
            market_order_to_remove.append(order)

        for order in market_order_to_remove:
            self.market_orders.remove(order)

    def process_positions(self,candle):
        open = candle.open
        high = candle.high
        low = candle.low
        close = candle.close
        datetime = candle.datetime

        positions_to_remove =[]

        for position in self.positions:

            position.update_price(candle)

            tp = position.take_profit
            sl = position.stop_loss
            if tp is None:
                tp_triggered = None
            else:
                tp_triggered = tp <= high and tp >=low # this triggers only when the price in range of candle
            if sl is None:
                sl_triggered = None
            else:
                sl_triggered = sl <= high and sl >=low

            if tp is None and sl is None:
                continue
                 
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

    def close_position(self,candle,position,exit_type):
        trade = Trade(
            self.strategy.generate_trade_id(),
            position,
            candle.close,
            candle.datetime,
            exit_type
        )

        self.positions.remove(position)

        self.trades.append(trade)

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

    def save_trades(self,file_path):
        data = []

        for trade in self.trades:
            data.append({
                "trade_id":trade.trade_id,
                "side":trade.side,
                "qty":trade.qty,
                "entry_price":trade.entry_price,
                "entry_time":trade.entry_time,
                "exit_price":trade.exit_price,
                "exit_time":trade.exit_time,
                "exit_type":trade.exit_type,
                "pct_return":trade.pct_return,
                "pnl":trade.pnl,
                "duration":trade.duration
            })

        df = pd.DataFrame(data)
        df.to_csv(file_path,index=False)

    
    def save_positions(self,file_path):
        data = []

        for position in self.positions:
            data.append({
                "position_id":position.position_id,
                "side":position.side,
                "qty":position.qty,
                "entry_price":position.entry_price,
                "current_price":position.current_price,
                "entry_time":position.entry_time,
                "take_profit":position.take_profit,
                "stop_loss":position.stop_loss,
                "current_pnl":position.current_pnl
            })

        df = pd.DataFrame(data)
        df.to_csv(file_path,index=False)

    def save_orders(self,file_path):
        data = []

        for order in self.orders:
            data.append({
               "order_id":order.order_id,
               "side":order.side,
               "order_type":order.order_type,
               "price":order.price,
               "qty":order.qty,
               "take_profit":order.take_profit,
               "stop_loss":order.stop_loss,
               "status":order.status,
               "timestamp":order.timestamp,
               "executed_timestamp":order.executed_timestamp 
            })

        df = pd.DataFrame(data)
        df.to_csv(file_path,index=False)

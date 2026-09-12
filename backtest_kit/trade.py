from enum import Enum
import datetime as dt
from backtest_kit.order import Side

class ExitType(Enum):
    TP="TP"
    SL="SL"
    SIGNAL="SIGNAL"
    MANUAL="MANUAL"

class Position:
    def __init__(self,position_id,order,entry_price,entry_time):
        self.position_id = position_id
        self.side=order.side
        self.qty=order.qty
        self.entry_price=entry_price
        self.current_price = entry_price
        self.entry_time =entry_time
        self.take_profit=order.take_profit
        self.stop_loss=order.stop_loss
        self.current_pnl = 0


    def update_price(self,candle):
        self.current_price = candle.close
        if self.side == Side.BUY:
            self.current_pnl = (self.current_price-self.entry_price)*self.qty
        elif self.side == Side.SELL:
            self.current_pnl = (self.entry_price-self.current_price)*self.qty
            



class Trade:
    def __init__(self,trade_id,position,exit_price,exit_time,exit_type):
        self.trade_id = trade_id
        self.side= position.side
        self.qty= position.qty
        self.entry_price=position.entry_price
        self.entry_time=position.entry_time
        self.exit_price=exit_price
        self.exit_time=exit_time
        self.exit_type=exit_type
        if self.side == Side.SELL:
            self.pct_return=(self.entry_price-self.exit_price)/self.entry_price
            self.pnl=(self.entry_price-self.exit_price)*self.qty
        elif self.side == Side.BUY:
            self.pct_return=(self.exit_price-self.entry_price)/self.entry_price
            self.pnl=(self.exit_price-self.entry_price)*self.qty
        self.duration=(self.exit_time-self.entry_time).total_seconds() / 60 # duration saved in minutes


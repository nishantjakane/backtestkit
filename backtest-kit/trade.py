from enum import Enum
import datetime as dt

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
    self.entry_time =entry_time
    self.take_profit=order.take_profit
    self.stop_loss=order.stop_loss
    self.current_pnl = 0



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
        self.pct_return=(self.entry_price-self.exit_price)/self.entry_price
        self.pnl=(self.entry_price-self.exit_price)*qty
        self.duration=(exit_time-entry_time).dt.minutes # duration saved in minutes


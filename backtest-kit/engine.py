from data import load_data,Candle,row_to_candle

class Engine:
    def __init__(self,file_path,strategy):
        self.file_path = file_path
        self.strategy = strategy()

        self.data = load_data(file_path)


    def run(self):
        self.strategy.init()

        for index,row in self.data.iterrows():
            candle = row_to_candle(row)
            
            self.strategy.current_candle = candle
            self.strategy.on_bar(candle)
            self.strategy.history.append(candle)
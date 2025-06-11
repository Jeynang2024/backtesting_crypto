
import backtrader as bt



class MovingAverageCrossover(bt.Strategy):
    params =(
        ('short_period',20),
        ('long_period',50),
        ('rsi_period',14),
        ('rsi_overbought',70),
        ('rsi_oversold',30),
        ('stop_loss', 0.02),  
        ('take_profit', 0.05)
    )

    def __init__(self):
        self.short_sma = bt.indicators.MovingAverageSimple(self.data.close,period = self.params.short_period)
        self.long_sma = bt.indicators.MovingAverageSimple(self.data.close,period = self.params.long_period)
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        self.buy_signals = []
        self.sell_signals = []

    def next(self):
        if self.short_sma[0] > self.long_sma[0] and self.rsi[0] < self.params.rsi_oversold:
            
            if not self.position:
                self.buy()

                self.buy_price = self.data.close[0]
                self.buy_signals.append((self.datas[0].datetime.datetime(0), self.datas[0].close[0]))
                print(f"BUY at {self.buy_price}")
        elif self.short_sma[0] < self.long_sma[0] and self.rsi[0] > self.params.rsi_overbought:
            
            if self.position:
                self.sell()
                self.sell_signals.append((self.datas[0].datetime.datetime(0), self.datas[0].close[0]))

                print(f"SELL at {self.data.close[0]}")
        if self.position:
            current_price =self.data.close[0]
            stop_loss_price = self.buy_price*(1-self.params.stop_loss)
            take_profit_price = self.buy_price * (1 + self.params.take_profit)
            if current_price <= stop_loss_price:
                self.sell()
                self.sell_signals.append((self.datas[0].datetime.datetime(0), self.datas[0].close[0]))

                print(f"STOP-LOSS triggered at {current_price}")

            elif current_price >= take_profit_price:
                self.sell()
                self.sell_signals.append((self.datas[0].datetime.datetime(0), self.datas[0].close[0]))

                print(f"TAKE-PROFIT triggered at {current_price}")
# momentum strategy

class MomentumStrategy(bt.Strategy):
    params = (
        ('momentum_period',100),
        ('roc_threshold', 0),
        ('stop_loss', 0.02),  
        ('take_profit', 0.05)
    )

    def __init__(self):
        self.roc = bt.indicators.RateOfChange(self.data.close,period = self.params.momentum_period)
        self.buy_price=None
        self.buy_signals = []
        self.sell_signals = []
    
    def next(self):
        if self.roc[0] > self.params.roc_threshold and not self.position:
            self.buy()
            self.buy_price=self.data.close[0]
            self.buy_signals.append((self.datas[0].datetime.datetime(0), self.datas[0].close[0]))
        elif self.roc[0] < self.params.roc_threshold and self.position:
            self.sell()
            self.sell_signals.append((self.datas[0].datetime.datetime(0), self.datas[0].close[0]))

        if self.position:
            current_price =self.data.close[0]
            stop_loss_price = self.buy_price*(1-self.params.stop_loss)
            take_profit_price = self.buy_price * (1 + self.params.take_profit)
            if current_price <= stop_loss_price:
                self.sell()
                self.sell_signals.append((self.datas[0].datetime.datetime(0), self.datas[0].close[0]))

                print(f"STOP-LOSS triggered at {current_price}")

            elif current_price >= take_profit_price:
                self.sell()
                self.sell_signals.append((self.datas[0].datetime.datetime(0), self.datas[0].close[0]))

                print(f"TAKE-PROFIT triggered at {current_price}")



# Mean Reversion Strategy 
class MeanReversion(bt.Strategy):
    params = (
        ('bollinger_period', 20),
        ('bollinger_dev', 2),
        ('rsi_period', 14),
        ('rsi_oversold', 30),
        ('rsi_overbought', 70),
        ('stop_loss', 0.02),  
        ('take_profit', 0.05)
    )

    def __init__(self):
        self.bollinger = bt.indicators.BollingerBands(self.data.close, period=self.params.bollinger_period, devfactor=self.params.bollinger_dev)
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        self.buy_price=None
        self.buy_signals = []
        self.sell_signals = []

    def next(self):
        if self.data.close[0] < self.bollinger.bot[0] and self.rsi[0] < self.params.rsi_oversold:
            if not self.position:
                self.buy()
                self.buy_price=self.data.close[0]
                self.buy_signals.append((self.datas[0].datetime.datetime(0), self.datas[0].close[0]))


        elif self.data.close[0] > self.bollinger.top[0] and self.rsi[0] > self.params.rsi_overbought:
            if self.position:
                self.sell()
                self.sell_signals.append((self.datas[0].datetime.datetime(0), self.datas[0].close[0]))


        if self.position:
            current_price =self.data.close[0]
            stop_loss_price = self.buy_price*(1-self.params.stop_loss)
            take_profit_price = self.buy_price * (1 + self.params.take_profit)
            if current_price <= stop_loss_price:
                self.sell()
                self.sell_signals.append((self.datas[0].datetime.datetime(0), self.datas[0].close[0]))

                print(f"STOP-LOSS triggered at {current_price}")

            elif current_price >= take_profit_price:
                self.sell()
                self.sell_signals.append((self.datas[0].datetime.datetime(0), self.datas[0].close[0]))

                print(f"TAKE-PROFIT triggered at {current_price}")


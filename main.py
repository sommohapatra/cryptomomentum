import decimal as d
import pandas as pd
from datetime import datetime, timedelta


class BasicTemplateCryptoAlgorithm(QCAlgorithm):
    
    def __init__(self):
    # set the flag for rebalance
        self.reb = 1

    # Number of assets to long/short
        self.num_fine = 8
        
    def Initialize(self):

        self.SetStartDate(2018, 10, 1)  #Set Start Date
        self.SetEndDate(2018, 12, 31)    #Set End Date


        # Set Strategy Cash (USD)
        self.SetCash(10000)


        self.SetBrokerageModel(BrokerageName.Bitfinex, AccountType.Margin)
        
        self.SetBenchmark('BTCUSD')


        tickers = ["BTCUSD", "ETHUSD", "XRPUSD", "LTCUSD", "EOSUSD", "NEOUSD", "XMRUSD", "TRXUSD"]
        # in the alpha version these 8 pairs are hardcoded, but you can feed in an algorithm that scrapes any pair from an exchange


        for ticker in tickers:
            self.AddCrypto(ticker, Resolution.Daily, Market.Bitfinex)
        
        

        # set warmup period
        #self.SetWarmUp(20)
        self.SetWarmUp(timedelta(7))

        # Schedule the rebalance function to execute at the begining of each month (can change this to rebalance weekly or daily)
        self.Schedule.On(self.DateRules.WeekStart(), self.TimeRules.At(12, 0, 0), Action(self.rebalance))

    def OnData(self, data):
        pass
        
    def rebalance(self):
        
        tickers = ["BTCUSD", "ETHUSD", "XRPUSD", "LTCUSD", "EOSUSD", "NEOUSD", "XMRUSD", "TRXUSD"] # again, this is harcoded

        
        df = pd.DataFrame()

        start = datetime(2021, 6, 11)  # you want to change these dates for backtesting
        end = datetime(2021, 6, 11)
       
        # Get historical data from the subscribed assets
       
        h1 = self.History(tickers, start, end, Resolution.Daily)
        
        if h1.empty:
            self.Log("EMPTY dataframe!")
        
        # Resample to 1W timeframe.
        for i in tickers:
            df[i] = h1.loc[i]['close'].resample('W').mean().pct_change()
        
        # Sort the lastrow of dataframe       
        last_week = df.iloc[-1].sort_values(ascending=False)
        
        # Assign the assets to short/long       
        self.long = [last_week.index[0], last_week.index[1], last_week.index[2], last_week.index[3]]
        self.short = [last_week.index[4], last_week.index[5], last_week.index[6], last_week.index[7]]

        # if this month the coins are not going to be long/short, liquidate it.
        self.Liquidate()
        
        # Assign each asset equally. Alternatively you can design your own portfolio construction method
        for i in self.long:
            self.SetHoldings(i, 0.9/self.num_fine)
        
        for i in self.short:
            self.SetHoldings(i, -0.9/self.num_fine)

        self.reb = 1

    def OnOrderEvent(self, orderEvent):
        self.Debug("{} {}".format(self.Time, orderEvent.ToString()))

    def OnEndOfAlgorithm(self):
        self.Log("{} - TotalPortfolioValue: {}".format(self.Time, self.Portfolio.TotalPortfolioValue))
        self.Log("{} - CashBook: {}".format(self.Time, self.Portfolio.CashBook))

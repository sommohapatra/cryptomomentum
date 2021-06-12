%matplotlib inline
# Imports
from clr import AddReference
AddReference("System")
AddReference("QuantConnect.Common")
AddReference("QuantConnect.Jupyter")
AddReference("QuantConnect.Indicators")
from System import *
from QuantConnect import *
from QuantConnect.Data.Custom import *
from QuantConnect.Data.Market import TradeBar, QuoteBar
from QuantConnect.Jupyter import *
from QuantConnect.Indicators import *
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

# Create an instance
qb = QuantBook()


# Select asset data
tickers = ["BTCUSD", "ETHUSD", "XRPUSD", "LTCUSD", "EOSUSD", "NEOUSD", "XMRUSD", "TRXUSD"]

for ticker in tickers:
    qb.AddCrypto(ticker, Resolution.Daily, Market.Bitfinex)

start = datetime(2018, 1, 1)
end = datetime(2018, 12, 31)

# Gets historical data from the subscribed assets, the last 360 datapoints with daily resolution
h1 = qb.History(qb.Securities.Keys, start, end, Resolution.Daily)

# Plot closing prices from asset 
h1.loc["NEOUSD"]["close"].plot()

import numpy as np
rate_return = 102.0/100 - 1
print(rate_return)

import pandas as pd

#df = pd.DataFrame(tickers, columns=['Name'])

x = 0
for i in tickers:
    rate_return = (h1.loc[i]["close"][0] / h1.loc[i]["close"][6]) - 1
    print(i+" "+str(rate_return))
    #df['rate_return'] = rate_return
    x += 1
    
fine_nr = len(tickers)

df = pd.DataFrame()


for i in tickers:
    df[i] = h1.loc[i]['close'].resample('W').mean().pct_change()

last_week = df.iloc[-1].sort_values(ascending=False)

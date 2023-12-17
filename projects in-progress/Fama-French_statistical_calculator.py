#  Fama-French three factor model proposed by Eugene Fama and Kenneth French to describe stock returns.
#     It uses additional risk factors besides market risk to interpret asset returns and calculate an estimated or expected return required for adding the asset to ones portfolio

#     MKT = the excess return of the market over the risk-free rate. 
#         Basically, the additional return required to invest in an asset exposed to market and credit risk versus one exposed to none.

#     SMB = Small minus Big; the idea is to measure the excess return of small cap stocks over larger cap stocks
#         Basically, the additional return required to invest in an asset larger than the large caps

#     HML = High minus Low; it measures the excess return of value stocks (those with high book to price ratio) over growth stock (high price to book)
#         Basically, the additional return required to invest in an asset based on its value despite lower growth 
#         opportunities vs the growth stocks that boast a risky but attainable high return

#     Five Factor Fama-French adds RMW and CMA
#     RMW = Robust minus Wea and measures the excess returns


import pandas as pd
import numpy as np
import yfinance as yf
import statsmodels.api as sm
import getFamaFrenchFactors as gff
import datetime as dt
from datetime import timedelta
from pandas_datareader import data as pdr

#Model Format --> R3 = 3-Factor model ; R5 = 5-Factor model

    # R3 = a + Bm * (MKT) + Bs * (SMB) + Bh * (HML)
    # R5 = a + Bm * (MKT) + Bs * (SMB) + Bh * (HML) + Br * (RMW) + Bc * (CMA)


# #Set the ticker to the desired company
### rolling + input settings - data begins 5 years back from today and ends 30 days from today

ticker = input("Enter ticker symbol here: ")

now=dt.datetime.now()
today = dt.datetime.today()
yesterday = today - timedelta(days=1)

start = today - timedelta(days=1825)
end = today - timedelta(days=30)

#
# 
### manual date settings
# ticker = 'msft'
# start = '2016-8-31'
# end = '2022-8-31'


stock_data = yf.download(ticker, start, end, adjusted = True)

ff3_monthly = gff.famaFrench3Factor(frequency = 'm')
ff3_monthly.rename(columns={"date_ff_factors": 'Date'}, inplace = True)
ff3_monthly.set_index('Date', inplace = True)

###################################SETUP ABOVE, WORK BELOW##############################################################################

#Calculation of the stock's historical monthly returns
        #first we extract the adjusted close prices from the stock data and resample them into monthly prices. Adj close is a column in the stock_data command via yfinance
            #We're resampling them into monthly prices by setting a parameter "M" to the resammple function
        #Next we're using the pct_change function to calculate the % change of the last price of monthly data compared to the previous month. Hence, our stock return
stock_returns = stock_data['Adj Close'].resample('M').last().pct_change().dropna()
stock_returns.name = "Month_Rtn"
ff_data = ff3_monthly.merge(stock_returns, on = 'Date')

#Calculation of the Betas
        #we'll use the Fama-French benchmark data from the imported fama-french packages above
        #first we're extracting the required Fama-French benchmark data from the columns Mkt-RF, SMB, and HML and assigning the extracted data series to X
        #next, we subtract the risk free rate out of the historical monthly return to get the equity risk premium
        #then we use the add_constant function to add a constant to X, on a graphic just imagine the number 1 assigned to every row value of X
X = ff_data[['Mkt-RF' ,'SMB', 'HML']]
Y = ff_data['Month_Rtn'] - ff_data['RF']
X = sm.add_constant(X)
ff_model = sm.OLS(Y, X).fit()
print(ff_model.summary())
intercept, b1, b2, b3 = ff_model.params


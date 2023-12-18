import pandas as pd
import numpy as mp
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
from datetime import timedelta

yf.pdr_override()

stock = input("Enter stock ticker symbol: ")
print(stock)

startyear=2018
startmonth=1
startday=1
start=dt.datetime(startyear,startmonth,startday)
end = dt.datetime(2020,1,9)
now = dt.datetime.now()
today = dt.datetime.today()
yesterday = today - timedelta(days=1)

dfcompletestockdata = pdr.get_data_yahoo(stock,)
dfstockdata = pdr.get_data_yahoo(stock, start, end)

rangema = int(input('desired moving average range? (## format): '))
# rangema=50

smaString = "Sma_"+str(rangema)
# names the simple moving average based on the range desired

dfstockdata[smaString]=dfstockdata.iloc[:,4].rolling(window=rangema).mean()
# adds the simple moving average desired as a field (the fourth field from the right, adj close here),
# calculating based on each adj close for every date/row

question = input("do you have a desired date to return? (yes/no): ")
def macalculator(question): 
    if question == "yes":
        qdesireddate = input("enter desired date in yyyy-mm-dd format (ex: 2019-05-08): ")
        answer = dfstockdata.loc[qdesireddate,smaString]
        return "simple moving average on "+ qdesireddate +" for " + stock + " is " + str(answer)
    else:
        question2 = input("do you have a desired date range? (yes/no): ")
        if question2 == "yes":
            qdesiredstartdate = input("enter desired start date in yyyy-mm-dd format: ")
            qdesiredenddate = input("enter desired end date in yyyy-mm-dd format): ")
            answer = dfstockdata.loc[qdesiredstartdate:qdesiredenddate,smaString]
            print("simple moving average between ", qdesiredstartdate , " and " , qdesiredenddate, ":\n", answer)
        else:
            lastsma = float(dfcompletestockdata.iloc[-1][5])
            return "no dates given, so here is the latest " + str(rangema) + " day simple moving average : " + str(lastsma)
        

print(macalculator(question))


dfrangema = dfstockdata.iloc[rangema:] 

numH = 0
numC = 0
for i in dfrangema.index:
    if(dfrangema["Adj Close"][i]>dfrangema[smaString][i]):
        numH+=1
    else:
        numC+=1

print("# of days in the full moving average range where the sma > adj close: ",str(numH))
print("# of days in the full moving average range where the sma < adj close: ",str(numC))
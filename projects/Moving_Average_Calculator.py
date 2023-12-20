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

dfstockdata = pdr.get_data_yahoo(stock,)

rangema = int(input('desired moving average range? (## format): '))
# rangema=50

smaString = "Sma_"+str(rangema)
ewmaString = "EWMA_"+str(rangema)
# names the simple and exponentially-weighted moving averages based on the range desired

dfstockdata[smaString]=dfstockdata.iloc[:,4].rolling(window=rangema).mean()
dfstockdata[ewmaString]=dfstockdata.iloc[:,4].ewm(span=rangema, adjust=False).mean()

print(dfstockdata)

# adds the simple and exponentially-weighted moving averages desired as a field (the fourth field from the right, adj close here),
# calculating based on each adj close for every date/row


datequestion = 0

def smacalculator(datequestion): 
    datequestion = input("do you have a desired date to return? (yes/no): ")
    if datequestion == "yes":
        qdesireddate = input("enter desired date in yyyy-mm-dd format (ex: 2019-05-08): ")
        answer = dfstockdata.loc[qdesireddate,smaString]
        return "simple moving average on "+ qdesireddate +" for " + stock + " is " + str(answer)
    else:
        datequestion2 = input("do you have a desired date range? (yes/no): ")
        if datequestion2 == "yes":
            qdesiredstartdate = input("enter desired start date in yyyy-mm-dd format: ")
            qdesiredenddate = input("enter desired end date in yyyy-mm-dd format): ")
            answer = dfstockdata.loc[qdesiredstartdate:qdesiredenddate,smaString]
            return "simple moving average between " + qdesiredstartdate + " and " + qdesiredenddate + ":\n" + answer
        else:
            lastsma = float(dfstockdata.iloc[-1][5])
            return "no dates given, so here is the latest cd" + str(rangema) + " day simple moving average : " + str(lastsma)
        
def ewmacalculator(datequestion): 
    datequestion = input("do you have a desired date to return? (yes/no): ")
    if datequestion == "yes":
        qdesireddate = input("enter desired date in yyyy-mm-dd format (ex: 2019-05-08): ")
        answer = dfstockdata.loc[qdesireddate,ewmaString]
        return "exponentially weighted moving average on "+ qdesireddate +" for " + stock + " is " + str(answer)
    else:
        datequestion2 = input("do you have a desired date range? (yes/no): ")
        if datequestion2 == "yes":
            qdesiredstartdate = input("enter desired start date in yyyy-mm-dd format: ")
            qdesiredenddate = input("enter desired end date in yyyy-mm-dd format): ")
            answer = dfstockdata.loc[qdesiredstartdate:qdesiredenddate,ewmaString]
            return "exponentially weighted moving average between "+ qdesiredstartdate + " and " + qdesiredenddate+ ":\n"+ answer
        else:
            lastewma = float(dfstockdata.iloc[-1][6])
            return "no dates given, so here is the latest " + str(rangema) + " day exponentially weighted moving average : " + str(lastewma)

def bothmacalculator(datequestion): 
    datequestion = input("do you have a desired date to return? (yes/no): ")
    if datequestion == "yes":
        qdesireddate = input("enter desired date in yyyy-mm-dd format (ex: 2019-05-08): ")
        answersma = dfstockdata.loc[qdesireddate,smaString]
        answerewma = dfstockdata.loc[qdesireddate,ewmaString]
        return "simple moving average on "+ qdesireddate +" for " + stock + " is " + str(answersma) + "\n" + "exponentially weighted moving average on "+ qdesireddate +" for " + stock + " is " + str(answerewma)
    else:
        datequestion2 = input("do you have a desired date range? (yes/no): ")
        if datequestion2 == "yes":
            qdesiredstartdate = input("enter desired start date in yyyy-mm-dd format: ")
            qdesiredenddate = input("enter desired end date in yyyy-mm-dd format): ")
            answersma = dfstockdata.loc[qdesiredstartdate:qdesiredenddate,smaString]
            answerewma = dfstockdata.loc[qdesiredstartdate:qdesiredenddate,ewmaString]
            return "simple moving average between "+ qdesiredstartdate + " and " + qdesiredenddate+ ":\n"+ answersma + "\n" "exponentially weighted moving average between ", qdesiredstartdate , " and " , qdesiredenddate, ":\n", answerewma
        else:
            lastsma = float(dfstockdata.iloc[-1][6])
            lastewma = float(dfstockdata.iloc[-1][7])
            return "no dates given, so here is the latest " + str(rangema) + " day simple moving average : " + str(lastsma) + "\n"+ "and here is the latest "+ str(rangema) + " day exponentially weighted moving average : " + str(lastewma)

def askitagainloop():
    while  True:
        ewmaorsma = input("exponentially-weighted moving average or simple moving average? (enter ewma or sma or both): ")
        if ewmaorsma not in ['sma','ewma','both']:
            print("invalid response, enter ewma or sma or both, otherwise I'll loop all day")
            continue
        elif ewmaorsma == "sma":
            print(smacalculator(datequestion))
            break
        elif ewmaorsma == "ewma":
            print(ewmacalculator(datequestion))
            break
        else:
            print(bothmacalculator(datequestion))
            break

askitagainloop()

# as of 12/19/2023
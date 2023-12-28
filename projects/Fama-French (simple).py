
# Fama-French Three Factor Model with simple correlation based factor coefficient

# The betas (bERP, bSMB, bHML, etc.) are used as the factor coefficients. For now, they're simple correlations between the subject stock price and the factor representative share price 

#     MKT = the excess return of the market over the risk-free rate. 
#         Basically, the additional return required to invest in an asset exposed to market and credit risk versus one exposed to none.

#     SMB = Small minus Big; the idea is to measure the excess return of small cap stocks over larger cap stocks
#         Basically, the additional return required to invest in an asset larger than the large caps

#     HML = High minus Low; it measures the excess return of value stocks (those with high book to price ratio) over growth stock (high price to book)
#         Basically, the additional return required to invest in an asset based on its value despite lower growth 
#         opportunities vs the growth stocks that boast a risky but attainable high return



import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import statsmodels.api as sm
yf.pdr_override()
from sklearn.linear_model import LinearRegression
from datetime import timedelta
from pandas_datareader import data as pdr

now=dt.datetime.now()
today = dt.datetime.today()
yesterday = today - timedelta(days=1)

target_stock = 'MSFT'

months_invhorizon = input("Enter your investment horizon in months: ")
rf = float(input("Enter your risk-free rate: "))
invhorizon = int(months_invhorizon) * 30

start = today - timedelta(days=invhorizon*2)
end = today - timedelta(days=5)


### Equity Risk Premium

ERP_ticker = 'SPY'
# ERP_ticker = input("Enter ticker representing broad market return: ")
ERP_input = [ERP_ticker, target_stock]
df_ERP=pdr.get_data_yahoo(ERP_input,start,now)['Adj Close']

Rmkt_return="mkt_return"
target_return="target_return"
df_ERP[Rmkt_return]=df_ERP.iloc[:,0].pct_change(invhorizon)
df_ERP[target_return]=df_ERP.iloc[:,1].pct_change(invhorizon)

df_cov_ERP=df_ERP.cov()

cov_ERP = df_cov_ERP.iat[len(df_cov_ERP)-1,df_cov_ERP.columns.get_loc('mkt_return')]

var_mkt = df_ERP['mkt_return'].var()

Rmkt=df_ERP.iat[len(df_ERP)-1,df_ERP.columns.get_loc('mkt_return')]
ERP = float(Rmkt) - rf

bERP = float(cov_ERP) / float(var_mkt)
print('ERP beta: ',bERP,'ERP: ',ERP)


CAPM = rf + bERP*(ERP)
print('CAPM expected return = ',CAPM)

### Small minus Big Premium

smallcap_ticker = 'VB'
largecap_ticker = 'VV'
# smallcap_ticker = input("Enter the small cap equity return's representative ticker: ")
# largecap_ticker = input("Enter the large cap equity return's representative ticker: ")


SMB_input = [smallcap_ticker, largecap_ticker , target_stock]
df_SMB=pdr.get_data_yahoo(SMB_input,start,now)['Adj Close']

SMB_return = "SMB_return"
smallcap_return = "smallcap_return"
largecap_return = "largecap_return"
df_SMB[smallcap_return]=df_SMB.iloc[:,0].pct_change(invhorizon)
df_SMB[largecap_return]=df_SMB.iloc[:,1].pct_change(invhorizon)
df_SMB[target_return]=df_SMB.iloc[:,2].pct_change(invhorizon)
df_SMB[SMB_return]=df_SMB[smallcap_return] - df_SMB[largecap_return]

SMB=df_SMB.iat[len(df_SMB)-1,df_SMB.columns.get_loc('SMB_return')]



df_cov_SMB=df_SMB.cov()
cov_SMB = df_cov_SMB.iat[len(df_cov_SMB)-2,df_cov_SMB.columns.get_loc('SMB_return')]

var_SMB = df_SMB['SMB_return'].var()
bSMB = float(cov_SMB) / float(var_SMB)

print('SMB beta: ',bSMB,'SMB: ',SMB)

r2 = rf + bERP*(ERP) + bSMB*(SMB)

print('two factor expected return: ',r2)

### High minus Low Premium

highBTM_ticker = 'VTV'
lowBTM_ticker = 'VUG'
# highBTM_ticker = input("Enter the high book to market return's representative ticker: ")
# lowBTM_ticker = input("Enter the low book to market return's representative ticker: ")


HML_input = [highBTM_ticker, lowBTM_ticker , target_stock]
df_HML=pdr.get_data_yahoo(HML_input,start,now)['Adj Close']

HML_return = "HML_return"
highBTM_return = "highBTM_return"
lowBTM_return = "lowBTM_return"
df_HML[highBTM_return]=df_HML.iloc[:,0].pct_change(invhorizon)
df_HML[lowBTM_return]=df_HML.iloc[:,1].pct_change(invhorizon)
df_HML[target_return]=df_HML.iloc[:,2].pct_change(invhorizon)
df_HML[HML_return]=df_HML[highBTM_return] - df_HML[lowBTM_return]

HML=df_HML.iat[len(df_HML)-1,df_HML.columns.get_loc('HML_return')]



df_cov_HML=df_HML.cov()
cov_HML = df_cov_HML.iat[len(df_cov_HML)-2,df_cov_HML.columns.get_loc('HML_return')]

var_HML = df_HML['HML_return'].var()
bHML = float(cov_HML) / float(var_HML)

print('HML beta: ',bHML,'HML: ',HML)

r3 = rf + bERP*(ERP) + bSMB*(SMB) + bHML*(HML)





print('Three Factor expected return: ',r3)

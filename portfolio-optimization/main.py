#Portfolio Optimization: Selecting the best stocks

from pandas_datareader import data as web
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Get the tickers in the portfolio with FAANG companies
assets = ['FB','AMZN','AAPL','NFLX','GOOG']
#Assign weights to the stocks in the portfolio
weights=np.array([0.2,0.2,0.2,0.2,0.2]) #equal weight
#Get the portfolio starting date and ending date (today)
stockStartDate = '2013-01-01' #First full year for FB
today = datetime.today().strftime('%Y-%m-%d')

#Create a dataframe to store the adjusted close price of the stocks
df = pd.DataFrame()
#Store the adjusted close price of the stock into the df
df = web.DataReader(name=assets, data_source='yahoo', start=stockStartDate, end=today)['Adj Close']
#print(df)

# VISUALISATION
title = 'Portfolio Adj. Close Price History'
#Get the stocks
my_stocks=df
#Plot the graph
for c in my_stocks.columns.values:
    plt.plot(my_stocks[c],label=c)
plt.title(title)
plt.xlabel('Date',fontsize=18)
plt.ylabel('Adj. Price in USD ($)',fontsize=18)
plt.legend(my_stocks.columns.values,loc='upper left')
#plt.show()

# CALCULATIONS
#Show the daily simple return
returns=df.pct_change()
#Show the annualized covariance matrix
cov_matrix_annual = returns.cov()*252  # number of trading days a year
#Calculate the portfolio variance
port_variance = np.dot(weights.T, np.dot(cov_matrix_annual, weights))
#print(port_variance)
#Calculate the portfolio volatility (std)
port_volatility = np.sqrt(port_variance)
#print(port_volatility)
#Calculate the annual portfolio return
portfolioSimpleAnnualReturn = np.sum(returns.mean()*weights)*252
#print(portfolioSimpleAnnualReturn)

#Show the expected annual return, volatility, and variance
percent_var = str(round(port_variance,2)*100)+'%'
percent_vols = str(round(port_volatility,2)*100)+'%'
percent_ret = str(round(portfolioSimpleAnnualReturn,2)*100)+'%'
print('Expected annual return: '+percent_ret)
print('Annual volatility: '+percent_vols)
print('Annual variange: '+ percent_var)

# USING PYPORTFOLIO OPT
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

# PORTFOLIO OPTIMIZATION

#Calculate the expected returns and the annualised sample covariance matrix of asset returns
mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)
#Optimise for max sharpe ratio
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()  #Any weights below some cut off
#print(cleaned_weights)
ef.portfolio_performance(verbose = True)

#Get the allocation of each share per stock
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

latest_prices = get_latest_prices(df)
weights = cleaned_weights
da = DiscreteAllocation(weights,latest_prices,total_portfolio_value=15000) # Dummy number
allocation, leftover = da.lp_portfolio()
print('Discrete allocation: ', allocation)
print(f'Funds remaning:${leftover}')

from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np 
from datetime import datetime


START_DATE='28-01-2015'
END_DATE=str(datetime.now().strftime('%d-%m-%y'))



UK_STOCK = 'UU.L'
USA_STOCK='AMZN'

def get_stats(stock_data):
	return {
	'last':np.mean(stock_data.tail(1)),
	'short_mean': np.mean(stock_data.tail(20)),
	'long_mean': np.mean(stock_data.tail(500)),
	'short_rolling': stock_data.rolling(window=20).mean(),
	'long_rolling': stock_data.rolling(window=200).mean()
	
	
	
	}

def create_plot(stock_data, ticker):
	stats = get_stats(stock_data)
	plt.style.use('dark_background')
	plt.subplots(figsize=(12,8))
	plt.plot(stock_data, label=ticker)
	plt.plot(stats['short_rolling'],label='20 day rolling mean')
	plt.plot(stats['long_rolling'],label='200 day rolling mean')
	plt.xlabel('Date')
	plt.ylabel('Adj Close (p)')
	plt.legend()
	plt.title('stock price over time')


	plt.show()


def clean_data(stock_data, col):
	weekdays = pd.date_range(start=START_DATE, end = END_DATE)
	clean_data = stock_data[col].reindex(weekdays)
	return clean_data.fillna(method='ffill')



def get_data(ticker):
	try:
		stock_data = data.DataReader(ticker,
			                        'yahoo',
			  						START_DATE,
									END_DATE)

		adj_close = clean_data(stock_data,'Adj Close')
		create_plot(adj_close,ticker)

	except RemoteDataError:
		print('No data found for {t}'.format(t=ticker))



if __name__ ==  "__main__":
	get_data(UK_STOCK)
     
    
  
	

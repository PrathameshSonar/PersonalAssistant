

import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd 
import pandas_datareader as web
import numpy as np 
from datetime import datetime


def get_stock():
	style.use("ggplot")
	START_DATE='28-01-2015'
	END_DATE=str(datetime.now().strftime('%d-%m-%y'))
	df = web.get_data_yahoo("AAPL",START_DATE,END_DATE)
	df2 = web.get_data_yahoo("TSLA",START_DATE,END_DATE)
	df3 = web.get_data_yahoo("MSFT",START_DATE,END_DATE)
	df["Adj Close"].plot(color="red")
	df2["Adj Close"].plot(color="yellow")
	df3["Adj Close"].plot(color="blue")
	plt.show()
	print("Apple"+"is red"+"Tesla"+"yellow"+"Microsoft id"+"blue")

if __name__ ==  "__main__":
	get_stock()



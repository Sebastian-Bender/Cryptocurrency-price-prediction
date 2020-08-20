import pandas as pd
import requests
import time
import datetime
import math

def get_data(coin, date):
	"""Helper-function. Gets the data from the cryptocompare api

	Parameters
	----------
	coin : str
		Symbol of the coin to request (eg BTC for Bitcoin)
	date : str
		start date

	Returns
	-------
	ipdata : dict
		column : value
	"""
	today = datetime.datetime.now().date()
	date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
	days = (today - date).days
	if days <= 0:
		days = 1
	
	url = f"https://min-api.cryptocompare.com/data/histoday?fsym={coin}&tsym=USD&limit={days}"
	r = requests.get(url)
	ipdata = r.json()
	return ipdata

def get_trimmed_dataframe(coin, date):
	"""Gets the data from the get_data function and returns a dataframe
	that contains only the needed columns

	Parameters
	----------
	coin : str
		Symbol of the coin to request (eg BTC for Bitcoin)
	date : str
		start date

	Returns
	-------
	df : DataFrame
		DataFrame containing the needed columns
	"""
	df = pd.DataFrame(get_data(coin, date)['Data'])
	df.time = pd.to_datetime(df.time, unit = 's')
	df.set_index('time', inplace=True)
	df[f'{coin}_value'] = df[['close', 'high', 'low', 'open']].mean(axis = 1)
	df.rename(columns={'volumeto' : f'{coin}_volume'}, inplace=True)
	return df[[f'{coin}_value', f'{coin}_volume']]

def get_forex_dataframe(symbol, date):
	"""Gets the data from the exchangeratesapi API and returns a dataframe.

	Parameters
	----------
	symbol : str
		Symbol of the currency to request (eg EUR for Euro)
	date : str
		start date

	Returns
	-------
	df : DataFrame
		DataFrame containing the exchange rates from USD to (symbol) per day starting from (date)
	"""
	safedDate = date
	date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
	oneDay = datetime.timedelta(days = 1)
	today = datetime.datetime.now().date()
	
	start = (date - oneDay - oneDay).strftime('%Y-%m-%d')
	end = today.strftime('%Y-%m-%d')

	url = f"https://api.exchangeratesapi.io/history?start_at={start}&end_at={end}&base=USD&symbols={symbol}"
	r = requests.get(url)
	hist_rates = r.json()

	rates_by_date = hist_rates['rates']
	# Convert the dictionary into desired format
	hist_data = []
	for key, value in rates_by_date.items():
		hist_dict = {'date': key, symbol: value[symbol]}
		hist_data.append(hist_dict)

	hist_data.sort(key = lambda x:x['date'])

	df = pd.DataFrame.from_dict(hist_data)
	
	df.rename(columns={'date' : 'time'}, inplace=True)
	df.set_index('time', inplace=True)
	idx = pd.date_range(start, end)

	df.index = pd.DatetimeIndex(df.index)
	df = df.reindex(idx)

	df[symbol] = df[symbol].interpolate(method='slinear').interpolate(method='linear')
	df = df.round(5)
	df = df[df.index <= end]
	return df[df.index >= safedDate]

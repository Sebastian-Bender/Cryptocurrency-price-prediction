import pandas as pd
import requests
import time
import datetime
import math

def days_since_last_update(date):
	today = datetime.datetime.now().date()
	date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
	days = (today - date).days
	if days == 0:
		return 1
	return days

def get_data(coin, date):
	days = days_since_last_update(date)
	url = f"https://min-api.cryptocompare.com/data/histoday?fsym={coin}&tsym=USD&limit={days}"
	r = requests.get(url)
	ipdata = r.json()
	return ipdata

def get_trimmed_dataframe(coin, date):
	df = pd.DataFrame(get_data(coin, date)['Data'])
	df.time = pd.to_datetime(df.time, unit = 's')
	df.set_index('time', inplace=True)
	df[f'{coin}_value'] = df[['close', 'high', 'low', 'open']].mean(axis = 1)
	df.rename(columns={'volumeto' : f'{coin}_volume'}, inplace=True)
	return df[[f'{coin}_value', f'{coin}_volume']]

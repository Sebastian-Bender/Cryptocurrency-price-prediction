import pandas as pd
import sqlalchemy
import pymysql
import datetime

import apiController
from apiController import get_trimmed_dataframe

def connectDB():
	"""Connects to the database with the login information contained
	in the login_DB.txt.
	Returns
	-------
	engine
		sqlalchemy engine
	"""
	with open('login_DB.txt') as f:
		lines = f.read().splitlines()
	engine = sqlalchemy.create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user = lines[0], pw = lines[1], db = lines[2]))

	return engine

def closeDB(conn, engine):
	"""Closes the connection to the database.
	Parameters
	----------
	conn
	engine
	"""
	conn.close()
	engine.dispose()
	print('DB connection has been closed')


def updateDB():
	"""Updates the coin_data table in the database

	Returns
	-------
	returnStr : str
		information on what has been updated
	"""
	returnStr = ''
	engine = connectDB()

	conn = engine.connect()
	metadata = sqlalchemy.MetaData()
	coin_data = sqlalchemy.Table('coin_data', metadata, autoload = True, autoload_with=engine)

	query = sqlalchemy.select([coin_data]).order_by(sqlalchemy.desc(coin_data.columns.time)).limit(1)
	result = conn.execute(query).fetchall()

	if result == []:
		bitcoin = get_trimmed_dataframe('BTC', '2017-01-01')
		ethereum = get_trimmed_dataframe('ETH', '2017-01-01')
		litecoin = get_trimmed_dataframe('LTC', '2017-01-01')
		ripple = get_trimmed_dataframe('XRP', '2017-01-01')
		
		coinDF = pd.concat([bitcoin, ethereum, litecoin, ripple], axis=1)

		coinDF.to_sql('coin_data', con = engine, if_exists='append', chunksize = 1000)

		returnStr =  'DB has successfully been initiated with values since 2017-01-01'
	else:
		date = str(result[0][0])
		bitcoin = get_trimmed_dataframe('BTC', date)
		ethereum = get_trimmed_dataframe('ETH', date)
		litecoin = get_trimmed_dataframe('LTC', date)
		ripple = get_trimmed_dataframe('XRP', date)
		
		coinDF = pd.concat([bitcoin, ethereum, litecoin, ripple], axis=1)
		
		# get previously saved rows that may be outdated
		coinDF_list = coinDF.index.tolist()
		coinDF_list = [x.date().strftime('%Y-%m-%d') for x in coinDF_list]
		
		# delete outdated data
		engine.execute(f"DELETE FROM coin_data WHERE time in {tuple(coinDF_list)}")

		# update DB with new data
		coinDF.to_sql('coin_data', con = engine, if_exists='append', chunksize = 1000)
		
		returnStr =  f'Updated DB from {date} - today'
	
	closeDB(conn, engine)
	return returnStr

def readDB():
	"""Reads the coin_data table in the database

	Returns
	-------
	df : pandas DataFrame
		DataFrame with all entries of the coin_data table
	"""
	engine = connectDB()
	conn = engine.connect()

	df = pd.read_sql('SELECT * FROM coin_data', con = engine)
	df.set_index('time', inplace=True)
	closeDB(conn, engine)
	return df

def updateDB_forex():
	"""Updates the forex_data table in the database

	Returns
	-------
	returnStr : str
		information on what has been updated
	"""
	returnStr = ''
	engine = connectDB()
	conn = engine.connect()
	metadata = sqlalchemy.MetaData()
	forex_data = sqlalchemy.Table('forex_data', metadata, autoload = True, autoload_with=engine)

	query = sqlalchemy.select([forex_data]).order_by(sqlalchemy.desc(forex_data.columns.time)).limit(1)
	result = conn.execute(query).fetchall()
	if result == []:
		eur = apiController.get_forex_dataframe('EUR', '2017-01-01')
		chf = apiController.get_forex_dataframe('CHF', '2017-01-01')
		cad = apiController.get_forex_dataframe('CAD', '2017-01-01')

		forex = pd.concat([eur, chf, cad], axis=1)
		forex.index.name = 'time'
		forex.to_sql('forex_data', con = engine, if_exists='append', chunksize = 1000)

		returnStr =  'forex DB has successfully been initiated with values since 2017-01-01'
	else:
		print(result[0][0])
		date = result[0][0] + datetime.timedelta(days = 1)

		if date >= datetime.datetime.now().date():
			closeDB(conn, engine)
			return 'Forex DB already up to date'
		date = date.strftime('%Y-%m-%d')

		eur = apiController.get_forex_dataframe('EUR', date)
		chf = apiController.get_forex_dataframe('CHF', date)
		cad = apiController.get_forex_dataframe('CAD', date)

		forex = pd.concat([eur, chf, cad], axis=1)
		forex.index.name = 'time'
		forex.to_sql('forex_data', con = engine, if_exists='append', chunksize = 1000)
		
		returnStr = f'Updated forex DB from {date} - today'
	
	closeDB(conn, engine)
	return returnStr

def readDB_forex():
	"""Reads the forex_data table in the database

	Returns
	-------
	df : pandas DataFrame
		DataFrame with all entries of the forex_data table
	"""
	engine = connectDB()
	conn = engine.connect()

	df = pd.read_sql('SELECT * FROM forex_data', con = engine)
	df.set_index('time', inplace=True)
	closeDB(conn, engine)
	return df

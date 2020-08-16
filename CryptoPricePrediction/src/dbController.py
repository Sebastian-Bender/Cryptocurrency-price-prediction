import pandas as pd
import sqlalchemy
import pymysql
import datetime

import apiController
from apiController import get_trimmed_dataframe

def connectDB():
	with open('login_DB.txt') as f:
		lines = f.read().splitlines()
	engine = sqlalchemy.create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user = lines[0], pw = lines[1], db = lines[2]))

	return engine

def closeDB(conn, engine):
	conn.close()
	engine.dispose()
	print('DB connection has been closed')


def updateDB():
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
	engine = connectDB()
	conn = engine.connect()

	df = pd.read_sql('SELECT * FROM coin_data', con = engine)

	closeDB(conn, engine)
	return df

def updateDB_forex():
	returnStr = ''
	engine = connectDB()
	conn = engine.connect()
	metadata = sqlalchemy.MetaData()
	forex_data = sqlalchemy.Table('forex_data', metadata, autoload = True, autoload_with=engine)

	query = sqlalchemy.select([forex_data]).order_by(sqlalchemy.desc(forex_data.columns.time)).limit(1)
	result = conn.execute(query).fetchall()
	
	eur = apiController.get_forex_dataframe('EUR', '2017-01-01')
	chf = apiController.get_forex_dataframe('CHF', '2017-01-01')
	cad = apiController.get_forex_dataframe('CAD', '2017-01-01')

	forex = pd.concat([eur, chf, cad], axis=1)
	forex.to_sql('forex_data', con = engine, if_exists='append', chunksize = 1000, index=False)

	returnStr =  'forex DB has successfully been initiated with values since 2017-01-01'
	
	closeDB(conn, engine)
	return returnStr

	closeDB(conn, engine)

def readDB_forex():
	engine = connectDB()
	conn = engine.connect()

	df = pd.read_sql('SELECT * FROM forex_data', con = engine)

	closeDB(conn, engine)
	return df
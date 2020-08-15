CREATE DATABASE CryptoCurrencies;
USE CryptoCurrencies;

CREATE TABLE coin_data (
	time date NOT NULL PRIMARY KEY, 
    BTC_value decimal(20,2), 
    BTC_volume bigint, 
    ETH_value decimal(20,2), 
    ETH_volume bigint, 
    LTC_value decimal(20,2), 
    LTC_volume bigint, 
    XRP_value decimal(20,2), 
    XRP_volume bigint);
    

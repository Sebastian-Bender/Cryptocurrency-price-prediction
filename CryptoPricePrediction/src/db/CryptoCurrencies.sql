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

    
CREATE TABLE forex_data (
	id bigint NOT NULL PRIMARY KEY AUTO_INCREMENT,
	time date, 
    EUR decimal(10, 5), 
    CHF decimal(10, 5), 
    CAD decimal(10, 5));
    
UPDATE forex_data
SET time = DATE_ADD("2016-12-31", INTERVAL id DAY);

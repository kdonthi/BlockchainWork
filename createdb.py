import sqlite3

db = sqlite3.connect("exchangerate.db")
cursor = db.cursor()
cursor.execute("""DROP TABLE IF EXISTS nexchange""") #remove when actually running program
cursor.execute("""CREATE TABLE IF NOT EXISTS nexchange
(
	public_key_base_64 string,
	public_key_base_16 string,
	epoch_start_time string,
	epoch_end_time string,
	epoch_start_time_unix int,
	epoch_number integer,
	avg_eth_dollar_exchange_rate string,
	max_eth_dollar_exchange_rate string,
	min_eth_dollar_exchange_rate string,
	change_in_balance_eth real,
	change_in_balance_dollar real,
	correlation_timestamp string,
	PRIMARY KEY (public_key_base_64, epoch_number)
)""")

cursor.execute("""DROP TABLE IF EXISTS percentAdded""")
cursor.execute("""CREATE TABLE IF NOT EXISTS percentAdded
(
	epoch_number integer,
	num_addresses_from_scraper integer,
	addresses_successfully_added integer
)""")
db.close()

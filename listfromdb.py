import sqlite3
import sys
import time
from datetime import datetime
import calendar
import logging

try:
	import balance.priceoverepoch as priceoverepoch
	import balance.mergesort as mergesort
	import balance.basesixtyfour as basesixtyfour
	import balance.successfulValidators as successfulValidators
	import poloniex_interface.price as price
except ImportError as e:
	import priceoverepoch
	import mergesort
	import basesixtyfour
	import successfulValidators
	sys.path.append('..')
	from poloniex_interface import price
	#print(e)
"""Running this file uses two command line arguments,
	python3 listfromdb.py [first time] [number of validators to get data from]
	If it is your first time, use 1 for the "first time" argument. Otherwise, use 0.
	The second one is optional - if you have a specific number of validators you would like to check, type it in. Otherwise, it will just check the amount of unique validators scraped."""

def getKeysAndReturnCursor():
	# Path to database is different depending on where the script is called
	try:
		db = sqlite3.connect("../etherscan_scraper/etherscan_data.db")
	except sqlite3.OperationalError as e:
		db = sqlite3.connect("./etherscan_scraper/etherscan_data.db")

	cursor = db.cursor()
	if len(sys.argv) == 1:
		cursor.execute("SELECT COUNT(DISTINCT(validator_public_key_base_64)) FROM transactions")
		numberOfKeys = cursor.fetchall()[0][0]
		cursor.execute("SELECT DISTINCT validator_public_key_base_64, validator_public_key_base_16 FROM transactions") #add limit if you want to check quickly
	elif len(sys.argv) >= 2:
		assert(len(sys.argv) == 2)
		assert((sys.argv[1]).isnumeric())
		numberOfKeys = sys.argv[1]
		cursor.execute("SELECT DISTINCT validator_public_key_base_64, validator_public_key_base_16 FROM transactions LIMIT %i" % (int(sys.argv[1])))
	listobj = cursor.fetchall()
	db.close()

	# Path to database is different depending on where the script is called
	try:
		db2 = sqlite3.connect("./balance/exchangerate.db")
	except sqlite3.OperationalError as e:
		db2 = sqlite3.connect("exchangerate.db")


	cursor2 = db2.cursor()
	dictOfIds = {}
	for i in listobj:
		dictOfIds.update({i[0]: i[1]})
	return (cursor2, dictOfIds, db2, int(numberOfKeys))


def insertIntoDb(epochnum:str, avgExchangeRate:str, minExchangeRate:str, maxExchangeRate:str, startOfEpoch:str, endOfEpoch:str, startofEpochUnix:str, endoOfEpochUnix: str, sortedLists:list, correlationTime:str, cursor):
	insertList = []
	for i in sortedLists:
		changeInEth = i[1]
		structTime = time.strptime(startOfEpoch, "%Y-%m-%dT%H:%M:%SZ")
		unixTime = calendar.timegm(structTime)
		insertList.append((i[0][0], i[0][1], startOfEpoch, endOfEpoch, unixTime, epochnum, avgExchangeRate, minExchangeRate, maxExchangeRate, changeInEth, changeInEth * avgExchangeRate, correlationTime))
	cursor.executemany("""INSERT OR IGNORE INTO nexchange (public_key_base_64, public_key_base_16, epoch_start_time, epoch_end_time, epoch_start_time_unix, epoch_number,
	avg_eth_dollar_exchange_rate, min_eth_dollar_exchange_rate, max_eth_dollar_exchange_rate, change_in_balance_eth, change_in_balance_dollar, correlation_timestamp)
	VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", insertList)

def removeComma(publicKey : tuple) -> str:
	""" Removes the comma and beginning characters that come with the public key in the database."""
	newkey = publicKey[0].replace(",","")
	newkey = newkey.replace("0","",1)
	newkey = newkey.replace("x","",1)
	return (newkey)

def epochStartTime(epochNumber:str) -> int:
	""" Converting our timestamp in YYYY-MM-DDTHH:MM:SSZ format to the Unix format to find the start of the epoch. """
	epochStart = priceoverepoch.startofcurrentepoch(epochNumber)
	datetimeobject = datetime.strptime(epochStart, "%Y-%m-%dT%H:%M:%SZ")
	return (calendar.timegm(datetimeobject.timetuple())) #time.mktime assumes local time

def epochEndTime(epochNumber:str) -> int:
	""" Converting our timestamp in YYYY-MM-DDTHH:MM:SSZ format to the Unix format to find the end of the epoch - approximating the end of an epoch as the start of the next epoch. """
	epochEnd = priceoverepoch.startofcurrentepoch(str(int(epochNumber) + 1))
	datetimeobject = datetime.strptime(epochEnd, "%Y-%m-%dT%H:%M:%SZ")
	return calendar.timegm(datetimeobject.timetuple())

def avgMinAndMaxExchangeRate(epochNumber:str) -> (int,int,int):
	return (price.getPrice("USDT_ETH", epochStartTime(epochNumber), epochEndTime(epochNumber)))

def runProgram(firstTime:int):
	assert(firstTime == 1 or firstTime == 0)
	if firstTime == 1: #use this if this is the first time
		firstEpoch = priceoverepoch.headEpochNumber()
		epoch = firstEpoch
		while (firstEpoch == epoch):
			epoch = priceoverepoch.headEpochNumber()
		print("Epoch we entered at: " + str(firstEpoch) + ", epoch we are in now: " + str(epoch))
		logging.info(f"Epoch we entered at: {firstEpoch}, epoch we are in now: {epoch}")
		return (None)
	elif firstTime == 0:
		cursor, dictOfIds, connection, numberOfKeys = getKeysAndReturnCursor()
		listOfIds = mergesort.dictToListOfLists(dictOfIds)
		amountReturnedFromAPI = 0
		increment = 500
		amount = len(listOfIds) #last index will be len - 1
		start = 0
		end = increment
		starttime = time.time()
		wrongcalls = 0
		for k in range((amount//increment) + 1):
			dictofbalances = {}
			listOfIndices = []
			if end > amount:
				end = amount
			for j in range(start,end):
				listOfIndices.append(listOfIds[j])
			dictOfIndices = mergesort.listOfListsToDict(listOfIndices)
			if k == 0:
				a,d,e = priceoverepoch.diffOverEpoch(dictOfIndices, dictofbalances, 1)
			else:
				a,d,e = priceoverepoch.diffOverEpoch(dictOfIndices, dictofbalances, 0)
			if k == 0:
				startnum = a
			start += increment
			end += increment
			listOfLs = mergesort.dictToListOfLists(dictofbalances)
			sortedLists = mergesort.mergesort(listOfLs)
			amountReturnedFromAPI += len(sortedLists)
			#only calculate these anew when it is the first call
			if k == 0:
				exchangeRate, minExchangeRate, maxExchangeRate = avgMinAndMaxExchangeRate(a)
				startOfEpoch = priceoverepoch.startofcurrentepoch(a)
				endOfEpoch = priceoverepoch.startofcurrentepoch(str(int(a) + 1))
				startOfEpochUnix = epochStartTime(a)
				endOfEpochUnix = epochEndTime(a)
			if a != startnum: #if our epoch number changes, stop the iterating
				break
			if e == 1:
				insertIntoDb(a, exchangeRate, minExchangeRate, maxExchangeRate, startOfEpoch, endOfEpoch, startOfEpochUnix, endOfEpochUnix, sortedLists, d, cursor)
			else:
				wrongcalls += 1
		endtime = time.time()
		print("Time taken: " + str(round(endtime - starttime, 3)) + " seconds")

		print("Epoch #%s Added" % (startnum))
		print("Epoch ended on: %s" % (a))
		print("Number of keys given: " + str(numberOfKeys))
		print("Number of keys gotten from API: " + str(amountReturnedFromAPI))
		print("Success Rate: " + str(round(((amountReturnedFromAPI / numberOfKeys) * 100),2)) + "%")
		print("Faulty calls: " + str(wrongcalls))

		# Logging
		logging.info(f"Epoch #{startnum} Added")
		logging.info(f"Keys given: {numberOfKeys}")
		logging.info(f"Keys gotten from API: {amountReturnedFromAPI}")
		logging.info(f"Success Rate: {round(((amountReturnedFromAPI / numberOfKeys) * 100),2)}%")
		logging.info(f"Faulty calls: {wrongcalls}")

		connection.commit()
		connection.close()
		successfulValidators.insertTotalAndSuccessfullyAdded(startnum, numberOfKeys, amountReturnedFromAPI)


def main():
	counter = 0
	while True:
		if counter == 0:
			runProgram(1)
		else:
			runProgram(0)
		counter += 1
		print()
		"""
		try:
			db = sqlite3.connect("exchangerate.db")
		except sqlite3.OperationalError as e:
			db = sqlite3.connect("./balance/exchangerate.db")

		#cursor = db.cursor()

		#cursor.execute("SELECT * FROM nexchange")
		#for i in cursor.fetchall():
			#print(i)
		"""
if __name__ == "__main__":
	main()

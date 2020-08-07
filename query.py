""" Functions to:
1) Produce a list of transactions for an address in base16 ("0x..." included),
2) Produce a list of the transaction for an address in a given unix timeframe,
and 3) Given a unix time frame, rank the top changes in balance in a given time frame."""

import sqlite3
import sys
sys.path.append("..")
from balance import listfromdb
from balance import basesixtyfour
#except ImportError:
#	import listfromdb
#	import basesixtyfour
import time
import calendar

db = sqlite3.connect("exchangerate.db")
cursor = db.cursor()

def formatTimeToUnixTime(formattedTime:str) -> int:
	"""Converts the UTC time in "%Y-%m-%dT%H:%M:%SZ" format to seconds from the epoch (January 1, 1970, 00:00:00 (UTC))"""
	struct = time.strptime(formattedTime, "%Y-%m-%dT%H:%M:%SZ")
	return calendar.timegm(struct)

def listOfTransactions(publicKey:str):
	#tuplepublickey = (publicKey, 0)
	#a = basesixtyfour.baseSixteenToSixtyFour(listfromdb.removeComma(tuplepublickey))
	cursor.execute("SELECT * FROM nexchange WHERE public_key_base_16='%s'" % (publicKey))
	for i in cursor.fetchall():
		print(i)

def listOfTransactionsInWindow(publicKey:str, startTime:str, endTime:str):
	""" Returns the transactions with the start of its epoch in a given window of time, given by startTime and endTime. The time parameters
	are accepted in the format Y-m-dTH:M:SZ and the publicKey should be in a base16 format"""
	#tuplepublickey = (publicKey, 0)
	#a = basesixtyfour.baseSixteenToSixtyFour(listfromdb.removeComma(tuplepublickey))
	startTimeUnix = formatTimeToUnixTime(startTime)
	endTimeUnix = formatTimeToUnixTime(endTime)
	cursor.execute("SELECT * FROM nexchange WHERE public_key_base_16 = '%s' AND epoch_start_time_unix >= %i AND epoch_start_time_unix <= %i" % (publicKey, startTimeUnix, endTimeUnix))
	for i in cursor.fetchall():
		print(i)

def rankingValidatorDeltas(startTime:str, endTime:str, number:int):
	startTimeUnix = formatTimeToUnixTime(startTime)
	endTimeUnix = formatTimeToUnixTime(endTime)
	assert(endTimeUnix > startTimeUnix)
	cursor.execute("""SELECT public_key_base_16, SUM(change_in_balance_dollar) FROM nexchange WHERE epoch_start_time_unix >= %i AND epoch_start_time_unix <= %i
					GROUP BY public_key_base_16 ORDER BY SUM(change_in_balance_dollar) DESC LIMIT %i""" % (startTimeUnix, endTimeUnix, number))
	for i in cursor.fetchall():
		print(i)


if __name__ == "__main__":
	#listOfTransactions("0x94d3093ad6d99fbcce936be1dc01ed86179a6d7d27c7bb4589f65530debcfeff8af1e60f47275208d52b0ea33fe799ba")
	#cursor.execute("SELECT * FROM nexchange LIMIT 10")
	#for i in cursor.fetchall():
		#pass
		#print(i)
	#listOfTransactionsInWindow("0x94d3093ad6d99fbcce936be1dc01ed86179a6d7d27c7bb4589f65530debcfeff8af1e60f47275208d52b0ea33fe799ba", "2020-08-05T00:43:00Z", "2020-08-05T00:51:34Z")
	#listOfTransactions("0x97e3e035cd2b2c87a36cc83fff1359503a47b90ecd7f0573cbe920521b10c027867059d668e8d09c0368700d76260588")
	rankingValidatorDeltas("2020-08-05T00:40:20Z", "2020-08-05T01:57:34Z", 100)
	db.close()

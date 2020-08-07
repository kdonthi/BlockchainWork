import requests
import sqlite3
import time
try:
	import balance.mergesort
except ModuleNotFoundError:
	import mergesort
import sys
import json

def datenot(num:int) -> str:
	"""
	This function converts a number into a string and adds a zero at the front if it is only one digit long.
	It is meant to be used for single digit months, days, hours, minutes, and seconds when making date notation.
	"""
	strnum = str(num)
	if len(strnum) == 1:
		strnum = "0" + strnum
	return (strnum)
def daysinmonth(month: int, year: int) -> int:
	"""
	Gives the number of days in a month given the month and the year.
	 """
	if month == 2 and year % 4 == 0:
		return (29)
	elif month == 2:
		return (28)
	elif month <= 7 and month % 2 == 0:
		return (30)
	elif month <= 7:
		return (31)
	elif month > 7 and month % 2 == 0:
		return (31)
	elif month > 7:
		return (30)
def headEpochNumber() -> str:
	headEpochUrl = "https://api.prylabs.net/eth/v1alpha1/beacon/chainhead"
	req2 = 0
	epochurlres = 0
	while req2 != 200:
		epochon = 0
		try:
			epochon = requests.get(headEpochUrl)
		except requests.ConnectionError:
			req2 = 0
		if epochon:
			req2 = epochon.status_code
		try:
			epochurlres = epochon.json()
		except (json.decoder.JSONDecodeError, AttributeError):
			req2 = 0
	return (epochurlres["headEpoch"])

def genesisTimeCall():
	genesistimeurl = "https://api.prylabs.net/eth/v1alpha1/node/genesis"
	req3 = 0
	genesisurlres = 0
	while req3 != 200:
		genesis = 0
		try:
			genesis = requests.get(genesistimeurl)
		except requests.ConnectionError:
			req3 = 0
		if genesis: #only there when response = 200!?!
			req3 = genesis.status_code
		try:
			genesisurlres = genesis.json()
		except (json.decoder.JSONDecodeError, AttributeError):
			req3 = 0
	return (genesisurlres["genesisTime"])

def startofcurrentepoch(epochnumber:str) -> str:
	"""
	Calculates the start time of the epoch you give, given the epoch number as a string.
	"""
	genesistime = genesisTimeCall()
	seconds = 32 * 12 * int(epochnumber) #do we need to do for month?
	sinday = 24 * 60 * 60
	sinhour = 60 * 60
	sinminute = 60
	daystoadd = seconds // sinday
	seconds -= (daystoadd * sinday)
	hourstoadd = seconds // sinhour
	seconds -= (hourstoadd * sinhour)
	minutestoadd = seconds // sinminute
	seconds -= (minutestoadd * sinminute)
	secondstoadd = seconds
	year = int(genesistime[0:4])
	month = int(genesistime[5:7])
	day = int(genesistime[8:10])
	hour = int(genesistime[11:13])
	minutes = int(genesistime[14:16])
	seconds = int(genesistime[17:19])
	if seconds + secondstoadd >= 60:
		minutes += 1
	seconds = (seconds + secondstoadd) % 60
	if minutes + minutestoadd >= 60:
		hour += 1
	minutes = (minutes + minutestoadd) % 60
	if hour + hourstoadd >= 24:
		day += 1
	hour = (hour + hourstoadd) % 24
	addtomonth = 0
	if day + daystoadd > daysinmonth(month, year):
		addtomonth = 1 #don't change the month before we use in daysinmonth fn
	day = (day + daystoadd) % (daysinmonth(month,year) + 1)
	if addtomonth == 1:
		day += 1 #because days of month start from 0, not 1
		month += 1
	datestring = ""
	datestring += str(year) + "-" + datenot(month) + "-" + datenot(day) + "T" + datenot(hour) + ":" + datenot(minutes) + ":" + datenot(seconds) + "Z"
	return datestring

def diffOverEpoch(dictOfKeys:dict, dictofdiffs:dict, isfirstcall:int):
	"""
	This function gives us the change in balance before and after an epoch transition. It takes in a listofKeys (public keys) and a dictionary in which to store the Indices as keys and the change in balances as values.
	By passing in 0 to the 3rd parameter when it is not your first call and 1 when it is your first call, you can get the epochnumber before the first call and after your last one to make sure that you are getting data
	within the same epoch.
	"""
	balanceurl = "https://api.prylabs.net/eth/v1alpha1/validators/performance"
	listOfKeys = [i for i in dictOfKeys]
	#print(listOfKeys)
	params = {
		"publicKeys": listOfKeys,
		#"indices": [1],
	}
	statuscode = 0
	while statuscode != 200:
		response = 0
		try:
			response = requests.get(balanceurl, params, timeout=7)
		except (requests.ConnectionError, requests.exceptions.ReadTimeout, requests.exceptions.Timeout, requests.exceptions.ConnectTimeout) as e:
			statuscode = 0
		if response:
			statuscode = response.status_code
		try:
			balanceurlres = response.json()
		except (json.decoder.JSONDecodeError, AttributeError):
			statuscode = 0
	timestamp = time.gmtime(time.time())
	structtime = time.strftime("%Y-%m-%dT%H:%M:%SZ",timestamp)
	publicKeysInvolved = (balanceurlres['publicKeys'])
	balanceAfter = (balanceurlres['balancesAfterEpochTransition'])
	balanceBefore = (balanceurlres['balancesBeforeEpochTransition'])
	valid = 1
	if len(publicKeysInvolved) != len(balanceAfter) or len(publicKeysInvolved) != len(balanceBefore):
		print("Number of publicKeys does not match number of balances")
		valid = 0
	listofbalances = zip(balanceAfter, balanceBefore)
	#listindex = 0
	if isfirstcall == 1:
		epochnumbermone = str(int(headEpochNumber()) - 1)
	for counter,balances in enumerate(listofbalances):
		publicKey = publicKeysInvolved[counter]
		dictofdiffs.update({(publicKey, dictOfKeys[publicKey]) : ((int(balances[0]) - int(balances[1])) * 10 ** -9)})
		#listindex += 1
	if isfirstcall == 0:
		epochnumbermone = str(int(headEpochNumber()) - 1)
	return (epochnumbermone, structtime, valid)


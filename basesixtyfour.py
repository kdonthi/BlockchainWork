baseSixteenDict = {}
for i in range(10):
	baseSixteenDict.update({str(i):i})
for i in range(6):
	diff = ord("a")
	baseSixteenDict.update({chr(i + diff) : i + 10})
#print(baseSixteenDict) works!

def powersOfSixteen(power:int) -> int: #works!
	total = 1
	for i in range(power):
		total *= 16
	return (total)

#def baseSixteenDigitConverter(character:str)->str:

def baseSixteenToTen(publicKey:str) -> int:
	power = 0
	totalInBaseTen = 0
	for i in range(len(publicKey) - 1, -1, -1):
		totalInBaseTen += baseSixteenDict[publicKey[i]] * powersOfSixteen(power)
		power += 1
	return (totalInBaseTen)
#print(baseSixteenToTen(str('ADEF'))) #looks like it works!
baseSixtyFourDict = {}
for i in range(26):
	ucdiff = ord('A')
	baseSixtyFourDict.update({i : chr(i + ucdiff)})
for i in range(26, 52):
	lcdiff = ord('a') - 26
	baseSixtyFourDict.update({i : chr(i + lcdiff)})
for i in range(52, 62):
	numdiff = ord('0') - 52
	baseSixtyFourDict.update({i : chr(i + numdiff)})
baseSixtyFourDict.update({62 : "+"})
baseSixtyFourDict.update({63 : "/"})

def baseTenToSixtyFour(number:int, listofl : list) -> list:
	if number >= 64:
		baseTenToSixtyFour(number // 64, listofl)
	listofl.append(baseSixtyFourDict[(number % 64)])

def baseSixteenToSixtyFour(string : str) -> str:
	baseTen = baseSixteenToTen(string)
	stringi = []
	baseTenToSixtyFour(baseTen, stringi)
	baseSixtyFour = ''.join(stringi)
	return(baseSixtyFour)

if __name__ == "__main__":
	print(baseSixteenToSixtyFour('1045'))

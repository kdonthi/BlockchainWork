""" Assuming that everyone has the same probablity of becoming a validator, can we confirm that validators are indeed randomly chosen?"""

"""ideas: 1) take a list of 100 random validators and see their chance of being a validator over all the epochs. Do this 100 times. (Doesn't account for addition/removal of validators.))
2) Get 10 random validators from each epoch and see how any of them are validators."""

import sqlite3

db = sqlite3.connect("exchangerate.db")
c = db.cursor()
def etheriumRandomness(threshold:float):
	#c.execute("SELECT DISTINCT(change_in_balance_eth) FROM nexchange ORDER BY change_in_balance_eth DESC")
	#for i in c.fetchall():
		#print(i)
	#exit()
	c.execute("SELECT DISTINCT(public_key_base_64) FROM nexchange ORDER BY RANDOM() LIMIT 20")
	setOfValidators = {i[0] for i in c.fetchall()}
	c.execute("SELECT DISTINCT(epoch_number) FROM nexchange")
	listOfEpochNumbers = [i[0] for i in c.fetchall()]
	amountInCommon = 0
	for i in listOfEpochNumbers:
		c.execute("""SELECT public_key_base_64,change_in_balance_eth FROM nexchange WHERE epoch_number=%i AND
		change_in_balance_eth >= %f""" % (i, threshold))
		setOfValidatorsAboveThreshold = {i[0] for i in c.fetchall()}
		intersection = setOfValidators.intersection(setOfValidatorsAboveThreshold)
		amountInCommon += len(intersection)
	averageIntersection = amountInCommon / len(listOfEpochNumbers)
	averagePercentIntersection = (averageIntersection / len(setOfValidators)) * 100
	#print("Avg percent of random 100 picked as validators across epochs: " + str(averagePercentIntersection))
	return(averagePercentIntersection)

def main():
	sumOfPercentValidators = 0
	threshold = 7.5 * 10 ** -5
	trials = 100
	for i in range(trials):
		sumOfPercentValidators = sumOfPercentValidators + etheriumRandomness(threshold)
	print("Avg. Percent of Validators Over Threshold: " + str(round(sumOfPercentValidators / trials, 3)) + "%")


	c.execute("SELECT COUNT(DISTINCT(epoch_number)) FROM nexchange")
	amountOfEpochs = c.fetchall()[0][0]
	c.execute("SELECT COUNT(*) FROM nexchange")
	avgTransactionsPerEpoch = c.fetchall()[0][0] / amountOfEpochs
	print("Estimated Percent of Proposers: " + str(round(32 / avgTransactionsPerEpoch * 100,3)) + "%")
	db.close()

if __name__ == "__main__":
	main()

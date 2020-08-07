import sqlite3

def insertTotalAndSuccessfullyAdded(epochNumber:int, totalForEpoch:int, successfullyAdded:int):
	""" Inserts the amount of successfully added validators and the total amount of validators given for each epoch."""
	db = sqlite3.connect("exchangerate.db")
	c = db.cursor()

	c.execute("INSERT INTO percentAdded (epoch_number, num_addresses_from_scraper, addresses_successfully_added) VALUES (?,?,?)",  \
	(epochNumber, totalForEpoch, successfullyAdded))
	db.commit()
	db.close()

if __name__ == "__main__":
	insertTotalAndSuccessfullyAdded(9100, 30000, 10)
	db = sqlite3.connect("exchangerate.db")
	c = db.cursor()
	c.execute("SELECT * FROM percentAdded")
	for i in c.fetchall():
		print(i)
	db.close()

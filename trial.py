import sqlite3

db = sqlite3.connect("database.db")
c = db.cursor()
c.execute("DROP TABLE IF EXISTS bob")
#c.execute("DROP TABLE IF EXISTS table")
c.execute("""CREATE TABLE IF NOT EXISTS bob
(name string,
number int,
year int,
PRIMARY KEY (name, number))
""")

listofnames = [
	('kaushik', 5, 2019),
	('maria', 5, 2019),
	('jane', 3, 2019),
	('tom', 3, 2019),
	('maria', 3, 2020),
	('kaushik', 3, 2020),
	('jane', 5, 2020),
	('tom', 5, 2020)
]

c.executemany("INSERT OR IGNORE INTO bob (name,number,year) VALUES (?,?,?)", listofnames)
c.execute("SELECT * FROM bob")
for i in c.fetchall():
	print(i)
print()
c.execute("SELECT DISTINCT(name) FROM bob ORDER BY RANDOM() LIMIT 2")
setOfValidators = {i[0] for i in c.fetchall()}
print(setOfValidators)
c.execute("SELECT AVG(COUNT(DISTINCT(name))) FROM bob GROUP BY year")
print(c.fetchall())
exit()
listOfYears = [i[0] for i in c.fetchall()]
amountIntersected = 0
threshold = 4
exit()
for i in listOfYears:
	c.execute("SELECT * FROM bob WHERE year=%i AND number>%i" % (i, threshold))
	setOfValuesAboveThreshold = {i[0] for i in c.fetchall()}
	intersection = setOfValuesAboveThreshold.intersection(setOfValidators)
	amountIntersected += len(intersection)
print("Average percent of validators chosen to propose: " + str((amountIntersected/len(listOfYears))/len(setOfValidators) * 100) + "%")
#shift+tab tabs backwards!

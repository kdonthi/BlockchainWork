#def merge(to, from1, from2):

#def mergesort(array):
"""
Program to sort list of lists by values, highest at the beginning
"""
dictofnums = {1:3, 2:7, 3:4, 5:10}
def dictToListOfLists(dictionary:dict):
	listoftuples = list(dictionary.items())
	return ([list(i) for i in listoftuples])

def listOfListsToDict(listoflists:list):
	#listoftuples = [tuple(i) for i in listoflists]
	return (dict(listoflists))

def splitdict(listoflists:list): #works, even for dict of len 2
	list1 = []
	list2 = []
	lendict = len(listoflists)
	counter = 0
	for i in listoflists:
		if (counter < (lendict / 2)):
			list1.append(i)
		else:
			list2.append(i)
		counter += 1
	return list1, list2

def merge(to:list, from1:list, from2:list) -> list:
	l1c = 0
	l2c = 0
	toc = 0
	while toc < len(to): #if toc < len(to), we have at least one more thing to add?!
		if l1c == len(from1):
			to[toc] = from2[l2c]
			l2c += 1
		elif l2c == len(from2):
			to[toc] = from1[l1c]
			l1c += 1
		elif from1[l1c][1] > from2[l2c][1]:
			to[toc] = from1[l1c]
			l1c += 1
		elif from2[l2c][1] >= from1[l1c][1]:
			to[toc] = from2[l2c]
			l2c += 1
		toc += 1
	return (to)

def mergesort(listoflists:list) -> list:
	if not listoflists:
		return (listoflists)
	split1, split2 = splitdict(listoflists)
	if (len(listoflists) != 1):
		merge(listoflists, mergesort(split1), mergesort(split2))
	return(listoflists)

if __name__ == "__main__":
	dictofnums = {1:3, 2:7, 3:4, 5:10}
	thelistofls = dictToListOfLists(dictofnums)
	print(thelistofls)
	#print(listofListstoDicct(thelistofls))
	split1 = splitdict(thelistofls)[0]
	split2 = splitdict(thelistofls)[1]
	#print(split1, split2)
	print(merge(thelistofls,split1, split2))
	print(mergesort(dictToListOfLists(dictofnums)))

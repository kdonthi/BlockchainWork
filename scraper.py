import requests
from bs4 import BeautifulSoup

url = "https://algoexplorer.io/transactions"
page = requests.get(url)
content = page.content
soup = BeautifulSoup(content, "html5lib")
listOfElements = soup.find_all('a', class_="value link-primary with--trunc-large")
dictOfHashes = {}
for i in listOfElements:
	dictOfHashes.update({i.get_text() : []})
	newUrl = "https://algoexplorer.io/tx/{}".format(i.get_text())
	newPage = requests.get(newUrl)
	newContent = newPage.content
	newSoup = BeautifulSoup(newContent, "html5lib")
	idAndTimeStamp = newSoup.find_all('span', class_ = "paper-value small value blue with-trunc-intern")
	sendAndReceiver = newSoup.find_all('a', class_="detail with-trunc--large link-primary under")
	amount = newSoup.find('span', class_ = "values-details with-algo with-trunc--large")
	dictOfHashes[i.get_text()].append(idAndTimeStamp[1].get_text())
	dictOfHashes[i.get_text()].append(sendAndReceiver[0].get_text())
	dictOfHashes[i.get_text()].append(sendAndReceiver[1].get_text()) #order is time, sender, receiver, amount
	dictOfHashes[i.get_text()].append(amount.get_text())
print(dictOfHashes)

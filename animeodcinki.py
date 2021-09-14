import requests
from bs4 import BeautifulSoup
odcinki=list()
ilosc=0
odtwarzacze = list()
strona=requests.get("https://anime-odcinki.pl/anime/ghost-in-the-shell-1995")
zupka=BeautifulSoup(strona.text, 'html.parser')
def listepizodes():
	for a in zupka.find_all("li", {"class":"lista_odc_tytul_pozycja"}):
		for b in a.find_all("a"):
			odcinki.append({
				"name": b.get_text()
				"link": b["href"]
				})
			ilosc+=1
	print(tytuly, linki)
	return odcinki
def listplayers():
for i in odcinki:
	odtwarzacze.append(BeautifulSoup(requests.get(i).text, 'html.parser'))

for i in odtwarzacze:
	print(i.find_all("iframe"))
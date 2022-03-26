from bs4 import BeautifulSoup as zupka
import requests
def cda(adres):
	episodes = []
	stronka = requests.get(adres).text
	zupa = zupka(stronka)
	linki = zupa.find_all('a',{'class': 'link-title-visit'})
	for i in linki:
		episodes.append({'title':str(i.get_text()), 'player': str('https://cda.pl'+i['href'])})
	return episodes
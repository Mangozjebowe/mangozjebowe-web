import requests
from bs4 import BeautifulSoup as zupka
def desu(link):
	nazwa = link.replace('https://desu-online.pl/anime/','').replace('/','')
	zupa = zupka(requests.get(link).text, 'html.parser')
	odcinki = []
	print("nazwa anime: ",nazwa)
	for i in zupa.find_all('a'):
		try:
			if nazwa in i['href'] and '-odcinek-' in i['href']:
				odcinki.append({
					'title': i.find('div', {'class':'epl-title'}).get_text(),
					'player': i['href'] 
					})
				print(i['href'])
		except:
			None
	# print(odcinki)
	for i in range(len(odcinki)):
		zupa = zupka(requests.get(odcinki[i]['player']).text)
		odcinki[i]['player'] = zupa.find('iframe')['src']
	return odcinki
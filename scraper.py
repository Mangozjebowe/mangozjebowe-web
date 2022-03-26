from __main__ import *
enabled_plugins = ['cda', 'wbijam', 'desu']
for i in enabled_plugins:
	exec('from scrapery.'+i+' import '+i+'')
import json
# from scrapery.cda import cda
import requests
animeDB = json.load(open('anime-offline-database.json','r',encoding='UTF-8'))['data']

def getMetaData(title):
	# print("TYTUŁ TYTUŁ TYTUŁ ",title)
	responseDB = {}
	for i in animeDB:
		if title.upper() in i['title'].upper():
			responseDB = i
		else:
			for j in i['synonyms']:
				if title.upper() in j.upper():
					responseDB = i
	response = requests.get("https://api.jikan.moe/v3/search/anime?q="+str(title).replace(' ',"%20")).json()
	print(response.keys())
	response = response['results'][0]
	responseDB.update(response)
	# print(responseDB)
	return(responseDB)
def scrap(link, title):
	for i in enabled_plugins:
		if i in link:
			# print("'"+link+"'")
			episodes = eval((i+'('+'"'+link+'"'+')'))
			return({
				'Episodes': episodes,
				'Metadata': getMetaData(title)
			})

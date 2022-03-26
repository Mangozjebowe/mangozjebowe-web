from scraper import scrap
import json

result = scrap('https://www.cda.pl/klub-inferno/folder/33507767', 'neon genesis evangelion')
# plik = open('result.json', 'w')
print('Klucze result',result.keys())
print('Klucze Episodes',result['Episodes'])

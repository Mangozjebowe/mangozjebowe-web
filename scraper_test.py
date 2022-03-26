from scraper import scrap
import json
def test_cda():
	#given
	url = 'https://www.cda.pl/klub-inferno/folder/33707223'
	title = 'Yakusoku no Neverland'
	#when
	result = scrap(url, title)
	#then
	assert len(result['Episodes']) > 0
def test_wbijam():
	#given
	url = 'https://goh.wbijam.pl/pierwsza_seria.html'
	title = 'The God of High School'
	#when
	result = scrap(url, title)
	#then
	assert len(result['Episodes']) > 0
	assert 'The God of High School' in result['Metadata']['title']

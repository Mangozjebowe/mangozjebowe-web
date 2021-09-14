returndicts = list()
import requests
from bs4 import BeautifulSoup
names=list()
# mega vk sibnet cda vidlox mp4up
player = 'cda'
filename = "/dev/null"
def get_episode_page_url(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    links = []
    for link in soup.find_all('table', class_='lista'):
        for a in link.find_all('a', href=True):
            names.append(a.get_text())
            links.append(baseURL + a['href'])
    links.reverse()
    names.reverse()
    # print(links)
    return links


def get_player_page_url(links, player_name):
    urls = []
    if len(links) > 0 and player_name:
        for link in links:
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html.parser')
            players = soup.find('table', class_='lista')
            player = players.find('td', text=player_name)
            # print(player)
            if player is not None:
                player = player.find_parent('tr')
                playerURL = f"{baseURL}odtwarzacz-{player.find('span', class_='odtwarzacz_link')['rel']}.html"
                urls.append(playerURL)
        # print(urls)
    return urls


def get_player_url(links):
    urls = []
    if len(links) > 0:
        for link in links:
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html.parser')
            urls.append(soup.find('iframe')['src'])
    return urls


def save_file(filename, links):
    with open(filename, 'w') as file:
        file.write('\n'.join(links))


# episode_page_urls = get_episode_page_url(page)
# player_page_urls = get_player_page_url(episode_page_urls, player)
# players = get_player_url(player_page_urls)
# save_file(filename, players)

def wbijam(adres):
    URL = adres
    global baseURL
    baseURL = f"{URL.split('wbijam.pl/', 1)[0]}wbijam.pl/"
    page = requests.get(URL)
    episode_page_urls = get_episode_page_url(page)
    player_page_urls = get_player_page_url(episode_page_urls, player)
    players = get_player_url(player_page_urls)
    save_file(filename, players)
    try:
        returndicts.clear()
        # episode_page_urls.clear()
        # player_page_urls.clear()
    except:
        None
    for i in range(len(players)):
        returndicts.append({
        "name": names[i],
        "player": players[i]
        })
        print(names[i], players[i])

    return returndicts
# print(players)
import requests
from bs4 import BeautifulSoup

def fetch(game):
    url = f"https://gg.deals/game/{game}/?tab=bundles"
    data = requests.get(url)
    soup= BeautifulSoup(data.text,'html.parser')
    lis = soup.find('div', class_='title-line')
    try:
        bundle = lis.text
    except Exception:
        bundle = ''
    return bundle


#games = []
#with open('gam_2020.txt','r',encoding='utf-8', newline='') as file:
#    for line in file:
#        games.append(line.strip('\r\n'))

#bundles = {}
#for game in games:
#    fetch(game)
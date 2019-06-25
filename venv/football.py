import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

#base_url = 'https://www.marathonbet.ru/su/live/26418'
base_url = 'https://1xstavka.ru/live/Football/'

def hh_parse(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code ==200:

#        soup = request.content, 'html.parser'
#        soup.normalize('NFKC', p.decode()).encode('ascii', 'ignore')
#        print(soup)
    else:
        print('ERROR')

hh_parse(base_url, headers)
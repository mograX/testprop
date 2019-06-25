import requests
from bs4 import BeautifulSoup


#План:
#    1.узнать колличество лиг
#    2.проверить все ли лиги открыты, если нет, то открыть??????
#    3.собирать данные о матче из каждой лиги и проверять по критериям

headers = {'accept': '*/*',
           'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


def get_html(url):
    r = requests.get(url)
    return r.text

#def get_total_lig(html):
#    soup = BeautifulSoup(html, 'lxml')
#    name_match = soup.find('div', class_ = 'category-container').find_all('a', class_ = 'member-link')
#    time = soup.find('div', class_ = 'green bold nobr').text.strip()
#
    #   name_match = pages[0].find('div', class_ = 'member-area')
    #   for liga in pages:
    #       for match in liga:
    #           match_result = match.find('data-event-name')
    return name_match, time

def proverka_prinadlezhnosti_k_strategii(info_1match):
    schet = info_1match.find('div', class_ = 'cl-left red').text.string()
    print('podhodit')








def proverka_matcha_po_kriteriyu(html):
   soup = BeautifulSoup(html, 'lxml')
   lig_all = soup.find_all('div', class_ = 'category-container')
   for info_1lig in lig_all:
       info_all_match = info_1lig.find_all('div', class_ = 'bg coupon-row')
       for info_1match in info_all_match:
           break_or_no = info_1match.find('div', class_='green bold nobr').text.strip()
           if break_or_no != None:
               if break_or_no in ['Пер.']:
                   schet_nepraviln = info_1match.find('div', class_ = 'cl-left red').text.strip()
                   schet = schet_nepraviln.split('(')[0]
                   schet_1komand = schet.split(':')[0]
                   schet_2komand = schet.split(':')[1]


                   print(schet_1komand, schet_2komand)










#print(get_total_lig(get_html('https://www.marathonbet.ru/su/live/26418')))

html1 = get_html('https://www.marathonbet.ru/su/live/26418')
proverka_matcha_po_kriteriyu(html1)








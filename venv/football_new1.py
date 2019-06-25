import requests
from bs4 import BeautifulSoup
import re

# 1.распарсить все юрл лиг, поместить их из функции в переменную и вернуть
# 2.итерироваться по юрл лиг, вызывать функцию в которую передается юрл лиги(в которой есть переменные со значениями []),
#   распарсить матчи в лиге и итерироваться по ним, если есть значение Пер., то проверить счет, если значения не равны друг другу,
#   то применять различные условия из тетрадки, если условие верно, то append в ранее созданные переменные всех значений,
#   вернуть переменные со значениями названия лиги, счетом к1 и к2, форы на 1к и 2к и коэффициенты к ним.
# 3.проверить вернулись пустые переменные, или со значениями, если внутри есть значения, то вызвать функцию, которая бадет
#   формировать красивое сообщение и выводить его в консоль
#
#
#
#
#
#
#
#
# решить проблемму с преобразованием времени матча в текст и строку, т.к значение (90 +2:30), или вовсе его отсутствие
# при закрытии и открытии счета нельзя обратить в текст,(можно улавливать ошибку)

headers = {'accept': '*/*',
           'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

#getting html of url
def get_html(url):
    r = requests.get(url)
    return r.text


#getting html data with a list right data
# name leagues, url leagues, 1k name, 2k name, 1k score, 2k score, 1k handicap, 2k handicap, 1k ratio, 2k ratio
def get_nearly_right(html):
    match_all_good = []
    soup = BeautifulSoup(html, 'lxml')
    leagues_all =soup.find_all('div', class_ = 'category-container')
    for leagues_unknown in leagues_all:
        match_in_leagues = leagues_unknown.find_all('div', class_ = 'bg coupon-row')
        for match_unknown in match_in_leagues:
            try:
                if match_unknown.find('div', class_ = 'green bold nobr').text.strip() in ['Пер.']:
                    score = match_unknown.find('div', class_='cl-left red').text.strip()
                    score = score.split('(')[0]
                    score = score.split(':')
                    score = score[0], score[1].replace(' ', '')
                    #score on 1 and 2 team
                    print('perviy', score[0], 'vtoroy', score[1])
                    #difference handicap 1team from 2team
                    score_difference = int(score[0]) - int(score[1])
                    if score_difference in [2, 3, 4, 5, 6, -2, -3, -4, -5, -6]:
                        #name leagues
                        league_name = leagues_unknown.find(class_ = 'category-label simple-live').text.strip()
                        print(league_name)
                        #url leagues
                        league_url = leagues_unknown.find(class_ = 'category-label-link').get('href')
                        print(league_url)
                        #name team1 and team2
                        match_name = match_unknown.find_all('span', {'data-member-link' : 'true'})
                        print('Team 1: ', match_name[0].text, 'Team 2: ', match_name[1].text)
                        #handicap ratio and value
                        handicap_value = match_unknown.find_all('td', {'data-market-type' : 'HANDICAP'})
                        #############print(handicap_value[0].text.strip(), handicap_value[1].text)
                        #hanicap 1team value and ratio
                        handicap_1team_value = handicap_value[0].text
                        handicap_1team_value_and_ratio = handicap_1team_value.split()
                        print('Value one team: ', handicap_1team_value_and_ratio[0], 'Ratio one team: ', handicap_1team_value_and_ratio[1])
                        #handicap 2team value and ratio
                        handicap_2team_value = handicap_value[1].text
                        handicap_2team_value_and_ratio = handicap_2team_value.split()
                        print('Value two tean: ', handicap_2team_value_and_ratio[0], 'Ratio two team: ', handicap_2team_value_and_ratio[1])




            except Exception:
                print('ERROR')








sam = get_nearly_right(get_html('https://www.marathonbet.ru/su/live/26418'))
sam



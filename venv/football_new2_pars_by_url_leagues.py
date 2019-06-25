import requests
from bs4 import BeautifulSoup
import re
import time
import itertools

# 1.распарсить все юрл лиг, поместить их из функции в переменную и вернуть
# 2.итерироваться по юрл лиг, вызывать функцию в которую передается юрл лиги(в которой есть переменные со значениями []),
#   распарсить матчи в лиге и итерироваться по ним, если есть значение Пер., то проверить счет, если значения не равны друг другу,
#   то применять различные условия из тетрадки, если условие верно, то append в ранее созданные переменные всех значений,
#   вернуть переменные со значениями названия лиги, счетом к1 и к2, форы на 1к и 2к и коэффициенты к ним.
# 3.проверить вернулись пустые переменные, или со значениями, если внутри есть значения, то вызвать функцию, которая будет
#   формировать красивое сообщение и выводить его в консоль
#

headers = {'accept': '*/*',
           'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

#getting html of url
def get_html(url):
    r = requests.get(url)
    return r.text

#поиск соответствия условий и внесение результатов в список
def league_find_match(html, data_print):

    match_all = html.find_all('div', class_ = 'bg coupon-row')
    for match_unknown in match_all:
        try:
            if match_unknown.find('div', class_='green bold nobr').text.strip() in ['Пер.']:
                score = match_unknown.find('div', class_='cl-left red').text.strip()
                score = score.split('(')[0]
                score = score.split(':')
                score = score[0], score[1].replace(' ', '')


                # difference handicap 1team from 2team
                score_difference = int(score[0]) - int(score[1])
                if score_difference in [2, 3, 4, 5, 6, -2, -3, -4, -5, -6]:
                    # name leagues
                    league_name = html.find(class_='category-label simple-live').text.strip()
                    print(league_name)
                    # url leagues
                    league_url = html.find(class_='category-label-link').get('href')
                    print(league_url)
                    # name team1 and team2
                    match_name = match_unknown.find_all('span', {'data-member-link': 'true'})
                    print('Team 1: ', match_name[0].text, 'Team 2: ', match_name[1].text)
                    # score on 1 and 2 team
                    print('perviy', score[0], 'vtoroy', score[1])
                    # handicap ratio and value
                    handicap_value = match_unknown.find_all('td', {'data-market-type': 'HANDICAP'})
                    #############print(handicap_value[0].text.strip(), handicap_value[1].text)
                    # hanicap 1team value and ratio
                    handicap_1team_value = handicap_value[0].text
                    handicap_1team_value_and_ratio = handicap_1team_value.split()
                    print('Value one team: ', handicap_1team_value_and_ratio[0], 'Ratio one team: ', handicap_1team_value_and_ratio[1])
                    # handicap 2team value and ratio
                    handicap_2team_value = handicap_value[1].text
                    handicap_2team_value_and_ratio = handicap_2team_value.split()
                    print('Value two tean: ', handicap_2team_value_and_ratio[0], 'Ratio two team: ', handicap_2team_value_and_ratio[1])

                    # name leagues, url leagues, 1k name, 2k name, 1k score, 2k score, 1k handicap, 2k handicap, 1k ratio, 2k ratio
                    data_print.extend((league_name, league_url, match_name[0].text, match_name[1].text, score[0], score[1],
                                      handicap_1team_value_and_ratio[0], handicap_1team_value_and_ratio[1], handicap_2team_value_and_ratio[0],
                                      handicap_2team_value_and_ratio[1] ))


        except Exception:
            print('ERROR')
    return data_print



for i in itertools.count():
    time.sleep(1)

    soup = BeautifulSoup(get_html('https://www.marathonbet.ru/su/live/26418'), 'lxml')
    url_leagues_all = soup.find_all('div', class_='category-container')
    sport_who = soup.find(class_='sport-category-label').text
    if sport_who in ['Футбол']:
        data_for_print = []
        league_number = 0
        league_number_all = len(url_leagues_all)
        for url_league in url_leagues_all:
            url_league_for_def = url_league.find(class_='category-label-link').get('href')
            url_league_for_def = url_league_for_def.split()
            #def
            league_number += 1
            print(league_number, ' of ', league_number_all)
            data_for_print = league_find_match(BeautifulSoup(get_html('https://www.marathonbet.ru' + url_league_for_def[0]), 'lxml'), data_for_print)
            if league_number == league_number_all:
                print(data_for_print)


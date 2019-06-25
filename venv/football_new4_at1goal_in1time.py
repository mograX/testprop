import requests
from bs4 import BeautifulSoup
import re
import time
import itertools
#import telebot
import config
#from telebot import apihelper
from telegram import Bot
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler


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
            match_unknown_time = match_unknown.find('div', class_='green bold nobr').text.strip()
            #match_unknown_time = int(match_unknown_time.split(':')[0])

            if match_unknown_time.split(':')[0] in ['69', '70', '71', '72', '73', '74', '']:
                print(match_unknown_time)
                score = match_unknown.find('div', class_='cl-left red').text.strip()
                score = score.split('(')[0]
                score = score.split(':')
                score = score[0], score[1].replace(' ', '')


                # difference handicap 1team from 2team
                score_difference = int(score[0]) + int(score[1])
                if score_difference in [1]:
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
                    handicap_value = match_unknown.find_all('td', {'data-market-type': 'TOTAL'})
                    #############print(handicap_value[0].text.strip(), handicap_value[1].text)
                    # hanicap 1team value and ratio
                    handicap_1team_value = handicap_value[0].text
                    handicap_1team_value_and_ratio = handicap_1team_value.split()
                    print('Value one team: ', handicap_1team_value_and_ratio[0], 'Ratio one team: ', handicap_1team_value_and_ratio[1])
                    # handicap 2team value and ratio
                    handicap_2team_value = handicap_value[1].text
                    handicap_2team_value_and_ratio = handicap_2team_value.split()
                    print('Value two tean: ', handicap_2team_value_and_ratio[0], 'Ratio two team: ', handicap_2team_value_and_ratio[1])


                    if match_name[1].text not in data_print:
                        timin = time.time()
                        timin = int(timin)
                        #data_print(len(10))
                        data_print.extend((timin, league_name, league_url, match_name[0].text, match_name[1].text, score[0], score[1],
                                          handicap_1team_value_and_ratio[0], handicap_1team_value_and_ratio[1], handicap_2team_value_and_ratio[0],
                                          handicap_2team_value_and_ratio[1], match_unknown_time ))


        except Exception:
            print('error')
    return data_print


#check_time
def check_time(data):
    len_data = len(data)
    timin = time.time()
    timin = int(timin)
    for times in reversed(range(0, len_data, 12)):
        if (timin - int(data[times])) >= 500:
            for i in range(0, 12):
                data.pop(times)
    return data

#check_time for tg
def tg_check_time(data_print, data_tg):
    len_data = len(data_print)
    timin = time.time()
    timin = int(timin)
    for times in reversed(range(0, len_data, 12)):
        if (timin - int(data_print[times])) <= 60:
            for i in range(0, 12):
                data_tg.append(data_print[times])
                times +=1
    return data_tg



def tg_for_send(data_tg):
    len_data = len(data_tg)
    timin = time.time()
    timin = int(timin)
    for times in reversed(range(0, len_data, 12)):
        if (timin - int(data_tg[times])) >= 60:
            for i in range (0,12):
                data_tg.pop(times)
    return data_tg



#bot

def bot_sendler(tg_data):
    bot = Bot(token='785697453:AAE3plj51Sc1m-gbi4RDUJyLNLCSf0Zaqds', base_url='https://telegg.ru/orig/bot')

    len_data = len(tg_data)
    for data in (range(0, len_data, 12)):
        # time, name leagues, url leagues, 1k name, 2k name, 1k score, 2k score, 1k handicap, 2k handicap, 1k ratio, 2k ratio
        bot.send_message(-1001478479562, '{}\n{} VS {}\nTime: {}\n Score {}:{}\nТМ {} {} ТБ {} {}   '.format(tg_data[data+1], tg_data[data+3], tg_data[data+4],
                                                                             tg_data[data+11], tg_data[data+5], tg_data[data+6], tg_data[data+7],
                                                                             tg_data[data+8], tg_data[data+9], tg_data[data+10]))
        print('tg yes')




data_for_print = []
tg_data_send = []

#bot_sendler(bot)

for i in itertools.count():
    time.sleep(200)
    try:

        soup = BeautifulSoup(get_html('https://www.marathonbet.ru/su/live/26418'), 'lxml')
        url_leagues_all = soup.find_all('div', class_='category-container')
        sport_who = soup.find(class_='sport-category-label').text
        if sport_who in ['Футбол']:
            league_number = 0
            league_number_all = len(url_leagues_all)
            for url_league in url_leagues_all:
                #pars open leagues
                data_for_print = league_find_match(url_league, data_for_print)
                league_number += 1
                print(league_number, ' of ', league_number_all)


            #pars clossed leagues
            try:
                leagues_clossed = soup.find_all('div', class_ = 'category-container collapsed')
                for url_leagues_clossed in leagues_clossed:
                    url_league_for_def = leagues_clossed.find(class_='category-label-link').get('href')
                    url_league_for_def = url_league_for_def.split()
                    data_for_print = league_find_match(BeautifulSoup(get_html('https://www.marathonbet.ru' + url_league_for_def[0]), 'lxml'), data_for_print)
                    print('PARS URL')

            except Exception:
                    pass

            print('Data before time def')
            print(data_for_print)

            print('Data after time def')
            data_for_print = check_time(data_for_print)
            print(data_for_print)

            print('Tg def')
            tg_data_send = tg_check_time(data_for_print, tg_data_send)
            print(tg_data_send)

            print('Tg def for send')
            tg_data_send = tg_for_send((tg_data_send))
            print(tg_data_send)
            bot_sendler(tg_data_send)

    except Exception:
        pass


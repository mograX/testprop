import requests
from bs4 import BeautifulSoup
import re
import time
import itertools
#import telebot
#from telebot import apihelper
from telegram import Bot
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
import subprocess


headers = {'accept': '*/*',
           'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

def get_html (url):
    r = requests.get(url)
    return r.text

def league_match_ratio(html, data_ratio):


    match_all = html.find_all('div', class_ = 'bg coupon-row')
    for match_unknown in match_all:
        try:
            match_time = match_unknown.find('div', class_='cl-left red')
            match_time = match_time.text.strip()
            #print(match_time)
            match_time = len(match_time)

            if match_time < 20:
                #print('good')
                match_link = match_unknown.find(class_='member-link').get('href')

                if match_link not in data_ratio:
                    name_leaguess = html.find(class_='category-label simple-live').text.strip()
                    if not (re.search(r'\bЖенщины\b', name_leaguess)or re.search(r'\b16 лет\b', name_leaguess) or re.search(r'\b19 лет\b', name_leaguess) or re.search(r'\b20 лет\b', name_leaguess) or re.search(r'\b21 года\b', name_leaguess) or re.search(r'\b23 лет\b', name_leaguess) or re.search(r'\bТоварищеские\b', name_leaguess) or re.search(r'\bЮниорские\b', name_leaguess) or re.search(r'\bМолодежные\b', name_leaguess)):
                        timin = time.time()
                        timin = int(timin)

                        ratio = match_unknown.find_all('td', {'data-market-type': 'HANDICAP'})
                        ratio = ratio[0].text.replace('(', '', 1).replace('\n', '', 1).strip('').split('.')

                        ratio = int(ratio[0])

                        data_ratio.extend((timin, match_link, ratio))
        except Exception :
            pass
    return data_ratio


def league_match_find(html, data_ratio, data_send):
    if 1 ==1:
        match_all = html.find_all('div', class_='bg coupon-row')
        for match_unknown in match_all:
            try:
                match_link = match_unknown.find(class_='member-link').get('href')
                if match_link in data_ratio:

                    match_ratio_bk_index = data_ratio.index('{}'.format(match_link))

                    match_ratio_bk = data_ratio[match_ratio_bk_index + 1]

                    ratio_live = match_unknown.find_all('td', {'data-market-type': 'HANDICAP'})
                    ratio_live = ratio_live[0].text.replace('(', '', 1).replace('\n', '', 1).strip('').split('.')
                    ratio_live = int(ratio_live[0])

                    difference = 0

                    if match_ratio_bk < 25:
                        if ratio_live >= match_ratio_bk + 15:
                            difference = 1
                        if ratio_live <= match_ratio_bk - 15:
                            difference = 1

                    if difference == 1:
                        if match_link not in data_send:

                            match_time = match_unknown.find('div', class_='cl-left red')
                            match_time = match_time.text.strip()
                            match_time_new = match_time.split()
                            match_time_new = ''.join(match_time_new)
                            match_time_new = match_time_new.replace('(', ' (', 1).replace(')', ') ', 1).replace(',', ', ')

                            timin = time.time()
                            timin = int(timin)
                            name_leaguess = html.find(class_='category-label simple-live').text.strip()
                            match_name = match_unknown.find_all('span', {'data-member-link': 'true'})
                            data_send.extend((data_ratio[match_ratio_bk_index -1], timin, match_link, name_leaguess, match_name[0].text, match_name[1].text,
                                              match_ratio_bk, ratio_live, match_time_new ))
            except Exception:
                pass
    return data_send


def check_time_ratio(data_ratio):
    len_data = len(data_ratio)
    timin = time.time()
    timin = int(timin)
    for times in reversed(range(0, len_data, 3)):
        if (timin - int(data_ratio[times])) >= 6000:
            for i in range(0, 3):
                data_ratio.pop(times)

def check_time_send(data_send):
    len_data = len(data_send)
    timin = time.time()
    timin = int(timin)
    for times in reversed(range(0, len_data, 9)):
        if (timin - int(data_send[times])) >= 6000:
            for i in range(0, 9):
                data_send.pop(times)


def bot_sendler(tg_data):
    bot = Bot(token='785697453:AAE3plj51Sc1m-gbi4RDUJyLNLCSf0Zaqds', base_url='https://telegg.ru/orig/bot')

    len_data = len(tg_data)
    timin = time.time()
    timin = int(timin)
    for data in (range(0, len_data, 9)):
        if (timin - tg_data[data + 1]) < 30:
            # time, name leagues, url leagues, 1k name, 2k name, 1k score, 2k score, 1k handicap, 2k handicap, 1k ratio, 2k ratio
            bot.send_message(-1001478479562, '🏆 {}\n{} VS {}\n📈 bk hand: {} live hand: {}\n🧾 {}'.format(tg_data[data+3], tg_data[data+4], tg_data[data+5],
                                                                                 tg_data[data+6], tg_data[data+7], tg_data[data+8]))









data_total = []
data_for_ratio = []
data_for_send = []

for i in itertools.count():
    time.sleep(40)
    localtime = time.asctime(time.localtime(time.time()))
    print("Текущее локальное время :", localtime)

    print(data_for_ratio)
    print(data_for_send)


    internet = False
    while not internet:
        try:
            soup = BeautifulSoup(get_html('https://www.marathonbet.ru/su/live/45356'), 'lxml')
            print("Internet is up again!")


            html_leaguess_all = soup.find_all('div', class_='category-container')
            sport_who = soup.find(class_='sport-category-label').text
            internet = True

            if sport_who in ['Баскетбол']:
                print('bassketball on')

                for html_leagues in html_leaguess_all:
                    data_for_ratio = league_match_ratio(html_leagues, data_for_ratio)
                    data_for_send = league_match_find(html_leagues, data_for_ratio, data_for_send)
                check_time_ratio(data_for_ratio)
                check_time_send(data_for_send)
                bot_sendler(data_for_send)



        except Exception:
            time.sleep(5)
            print("Internet is still down :(")

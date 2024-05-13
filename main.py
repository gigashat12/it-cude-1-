import telebot
from bs4 import BeautifulSoup
import requests
from fuzzywuzzy import fuzz
import time
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#load_dotenv()

TELEGRAM_TOKEN = '6763137333:AAGIyKBkdM2jg-U54YNn_bJVtNEeWPM0pT4'
bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)
users_search = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("👋 Поздороваться")
    btn2 = telebot.types.KeyboardButton("❓ Задать вопрос")
    btn3 = telebot.types.KeyboardButton("ПРИСТУПИМ")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я телеграмм бот для поискав фильмов".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "👋 Поздороваться":
        bot.send_message(message.chat.id, text="Привеет.. Спасибо что пользуешься ботом!)")
# -------------------------------------------------------------------------------------------------------------------------------------------
    elif message.text == "❓ Задать вопрос":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton("Что ты можешь?")
        btn2 = telebot.types.KeyboardButton("Как пользоваться ботом?")
        back = telebot.types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос, если надо конечно", reply_markup=markup)
# -------------------------------------------------------------------------------------------------------------------------------------------
    elif message.text == "Что ты можешь?":
        bot.send_message(message.chat.id, text="Я способен искать ссылки на фильм и предоставлю возможость скачать его через себя (в зависимости от размеров фильма услуга может стать платной)")
# -------------------------------------------------------------------------------------------------------------------------------------------
    elif message.text == "Как пользоваться ботом?":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = telebot.types.KeyboardButton("как найти фильм?")
        button2 = telebot.types.KeyboardButton("как начать смотреть фильм онлайн?")
        button3 = telebot.types.KeyboardButton("как скачать фильм?")
        button4 = telebot.types.KeyboardButton("Вернуться в главное меню")
        markup.add(button1, button2, button3, button4)
        bot.send_message(message.chat.id, text="щас обьясню, что тебе не понятно?", reply_markup=markup)
    elif message.text == 'как найти фильм?':
        bot.send_message(message.chat.id, text ='пишешь боту примерное название прямо так в сообщениях, он если фильм не сильно старый найдёт его с шансом 75%')
# -------------------------------------------------------------------------------------------------------------------------------------------
    elif message.text == 'как начать смотреть фильм онлайн?':
        bot.send_message(message.chat.id, text = 'повторяешь предыдущие действия,'
                                                 'переходишь по ссылке')
# -------------------------------------------------------------------------------------------------------------------------------------------
    elif message.text == 'как скачать фильм?':
        bot.send_message(message.chat.id, text = 'повторяешь предыдущие действия и удостоверившись, что фильм тот скачиваешь')
# -------------------------------------------------------------------------------------------------------------------------------------------
    elif message.text == "Вернуться в главное меню":
        markup3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = telebot.types.KeyboardButton("👋 Поздороваться")
        button2 = telebot.types.KeyboardButton("❓ Задать вопрос")
        button3 = telebot.types.KeyboardButton("ПРИСТУПИМ")
        markup3.add(button1, button2, button3)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup3)
#-------------------------------------------------------------------------------------------------------------------------------------------

    elif message.text == 'ПРИСТУПИМ':
        markup2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        Btn1 = telebot.types.KeyboardButton("Посоветуй фильм")
        Btn2 = telebot.types.KeyboardButton("Найди фильм")
        Btn3 = telebot.types.KeyboardButton("Вернуться в главное меню")
        markup2.add(Btn1, Btn2, Btn3)
        bot.send_message(message.chat.id, text="что вас интересует", reply_markup=markup2)


#    elif message.text == 'Посоветуй фильм':
#        user_ratings_df = pd.read_csv("archive/ratings.csv")
#        user_ratings_df.head()
#       movie_metadata = pd.read_csv("archive/movies_metadata.csv")
#       movie_metadata = movie_names[['title', 'genres']]
#        movie_metadata.head()
#        movie_data = user_ratings_df.merge(movie_metadata, on='movieId')
#        movie_data.head()
#        user_item_matrix = ratings_data.pivot(index=['userId'], columns=['movieId'], values='rating').fillna(0)
#        user_item_matrix
#       # Define a KNN model on cosine similarity
#       cf_knn_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10, n_jobs=-1)#
 #       # Fitting the model on our matrix
 #      cf_knn_model.fit(user_item_matrix)

    else:
        markup1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        count = 0
        user_request = message.text

        for numder in range(1, 501):
            url = f'https://w140.zona.plus/movies/filter/sort-date?page={numder}'
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')

            #            https = 'https://w140.zona.plus/' + soup.find('li', class_='results-item-wrap').find('a', class_='results-item').get('href')
            #            name = soup.find('li', class_='results-item-wrap').find('a', class_='results-item').get('title')
            films = soup.findAll('li', class_='results-item-wrap')

            data = []
            for film in films:

                https = 'https://w140.zona.plus/' + film.find('a', class_='results-item').get('href')
                name = film.find('a', class_='results-item').get('title')

                if fuzz.partial_ratio(user_request, name) >= 80:
                    r_2 = requests.get(https)
                    soup_2 = BeautifulSoup(r_2.text, 'lxml')
                    text_1 = soup_2.find('div', class_='entity-desc-description').text
                    #            genre_1 = soup_2.find('a', class_='entity-desc-link').findall('span', class_='entity-desc-link-u')
                    #            time = soup_2.find("time datetime")
                    data.append([name, text_1, https])
                    count += 1
                    bot.send_message(message.from_user.id, text=name, reply_markup=markup1)
                    bot.send_message(message.from_user.id, text=text_1, reply_markup=markup1)
                    bot.send_message(message.from_user.id, text=https, reply_markup=markup1)
                    break
            if count == 1:
                break
        if count == 0:
            bot.send_message(message.chat.id, text='Прошу прощения, но в моей базе нет такого', reply_markup=markup1)

bot.polling(none_stop=True)

"""Написать программу, которая шлёт в некоторый канал в Телеграмме последнюю 
новость с сайта https://vc.ru. Условие: в коде не должно быть токенов.
Токен хранится в файле .env """

import requests
import telebot
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from environs import Env
from telebot import types


env = Env()
env.read_env() #Читаем переменную окружение из файла .env
token = env("BOT_TOKEN")  #Присваем токен прочитанный из переменной окружения
bot = telebot.TeleBot(token)
ua = UserAgent()
news = {
        'link': ''
    }


def get_page(url)->None:
    #Функция принимает на вход URL и сохраняет в словаре дату и время создания,
    #ссылку и текст самой свежей новости
    response = requests.get(url=url, headers={'user-agent': f'{ua.random}'})
    soup = BeautifulSoup(response.text, 'lxml')
    news_block = soup.select('div.feed')
    news['link'] = news_block[0].find('a', class_='content-link').get('href')

def create_button():
    #Функция создает кнопку для телеграмм бота и возращает её
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('Новость')
    markup.add(btn)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    #При старте бота выводим приветствие и формируем кнопку
    bot.send_message(message.chat.id, 'Привет! Я тестовый бот для отображения\
            первой новости с сайта vc.ru', reply_markup = create_button())


@bot.message_handler(content_types=['text'])
def send_new(message):
    #Функция отправляет ссылку на новость с сайт vc.ru в телеграмм бота
    #При вводе любого сообщения кроме /sart, бот предлагает почитать новости
    if message.text == 'Новость':
        bot.send_message(message.from_user.id, f"{news['link']}")
    else:
        bot.send_message(message.from_user.id, "Не хочешь почтитать новости?",\
                reply_markup=create_button())

get_page(url='https://vc.ru')
bot.polling(none_stop=True)#, interval=0)


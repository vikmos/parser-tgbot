import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import telebot;


bot = telebot.TeleBot(input("Введите токен: "));

ua = UserAgent()
news = {
    'time': '',
    'link': '',
    'text': ''
}


def get_page(url)->None:
    #Функция принимает на вход URL и сохраняет в словаре дату и время создания, ссылку и текст самой свежей новости

    response = requests.get(url=url, headers={'user-agent': f'{ua.random}'})

    soup = BeautifulSoup(response.text, 'lxml')
    newsBlock = soup.find('div', class_='news_item')
    news['time'] = newsBlock.find('time', class_='time').get('title')
    news['link'] = newsBlock.find('a', class_='news_item__title').get('href')
    news['text'] = newsBlock.find('a', class_='news_item__title').text


@bot.message_handler(content_types=['text'])
def send_new(message):
    #Функция отправляет новость из словаря news  в телеграмм бота, токен которого указан при старте программмы
    if message.text == "Привет" or message.text == "привет" or message.text == "/start":
        bot.send_message(message.from_user.id, f"{' '.join(news['time'].split(' ')[0:2:1])}\n{news['link']}\n{news['text']}")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

def main():
    get_page(url='https://vc.ru/')
    bot.polling(none_stop=True, interval=0)

if __name__ == '__main__':
    main()
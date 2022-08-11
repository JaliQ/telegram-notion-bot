from datetime import datetime
import time
import telebot
import requests
from bs4 import BeautifulSoup as b
from dotenv import load_dotenv
import os
import threading
# bot would have 2 mods : parse news site and remind about some thing that's have to be done
load_dotenv()
token = os.getenv("token")
bot = telebot.TeleBot(token)




URL = "https://cryptonews.com/"


def parser(URL):
    r = requests.get(URL)
    soup = b(r.text, "html.parser")
    news = soup.find_all("div", class_="mb-25 d-none d-md-block")
    return [c.text for c in news]

list_of_news = parser(URL)

@bot.message_handler(commands=["start"])
def start(message):
    mess = f"<b>Hello, {message.from_user.first_name}.</b> I'm only a test bot, but I'll remind you things that have to be done"
    bot.send_message(message.chat.id, mess, parse_mode="html")
    sti = open("sticker.webp", "rb")
    bot.send_sticker(message.chat.id, sti)


@bot.message_handler(commands=["note"])
def make_notion(message):
    bot.send_message(message.chat.id, "What do you want me to remind you of?")
    bot.register_next_step_handler(message, reg_note)


def reg_note(message):
    global note
    note = message.text
    bot.send_message(
        message.chat.id,
        f"Get it, wheh do I need to remind you that you have to {note} . Send me time if format : 15 30",
    )
    bot.register_next_step_handler(message, get_time)


def get_time(message):
    times = message.text
    bot.send_message(message.chat.id, "Ok, I'm goint to sleep waiting till this time")
    thread2 = threading.Thread(target=send_with_delay, args=(message,times))
    thread2.start()
    # time.sleep(
    #     (int(times[0:2]) - datetime.now().hour) * 360
    #     + (int(times[3:5]) - datetime.now().minute) * 60
    # )
    
    
def send_with_delay(message,times):
    if  (int(times[0:2]) <=24) and (int(times[3:5])<=60):
        time.sleep(
            (int(times[0:2])* 360 + int(times[3:5])*60 - (datetime.now().hour*360 + datetime.now().minute * 60)))
        
        bot.send_message(message.chat.id, f"You have to {note}!")
    else: bot.send_message(message.chat.id, f"Incorrect time format")



@bot.message_handler(commands=["news"])
def news(message):
    bot.send_message(
        message.chat.id, f"<b>Hello, actual news for today: </b>", parse_mode="html"
    )
    for i in range(len(list_of_news)):
        bot.send_message(message.chat.id, list_of_news[i])


def main():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()


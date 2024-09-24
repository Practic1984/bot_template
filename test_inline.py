# This example show how to write an inline mode telegram bot use pyTelegramBotAPI.
import logging
import sys
import time

import telebot
from telebot import types
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

data = ['гайка1', 'гайка2', 'гайка3', 'гайка4']

@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    try:
        if inline_query.text in data:
            print(inline_query)
            bot.answer_inline_query(inline_query.id, data)
    except Exception as e:
        print(e)


def main_loop():
    bot.infinity_polling()
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)
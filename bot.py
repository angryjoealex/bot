import logging
import settings
import ephem
import datetime
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='/Users/apetrov/LearnPython/projects/mybot/bot.log')


def greet_user(update, context):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def get_planet_place(update, context):
    input_message = update.message.text.split()
    try:
        command, planet = input_message
    except ValueError:
        update.message.reply_text("Вы не ввели название планеты") 
    if not hasattr(ephem, planet):
        update.message.reply_text("Введенная планета не найдена")
        return
    planet_info = getattr(ephem, planet)()
    planet_info.compute(datetime.date.today())
    planet_place = ephem.constellation(planet_info)
    update.message.reply_text(planet_place)


def wordcount(update, context):
    input_message = update.message.text.split("\wordcount")
    input_message[1].split()
    update.message.reply_text(input_message[1].split())

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", get_planet_place))
    dp.add_handler(CommandHandler("wordcount", wordcount))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()

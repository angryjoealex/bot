import logging
import settings
import ephem
import datetime
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
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
    counted_words = []
    input_message = update.message.text.partition(' ')[2]
    input_message = input_message.strip()
    for replc_simb in ('^,', ',$', ','):
        input_message = re.sub(replc_simb, ' ', input_message)
    text = input_message.split()
    try:
        text[0]
    except IndexError:
        update.message.reply_text("Вы не ввели текст")
        return 
    for word in text:
        matched_text = (re.match('(^[a-zA-Zа-яА-ЯёЁ]+([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?|^[a-zA-Zа-яА-ЯёЁ]+-[a-zA-Zа-яА-ЯёЁ]+|^[a-zA-Zа-яА-ЯёЁ]+)', word))
        try:
            matched_text.group(0)
        except AttributeError:
            pass
        else:
            counted_words.append(matched_text.group(0))
        word_count = len(counted_words) 
    update.message.reply_text(f"В тексте '{input_message}' {word_count} слов")

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

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem
from random import randint, choice
from emoji import emojize

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']

def greet_user(update, context):
    smile = get_smile(context.user_data)
    user_name = update.message.from_user.first_name
    print(f'Greetings, my dear little {user_name}! {smile} You push /start')
    update.message.reply_text(f'Greetings, my dear little {user_name}! {smile} You push /start')

def guess_number(update, context):
    my_len = 0
    if context.args:
        my_len = len(context.args)
    else:
        my_len = 'none'
    update.message.reply_text(my_len)


def planet(update, context):
    user_text = context.args
    try:
        when_next1 = ephem.next_full_moon(user_text[0])
        update.message.reply_text(when_next1)
    except:
        print('wrong date')
        update.message.reply_text('wrong date')

def main():
    PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    logging.basicConfig(filename='bot.log', level=logging.INFO)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start',greet_user))
    dp.add_handler(CommandHandler('wordcount', guess_number))
    dp.add_handler(CommandHandler('next_full_moon',planet))

    logging.info("Bot has just started")
    mybot.start_polling()
    mybot.idle()



if __name__ == "__main__":
    main()
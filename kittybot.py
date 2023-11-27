# kittybot/kittybot.py
import os
import requests

from dotenv import load_dotenv

from telegram.ext import CommandHandler, InlineQueryHandler, Updater
from telegram import ReplyKeyboardMarkup, InlineQueryResultPhoto

load_dotenv()

secret_token = os.getenv('TOKEN')


updater = Updater(token=secret_token)
URL = 'https://api.thecatapi.com/v1/images/search'


def get_new_image():
    response = requests.get(URL).json()
    random_cat = response[0].get('url')
    return random_cat


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def new_cat_inline(update, context):
    query = update.inline_query.query

    # if not query:  # empty query should not be handled
    #    return

    result = []

    for i in range(12):
        photo = get_new_image()
        result.append(
            InlineQueryResultPhoto(id=str(i), photo_url=photo, thumb_url=photo)
        )

    context.bot.answer_inline_query(inline_query_id=update.inline_query.id,
                                    results=result,
                                    cache_time=0)


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    # За счёт параметра resize_keyboard=True сделаем кнопки поменьше
    button = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри, какого котика я тебе нашёл'.format(name),
        reply_markup=button
    )

    context.bot.send_photo(chat.id, get_new_image())

updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
updater.dispatcher.add_handler(InlineQueryHandler(new_cat_inline), )

updater.start_polling()
updater.idle()

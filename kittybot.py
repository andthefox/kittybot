# kittybot/kittybot.py
import logging
import os

import requests

from telegram.ext import CommandHandler, InlineQueryHandler, Updater
from telegram import ReplyKeyboardMarkup, InlineQueryResultPhoto

from dotenv import load_dotenv

load_dotenv()

secret_token = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='catlog.log')


URL = 'https://api.thecatapi.com/v1/images/search'

CATS_INLINE = 6


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def new_cat_inline(update, context):
    query = update.inline_query

    result = []

    for i in range(CATS_INLINE):
        photo = get_new_image()
        result.append(
            InlineQueryResultPhoto(id=str(i), photo_url=photo, thumb_url=photo)
        )

    context.bot.answer_inline_query(inline_query_id=query.id,
                                    results=result,
                                    cache_time=0)


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name

    button = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри, какого котика я тебе нашёл'.format(name),
        reply_markup=button
    )

    context.bot.send_photo(chat.id, get_new_image())


def main():
    updater = Updater(token=secret_token)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(InlineQueryHandler(new_cat_inline))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

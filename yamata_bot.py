import logging
import requests
import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import os
from db import db


# Включить ведение журнала
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
REGISTER, NAME, STAMP, KEY, TIME, CONFIRMATION = range(6)
reply_keyboard = [['Подтверждаю', 'Перезаполнить']]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
TOKEN = '5031875066:AAFlPRGfzlRJplNSRSYGKh78xnWvJzAk3cY'
bot = telegram.Bot(token=TOKEN)
# TOKEN = os.environ['EXACT_TOKEN_TYPES']
chat_id = 'Yamata_telegram_bot'
user_data = {}


def callback_request(data, context):
    db.botkey.create({
        'telegram_id': data['chat_id'],
        'first_name': data['first'],
        'second_name': data['second'],
        'key': 2587
    })


def facts_to_str(user_data):
    facts = list()
    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))
    return "\n".join(facts).join(['\n', '\n'])


def start(update, context):
    reply_key = [['Регистрация', 'Код', 'Выход']]
    markup_key = ReplyKeyboardMarkup(reply_key, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(
        'Преветствуем вас в сервисе Yamata. '
        'Команда /cancel, чтобы прекратить разговор.\n\n'
        'Выберите вариант ответа?',
        reply_markup=markup_key, )
    return REGISTER


def firstname(update, context):
    user = update.message.from_user
    user_data = context.user_data
    user_data['chat_id'] = str(user.id)
    logger.info("registration of %s: %s", user.first_name, update.message.text)

    update.message.reply_text('Напишите свое имя, или нажмите /skip для выхода из программы')
    return NAME


def secondname(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'first'
    text = update.message.text
    user_data[category] = text
    logger.info("firstname %s: %s", user.first_name,  update.message.text)
    update.message.reply_text(
        'Напишите свою фамилию.')

    return STAMP


def skip_photo(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'secondname'
    user_data[category] = 'secondname'
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('Is the food halal? Vegetarian? Please type in the dietary specifications of the food.')

    return TIME


def stamp(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'second'
    text = update.message.text
    user_data[category] = text
    logger.info("secondname %s: %s", user.first_name,  update.message.text)
    update.message.reply_text('Введите номер вашего клейма/штампа')

    return CONFIRMATION


def confirmation(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'stamp'
    text = update.message.text
    user_data[category] = text
    logger.info("stamp %s: %s", user.first_name, update.message.text)
    update.message.reply_text("Спасибо за пройденную регистрацию", reply_markup=markup)

    return KEY


def receive_key(update, context):
    user = update.message.from_user
    user_data = context.user_data
    update.message.reply_text(facts_to_str(user_data))
    q = update.message.chat_id
    callback_request(user_data, q)
    logger.info("%s: %s", user.first_name, update.message.text)
    update.message.reply_text('Ваш код доступа!')

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! Hope to see you again next time.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    global updater
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    # Добавьте обработчик разговоров с состояниями пол, фото, местонахождение и биография
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

            REGISTER: [
                MessageHandler(Filters.regex('^Регистрация$'), firstname),
                MessageHandler(Filters.regex('^Код$'), receive_key),
                MessageHandler(Filters.regex('^Выход$'), cancel),
            ],

            NAME: [
                CommandHandler('start', start),
                MessageHandler(Filters.text, secondname),
                CommandHandler('skip', skip_photo)
            ],

            STAMP: [CommandHandler('start', start), MessageHandler(Filters.text, stamp)],

            CONFIRMATION: [CommandHandler('start', start), MessageHandler(Filters.text, confirmation)],

            KEY: [
                MessageHandler(Filters.regex('^Подтверждаю$'), receive_key),
                MessageHandler(Filters.regex('^Перезаполнить$'), start)
            ],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
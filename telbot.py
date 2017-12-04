import time
import logging
import telegram
from telegram import ReplyKeyboardMarkup,InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler, RegexHandler,filters
import json
import pprint
import argparse
#import errors
#### https://api.telegram.org/bot345178316:AAFxqQy7qIA7gJwUM4nmfvpjfXK0EcdUq-Q/getUpdates
global updater , db , t_end
t_end = time.time() + 60
updater = Updater(token='345178316:AAFxqQy7qIA7gJwUM4nmfvpjfXK0EcdUq-Q')
dp = updater.dispatcher


def parser():
    argparser = argparse.ArgumentParser('flag_users.py')
    argparser.add_argument('--message', help='Text to Send',action='store_true', required=False)
    argparser.add_argument('--group', help='Choose the group ... ' , choices=['rocket','botland'] )
    argparser.add_argument('--debug', help='Enable Debug Logging...' , action='store_true')
    argparser.add_argument('--polling', help='Enable Polling Mode...' , action='store_true')
    #argparser.add_argument('--polling', help='Enable Polling Mode...' , action='store_true')
    return argparser.parse_args()

def get_pretty_print(json_object):
    return json.dumps(json_object, sort_keys=True, indent=4, separators=(',', ': '))

def f_send(bot, chat, message):
    try:
        bot.send_message(chat_id=chat, text=message)
        return True
    except Exception as e:
        logger.error('Something went wrong sending the message: %s ' % str(e) )
        return False

def f_reply(bot, update):
    """Send a message when swears are issued."""
    update.message.reply_text('Language ... ')

def f_info(bot, update):
    """Send plain message"""
    telegram.ChatAction.TYPING
    group = update.message.chat_id
    reply_keyboard = [['start', 'stop', 'status']]
    #print update.message.__dict__
    #print update.message.from_user.__dict__
    #update.message.from_user
    user = update.message.from_user.first_name
    text = ' %s requested an Info Message .. ' % user
    reply_markup=InlineKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    option = 'You choose %s ' % reply_markup
    f_send(bot,group,option)
    f_send(bot,group,text)

def inl(bot, update):
    query = update.callback_query
    message = query.message.chat
    user = message.first_name
    group = message.id
    logger.info(query)
    logger.info(message)
    #logger.info(update.callback_query)
    if query.data == "start":
        #func for turn on light res = k_light.on()
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Started!")
        text=' %s requested to start the service .. ' % user
        f_send(bot,group,text)
        #bot.editMessageText(inline_message_id=update.callback_query.inline_message_id, text="Do you want to turn On or Off light? Light is ON")
        #hardcoded vars variant
        #bot.editMessageText(message_id=298, chat_id=174554240, text="Do you want to turn On or Off light? Light is ON")
    elif query.data == "status":
        #func for turn on light res = k_light.off()
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Find the status below : ")
        text=' %s requested a status update .. ' % user
        f_send(bot,group,text)
        #bot.editMessageText(inline_message_id=update.callback_query.inline_message_id, text="Do you want to turn On or Off light? Light is ON")
        #hardcoded vars variant
        #bot.editMessageText(message_id=298, chat_id=174554240, text="Do you want to turn On or Off light? Light is OFF")
    elif query.data == "stop":
        #func for turn on light res = k_light.off()
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Terminated!")
        text=' %s requested a termination .. ' % user
        f_send(bot,group,text)
        #bot.editMessageText(inline_message_id=update.callback_query.inline_message_id, text="Do you want to turn On or Off light? Light is ON")
        #hardcoded vars variant
        #bot.editMessageText(message_id=298, chat_id=174554240, text="Do you want to turn On or Off light? Light is OFF")
    else:
        logger.error("Error ... ")

def info_menu(bot, update):
    reply_markup = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton("start", callback_data="start"), telegram.InlineKeyboardButton("stop", callback_data="stop") , telegram.InlineKeyboardButton("status", callback_data="status")]])
    #update.message.reply_text(
    ddd = bot.sendMessage(chat_id=update.message.chat_id, text="Choose one of the following actions :", reply_markup=reply_markup)
    group = update.message.chat_id
    user = update.message.from_user.first_name
    mt = f_send(bot,group,"Choose in the next 10 seconds... %s " % user)
    #time.sleep(10)

    logger.info(update)
    #inl(bot,update)

def info_test(bot, update):
    #reply_keyboard = [['Boy', 'Girl', 'Other']]
    reply_markup = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton("start", callback_data="start"), telegram.InlineKeyboardButton("stop", callback_data="stop") , telegram.InlineKeyboardButton("status", callback_data="status")]])
    update.message.reply_text('Choose one of the following actions :',reply_markup=reply_markup)
    return True

def button(bot, update):
    query = update.callback_query
    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

def callback_handler(bot,update):
    reply_markup = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton("start", callback_data="start"), telegram.InlineKeyboardButton("stop", callback_data="stop") , telegram.InlineKeyboardButton("status", callback_data="status")]])
    update.message.reply_text('Choose one of the following actions :',reply_markup=reply_markup)
    #dp.add_handler(CallbackQueryHandler(update.message.reply_text('Choose one of the following actions :',reply_markup=reply_markup),inl))
    #return inl(bot,update)


def polling():
    """Polling function ... """
    #### Handlers ####

    dp.add_handler(RegexHandler('fuck',f_reply))
    #dp.add_handler(CommandHandler('info',info_menu))
    dp.add_handler(CommandHandler('info',info_test))
    dp.add_handler(CallbackQueryHandler(inl))

    #dp.add_error_handler(error)

    updater.start_polling()

    logger.info("Started polling ... ")

    updater.idle()

if __name__ == "__main__":
    logger = logging.getLogger('telbot')
    args = parser()
    if args.debug is True :
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else :
        logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if args.group == 'rocket':
        group = '-155882351'
    elif args.group == 'botland':
        group = '-243912457'

    #### Initialize Bpt
    bot = telegram.Bot(token='345178316:AAFxqQy7qIA7gJwUM4nmfvpjfXK0EcdUq-Q')

    if args.polling is True:
        ##### Updater
        polling()

    if args.message is True :
        ## get text from input ###
        text = args.message.decode('utf8')
        ### Send Messages
        mt = f_send(bot,group,text)
        logger.info(mt)

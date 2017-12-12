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

global updater , dp , now
now = time.ctime(int(time.time()))
#### Initialize Bpt
bot = telegram.Bot(token='345178316:AAFxqQy7qIA7gJwUM4nmfvpjfXK0EcdUq-Q')
updater = Updater(token='345178316:AAFxqQy7qIA7gJwUM4nmfvpjfXK0EcdUq-Q')
dp = updater.dispatcher

def parser():
    """Argument Parser"""
    argparser = argparse.ArgumentParser('telbot.py')
    argparser.add_argument('--message', help='Text to Send', required=False)
    argparser.add_argument('--group', help='Choose the group ... ' , choices=['rocket','botland'] )
    argparser.add_argument('--debug', help='Enable Debug Logging...' , action='store_true')
    argparser.add_argument('--polling', help='Enable Polling Mode...' , action='store_true')
    #argparser.add_argument('--polling', help='Enable Polling Mode...' , action='store_true')
    return argparser.parse_args()

def get_pretty_print(json_object):
    return json.dumps(json_object, sort_keys=True, indent=4, separators=(',', ': '))

def f_send(bot, chat, message):
    """Simle send message function"""
    try:
        bot.send_message(chat_id=chat, text=message)
        return True
    except Exception as e:
        logger.error('Something went wrong sending the message: %s ' % str(e) )
        return False

def f_reply(bot, update):
    """Send a message when swears are issued."""
    update.message.reply_text('Language ... ')

def inl(bot, update):
    """ Inline CallbackQueryHandler function """
    query = update.callback_query
    message = query.message.chat
    user_info = query.from_user
    g_name = ''
    if message.type == "group":
        user = user_info.first_name
        g_name = message.title
    elif message.type == "private":
        user = message.first_name
    group = message.id
    logger.info(query.from_user)
    logger.info(message)

    if query.data == "start":
        ### send start signal
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Started!")
        ### edit upon click
        edit_text = "Initialize from %s  @ %s " % ( user , now )
        bot.edit_message_text(text=edit_text,chat_id=query.message.chat_id,message_id=query.message.message_id)
        if g_name:
            text=' %s requested a to start the service from group %s .. ' % (user,g_name)
        else:
            text=' %s requested to start the service .. ' % user

        f_send(bot,group,text)

    elif query.data == "status":
        ### send status signal
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Find the status below : ")
        ### edit upon click
        edit_text = "Status update requested from %s @ %s " % ( user , now )
        bot.edit_message_text(text=edit_text,chat_id=query.message.chat_id,message_id=query.message.message_id)

        if g_name:
            text=' %s requested a status update from group %s .. ' % (user,g_name)
        else:
            text=' %s requested the status of the service .. ' % user

        f_send(bot,group,text)

    elif query.data == "stop":
        ### send stop signal
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Terminated!")
        ### edit upon click
        edit_text = "Stopped from %s @ %s " % ( user , now)
        bot.edit_message_text(text=edit_text,chat_id=query.message.chat_id,message_id=query.message.message_id)

        if g_name:
            text=' %s requested to stop the service from group %s .. ' % (user,g_name)
        else:
            text=' %s requested to stop the service .. ' % user

        f_send(bot,group,text)
    else:
        logger.error("Error ... ")

def info_menu(bot, update):
    """Pop UP menu for action """
    reply_markup = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton("start", callback_data="start"), telegram.InlineKeyboardButton("stop", callback_data="stop") , telegram.InlineKeyboardButton("status", callback_data="status")]])
    update.message.reply_text('Choose one of the following actions :',reply_markup=reply_markup)
    return True

def polling():
    """Polling function ... """
    #### Handlers ####

    dp.add_handler(RegexHandler('fuck',f_reply))
    dp.add_handler(CommandHandler('info',info_menu))
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

    if args.polling is True:
        ##### Updater
        polling()

    if args.message and group:
        ## get text from input ###
        text = args.message.decode('utf8')
        ### Send Messages
        mt = f_send(bot,group,text)
        logger.info(mt)

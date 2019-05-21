# Python-telegram-bot libraries
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup

# Logging and requests libraries
import logging

# Importing JSON library
import json
import random
import pandas as pd

# Importing token from config file
from config import token

# Importing the Updater object with token for updates from Telegram API
# Declaring the Dispatcher object to send information to user
# Creating the bot variable and adding our token
updater = Updater(token = token)
dispatcher = updater.dispatcher
bot = telegram.Bot(token = token)

# Logging module for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Importing our JSON file from our local path
folder_path = "..\\MotivationalQuotesBot\\"
quotes_file = "quotes.json"
json_file = folder_path + quotes_file
quotes_database = json.loads(open(json_file).read())

# Converting it to a Pandas DataFrame
df = pd.DataFrame(quotes_database)

quote_text = list(x for x in df["quoteText"])

reply_keyboard = [['/quote']]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard = True)

def start(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = "Hi there! Everybody needs motivation now and then, and we aim to provide it to you! Type /quote to get a new quote everytime!", reply_markup = markup)
    
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def quote_message(bot, update):
    random_quote = random.choice(quote_text)
    bot.send_message(chat_id = update.message.chat_id, text = random_quote)
    
quote_message_handler = CommandHandler('quote', quote_message)
dispatcher.add_handler(quote_message_handler)

def unknown(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text="Sorry, I didn't understand that command! Please try again!")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()
    
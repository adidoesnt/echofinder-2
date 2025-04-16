import telebot
from telebot.types import Message

from src.echofinder.constants import TELEGRAM_BOT_TOKEN, ENV, config

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message: Message):
    print(f"Received start command from {message.from_user.username}")
    
    reply: str = f"{config['bot']['handlers']['start']['message']}\n\n{config['bot']['handlers']['help']['message']}"
    bot.reply_to(message, reply)

@bot.message_handler(commands=['help'])
def help_handler(message: Message):
    reply: str = f"{config['bot']['handlers']['help']['message']}"
    bot.reply_to(message, reply)
    
def init_bot():
    print(f"Initialising bot in {ENV} mode...")
    
    if ENV == "dev":
        bot.infinity_polling()
    else:
        # TODO: Add webhook setup
        pass
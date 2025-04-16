import telebot
from telebot.types import Message

from src.echofinder.constants import TELEGRAM_BOT_TOKEN, ENV, config
from src.echofinder.bot.handlers import save_messages

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
    print(f"Received help command from {message.from_user.username}")
    
    reply: str = f"{config['bot']['handlers']['help']['message']}"
    bot.reply_to(message, reply)
    
@bot.message_handler(commands=['examples'])
def examples_handler(message: Message):
    print(f"Received examples command from {message.from_user.username}")
    reply: str = f"{config['bot']['handlers']['examples']['message']}"
    bot.reply_to(message, reply)
    
@bot.message_handler(commands=['search'])
def search_handler(message: Message):
    # TODO: Implement search functionality
    
    print(f"Received search command from {message.from_user.username}")
    
    reply: str = f"{config['bot']['handlers']['search']['message']}"
    bot.reply_to(message, reply) 
    
@bot.message_handler(commands=['tldr'])
def tldr_handler(message: Message):
    # TODO: Implement tldr functionality
    
    print(f"Received tldr command from {message.from_user.username}")
    reply: str = f"{config['bot']['handlers']['tldr']['message']}"
    bot.reply_to(message, reply)
    
# Save all messages that are not commands
@bot.message_handler(func=lambda message: True)
def echo_all(message: Message):
    print(f"Saving message from {message.from_user.username}: {message.text}")
    save_messages([message])
    
def set_bot_commands():
    commands = [
        telebot.types.BotCommand(command="/start", description=config['bot']['handlers']['start']['description']),
        telebot.types.BotCommand(command="/help", description=config['bot']['handlers']['help']['description']),
        telebot.types.BotCommand(command="/examples", description=config['bot']['handlers']['examples']['description']),
        telebot.types.BotCommand(command="/search", description=config['bot']['handlers']['search']['description']),
        telebot.types.BotCommand(command="/tldr", description=config['bot']['handlers']['tldr']['description']),
    ]
    
    bot.set_my_commands(commands)
    print("Bot commands set")
    
def init_bot():
    print(f"Initialising bot in {ENV} mode...")
    
    set_bot_commands()
    
    if ENV == "dev":
        print("Starting infinity polling...")
        bot.infinity_polling()
    else:
        # TODO: Add webhook setup
        pass
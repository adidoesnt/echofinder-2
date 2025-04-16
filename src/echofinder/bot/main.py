import telebot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import json

from src.echofinder.constants import TELEGRAM_BOT_TOKEN, ENV, TELEGRAM_WEBHOOK_URL, config
from src.echofinder.bot.handlers import save_messages, search_messages, summarise_messages

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
    print(f"Received search command from {message.from_user.username}")
    
    try:
        query = message.text.split(" ", 1)[1]
        print(f"Search query: {query}")
        
        process_search_query(message, query)
    except IndexError:
        reply = bot.reply_to(message, "What would you like to search for?")
        bot.register_next_step_handler(reply, get_search_query)
        
def get_search_query(message: Message):
    query = message.text
    print(f"Processing search query: {query}")
    
    process_search_query(message, query)
    
def process_search_query(message: Message, query: str):
    results = search_messages(query, message.chat.id)
    
    if not results['documents']:
        bot.reply_to(message, "No results found for your query.")
        return
    
    keyboard = InlineKeyboardMarkup()
    reply = f"I found {len(results['documents'])} results for your query. Please select one:\n"
    for i, document in enumerate(results['documents']):
        keyboard.add(InlineKeyboardButton(
            text=f"Result {i+1}",
            callback_data=json.dumps({
                "type": "see_suggestion",
                "id": results['ids'][i],
                "from_id": results['metadatas'][i]['sender_id']
            })
        ))
        reply += f"\n{i+1}. {document}"
    
    bot.reply_to(
        message,
        reply,
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_search_result_selection(call: CallbackQuery):
    data = json.loads(call.data)
    
    if data['type'] == "see_suggestion":
        msg_id = data['id']
        from_id = data['from_id']
        
        print(f"Referencing message {msg_id} from {from_id}")
        
        bot.send_message(
            chat_id=call.message.chat.id,
            text="^",
            reply_to_message_id=int(msg_id)
        )
        
        print(f"Checking from_id {from_id} against call.from_user.id {call.from_user.id}")
        
        if int(from_id) == int(call.from_user.id):
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
            
        bot.answer_callback_query(call.id, "Message referenced")
    else:
        print(f"Unknown callback data: {data}")
        bot.answer_callback_query(call.id, "Unknown action")


@bot.message_handler(commands=['tldr'])
def tldr_handler(message: Message):
    print(f"Received tldr command from {message.from_user.username}")
    
    try:
        n = message.text.split(" ", 1)[1]
        print(f"Summarise {n} messages")
        
        reply = summarise_messages(n, message.chat.id)
        bot.reply_to(message, reply)
    except IndexError:
        reply = bot.reply_to(message, "How many messages would you like to summarise?")
        bot.register_next_step_handler(reply, process_tldr_query)
        
def process_tldr_query(message: Message):
    n = message.text
    print(f"Processing tldr command for {n} messages")
    
    reply = summarise_messages(n, message.chat.id)
    bot.reply_to(message, reply)
    
# Save all messages that are not commands
@bot.message_handler(func=lambda message: True)
def save_all_messages(message: Message):
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
        print(f"Setting webhook to {TELEGRAM_WEBHOOK_URL}")
        bot.set_webhook(url=TELEGRAM_WEBHOOK_URL)
        
        print("Webhook set")
        
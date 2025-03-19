import telebot
import random
import os
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_CHATS = list(map(int, os.getenv("AUTHORIZED_CHATS", "").split(',')))

# Define port range
MIN_PORT = 10000
MAX_PORT = 65000

bot = telebot.TeleBot(BOT_TOKEN)

def change_apache_port():
    """Generate a new port and update Apache configuration"""
    new_port = random.randint(MIN_PORT, MAX_PORT)
    try:
        with open('/etc/apache2/ports.conf', 'r+') as f:
            content = f.read()
            f.seek(0)
            f.truncate()
            f.write(content.replace('Listen ', f'Listen {new_port}'))
        os.system('service apache2 restart')
    except Exception as e:
        print(f"Error updating Apache port: {e}")
    return new_port

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    if chat_id not in AUTHORIZED_CHATS:
        bot.send_message(chat_id, "You do not have access to this bot!")
        return
    
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    change_port_button = telebot.types.KeyboardButton('Change Port')
    port_history_button = telebot.types.KeyboardButton('Port History')
    markup.add(change_port_button, port_history_button)
    
    bot.send_message(chat_id, "Welcome! This bot helps you change Apache port.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Change Port')
def handle_change_port(message):
    chat_id = message.chat.id
    old_port = ""
    try:
        with open('/etc/apache2/ports.conf', 'r') as f:
            for line in f:
                if line.startswith('Listen '):
                    old_port = line.split()[1]
                    break
        new_port = change_apache_port()
        bot.send_message(chat_id, f"Old Apache port: {old_port}\nNew Apache port: {new_port}")
        with open('port_history.txt', 'a') as f:
            f.write(f"{datetime.datetime.now()} - Changed Apache port: {old_port} -> {new_port}\n")
    except Exception as e:
        bot.send_message(chat_id, "Error changing port.")
        print(f"Error: {e}")

@bot.message_handler(func=lambda message: message.text == 'Port History')
def handle_port_history(message):
    chat_id = message.chat.id
    try:
        with open('port_history.txt', 'r') as f:
            history = f.read()
            if not history:
                bot.send_message(chat_id, "Port history is empty")
            else:
                bot.send_message(chat_id, history)
    except FileNotFoundError:
        bot.send_message(chat_id, "Port history is empty")
    except Exception as e:
        bot.send_message(chat_id, "Error reading port history.")
        print(f"Error: {e}")

bot.polling()

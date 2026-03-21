import random
import re

import telebot
from telebot import types

Token = "8691555738:AAEBYYugDCgL3EPgmN8Wc3kK_AYbbuUzNtU"
bot=telebot.TeleBot(Token)

user_numbers = {}

@bot.message_handler(commands=['start','run'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello whats your name")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user = message.text
    bot.send_message(message.chat.id, f"hello {user}, here is what I can do:")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("Guess a number")
    markup.add(btn1)
    btn2 = types.KeyboardButton("Share a phone number")
    markup.add(btn2)
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)

def start_game(message):
    number = random.randint(1, 100)
    user_numbers[message.chat.id] = number
    msg = bot.send_message(message.chat.id, "Guess a number between 1 and 100:")
    bot.register_next_step_handler(msg, check)

def check(msg):
    if msg.text.isdigit():
        user_check = int(msg.text)
        number = user_numbers.get(msg.chat.id)

        if user_check == number:
            bot.send_message(msg.chat.id, "You guessed correctly")
        else:
            msg2 = bot.send_message(msg.chat.id, "Wrong, try again:")
            bot.register_next_step_handler(msg2, check)
    else:
        msg2 = bot.send_message(msg.chat.id, "Thats not a number, try again:")
        bot.register_next_step_handler(msg2, check)

def create(message):
    phone = message.text
    if re.fullmatch(r"\+?\d{8,15}", phone):
        bot.send_message(message.chat.id, f"Phone number saved: {phone}")
    else:
        msg = bot.send_message(message.chat.id, "Send a valid phone number :")
        bot.register_next_step_handler(msg, create)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Guess a number":
        start_game(message)
    elif message.text == "Share a phone number":
        create(message)

if __name__ == '__main__':
    print("Bot started")
    bot.infinity_polling()
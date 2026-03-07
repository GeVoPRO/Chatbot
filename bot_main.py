import random
from tabnanny import check

import telebot
from telebot import types

Token = "8691555738:AAEBYYugDCgL3EPgmN8Wc3kK_AYbbuUzNtU"
bot=telebot.TeleBot(Token)

@bot.message_handler(commands=['start','run'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello whats your name")
    bot.register_next_step_handler(message,get_name)

def get_name(message):
    user = message.text
    bot.send_message(message.chat.id, f"hello {user}, here is what can i do ")
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    btn1 = types.KeyboardButton(  "Guess a number")

    markup.add(btn1)

def start_game(message):
  message=bot.send_message(message.chat.id, " Guess a number Between 1 and 100:")
  bot.register_next_step_handler(message, check)


def check(message):
    number = random.randint(1,100)
    if message.text.isdigit():
        user_check = int(message.text)
        if user_check == number:
            bot.send_message(message.chat.id, " You guessed correctly")
        else:
            bot.reply_to(message.chat.id, " You guessed incorrectly it was {number}" )
    else:
        bot.reply_to(message.chat.id, "Thats not a number")


@bot.message_handler(commands=['text'])
def handle_text(message):
    if message.text == "Play game":
        start_game(message)
    else:
        replies = (message.chat.id, "try pressing a button","hello")
        bot.reply_to(message, random.choice(replies))


if __name__ == '__main__':
    print("Bot started")
    bot.infinity_polling()
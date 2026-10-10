import os
import threading
from flask import Flask
import telebot
from telebot import types

TOKEN = '8552372726:AAG76IL7tWhINFHHAbt2ngUaltSR_72fLzY'
bot = telebot.TeleBot(TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_photo = types.KeyboardButton('🖼 Показать картинку')
    btn_video = types.KeyboardButton('🎥 Показать видео')
    markup.add(btn_photo, btn_video)
    bot.send_message(message.chat.id, 'Привет! Нажми на одну из кнопок ниже:', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_buttons(message):
    if message.text == '🖼 Показать картинку':
        with open('photo.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption='Вот твоя картинка!')
    elif message.text == '🎥 Показать видео':
        with open('video.mp4', 'rb') as video:
            bot.send_document(message.chat.id, video, caption='Вот твое видео!')

if __name__ == '__main__':
    t = threading.Thread(target=run_flask)
    t.start()
    bot.infinity_polling()

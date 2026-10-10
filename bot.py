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
    btn_photo = types.KeyboardButton('📸 Улетное фото')
    btn_video = types.KeyboardButton('🎥 Памятное видео')
    btn_wish = types.KeyboardButton('✨ Загадать желание')
    markup.add(btn_photo, btn_video, btn_wish)
    bot.send_message(message.chat.id, 'Привет именинница! С 18-ти летием тебя) снизу есть много интересного, скорее жми 😇', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_buttons(message):
    if message.text == '📸 Улетное фото':
        with open('photo.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption='это точно останется в твоей голове надолго)')
    elif message.text == '🎥 Памятное видео':
        with open('video.mp4', 'rb') as video:
            bot.send_document(message.chat.id, video, caption='этот момент столь же прекрасен, как твой день рождения, дорогая ☺️')
    elif message.text == '✨ Загадать желание':
        markup_inline = types.InlineKeyboardMarkup()
        btn_blow = types.InlineKeyboardButton('🕯️ Задуть свечи и загадать', callback_data='blow_candles')
        markup_inline.add(btn_blow)
        bot.send_message(message.chat.id, "🎂 Загадай самое сокровенное желание...\n\nКогда будешь готов, нажми на кнопку ниже:", reply_markup=markup_inline)

@bot.callback_query_handler(func=lambda call: call.data == 'blow_candles')
def callback_blow(call):
    bot.answer_callback_query(call.id, "Ура! Желание загадано! 🌟")
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🎉 Ура! Свечи задуты, а твое самое заветное желание полетело исполняться во вселенную! 🌠 Пусть этот год принесет тебе тонну счастья, улыбок и сбывшихся мечт!"
    )

if __name__ == '__main__':
    t = threading.Thread(target=run_flask)
    t.start()
    bot.infinity_polling()

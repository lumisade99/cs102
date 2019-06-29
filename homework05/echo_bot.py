#простой эхо-бот

import telebot

access_token = '512638430:AAEniUwuaCe7q8TAaociCAUsRfqkA7jyDJ8'
bot = telebot.TeleBot(access_token)

@bot.message_handler(content_types=['text'])
def echo(message):
	bot.send_message(message.chat.id, message.text)



if __name__ == '__main__':
	bot.polling(none_stop=True)
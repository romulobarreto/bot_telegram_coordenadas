import telebot
import time
import random
from token_bot import token
from controllers.controller import gerador_coordenada
from daos.uc_dao import UCDao

bot = telebot.TeleBot(token)

def msg_numero(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

@bot.message_handler(commands=['menu'])
def start(message):
    bot.send_message(message.chat.id, f"""👋 Olá, {message.from_user.first_name}!
Sou o bot de coordenadas! Digite o número da UC para obter o link no Google Maps.""")

@bot.message_handler(func=lambda m: msg_numero(m.text))
def procurar_uc(message):
    numero = message.text.strip()
    sucesso, resultado = gerador_coordenada(numero, UCDao.buscar_uc)

    if sucesso:
        bot.send_message(message.chat.id, f"📍 Coordenadas encontradas:\n{resultado}")
    else:
        bot.send_message(message.chat.id, resultado)

@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "❗Digite apenas o número da UC ou envie /menu para ajuda.")

def iniciar_bot():
    print(f"🚀 Bot iniciado e rodando...")
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print(f"Erro durante polling: {e}")
            time.sleep(min(30, 5 + random.randint(1, 15)))

if __name__ == '__main__':
    iniciar_bot()

import telebot
import time
import random
from telebot.types import BotCommand, ReplyKeyboardMarkup, KeyboardButton
from token_bot import token
from controllers.controller import gerador_coordenada
from daos.uc_dao import UCDao
from daos.chave_dao import ChaveDao
from daos.poste_dao import PosteDao
from daos.trafo_dao import TrafoDao

bot = telebot.TeleBot(token)

# 🔥 Armazena o contexto do usuário
contexto_usuario = {}

# ✅ Menu fixo no chat
bot.set_my_commands([
    BotCommand("menu", "Abrir o menu"),
])

# ✅ Cria o teclado com botões
def teclado_opcoes():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton('🔌 UC'),
        KeyboardButton('🔑 Chave'),
        KeyboardButton('🗼 Poste'),
        KeyboardButton('⚡ Transformador')
    )
    return markup


# 🚀 Comando menu
@bot.message_handler(commands=['menu', 'start'])
def menu(message):
    bot.send_message(
        message.chat.id,
        f"👋 Olá, {message.from_user.first_name}!\nEscolha uma das opções abaixo:",
        reply_markup=teclado_opcoes()
    )


# 🔘 Quando clica numa opção do menu
@bot.message_handler(func=lambda m: m.text in ['🔌 UC', '🔑 Chave', '🗼 Poste', '⚡ Transformador'])
def escolher_busca(message):
    if message.text == '🔌 UC':
        contexto_usuario[message.chat.id] = 'UC'
        bot.send_message(message.chat.id, "🔢 Informe o número da UC:")

    elif message.text == '🔑 Chave':
        contexto_usuario[message.chat.id] = 'CHAVE'
        bot.send_message(message.chat.id, "🔢 Informe o número da Chave:")

    elif message.text == '🗼 Poste':
        contexto_usuario[message.chat.id] = 'POSTE'
        bot.send_message(message.chat.id, "🔢 Informe o número do Poste:")

    elif message.text == '⚡ Transformador':
        contexto_usuario[message.chat.id] = 'TRAFO'
        bot.send_message(message.chat.id, "🔢 Informe o número do Transformador:")


# 🔍 Processa o número informado
@bot.message_handler(func=lambda m: m.text.isdigit())
def processar_numero(message):
    contexto = contexto_usuario.get(message.chat.id)

    if contexto == 'UC':
        sucesso, resultado = gerador_coordenada(message.text, UCDao.buscar_uc)

    elif contexto == 'CHAVE':
        sucesso, resultado = gerador_coordenada(message.text, ChaveDao.buscar_chave)

    elif contexto == 'POSTE':
        sucesso, resultado = gerador_coordenada(message.text, PosteDao.buscar_poste)

    elif contexto == 'TRAFO':
        sucesso, resultado = gerador_coordenada(message.text, TrafoDao.buscar_trafo)

    else:
        bot.send_message(message.chat.id, "❗Escolha uma opção primeiro no menu /menu")
        return

    if sucesso:
        bot.send_message(message.chat.id, f"📍 Coordenadas encontradas:\n{resultado}")
    else:
        bot.send_message(message.chat.id, f"❌ {resultado}")

    # 🔄 Limpa o contexto após responder
    contexto_usuario.pop(message.chat.id, None)


# ❌ Mensagem padrão para qualquer coisa fora do fluxo
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(
        message.chat.id,
        "❗Digite apenas o número ou selecione uma opção no /menu",
        reply_markup=teclado_opcoes()
    )


# 🔄 Inicialização robusta
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
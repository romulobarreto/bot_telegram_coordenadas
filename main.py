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
        texto = """⚠️ *Atenção*: o número da *Chave* é formado por *9 dígitos*, sendo:
- Os *4 primeiros* correspondem ao código IBGE da cidade;
- Os *5 últimos* são os números que constam na placa do poste;
- Se não houver 5 números na placa, complete com zeros à esquerda.

📍 *Exemplo*:
Se a cidade é *Alvorada* e a placa tem o número *465*, então o número da Chave será *006000465*.

🏙️ *Códigos IBGE das Cidades*:
0060 Alvorada
0063 Amaral Ferrador
0085 Arambaré
0105 Arroio do Sal
0107 Arroio do Padre
0110 Arroio dos Ratos
0130 Arroio Grande
0160 Bagé
0163 Balneário Pinhal
0175 Barão do Triunfo
0190 Barra do Ribeiro
0270 Butiá
0350 Camaquã
0435 Candiota
0450 Canguçu
0463 Capão da Canoa
0466 Capão do Leão
0467 Capivari do Sul
0471 Carrá
0512 Cerrito
0517 Cerro Grande do Sul
0535 Charqueadas
0543 Chuí
0544 Chuvisca
0545 Cidreira
0605 Cristal
0650 Dom Feliciano
0655 Dom Pedro de Alcântara
0660 Dom Pedrito
0676 Eldorado do Sul
0690 Encruzilhada do Sul
0710 Herval
0930 Guaíba
0965 Hulha Negra
1033 Imbé
1065 Itati
1100 Jaguarão
1150 Lavras do Sul
1173 Mampituba
1177 Maquiné
1198 Mariana Pimentel
1225 Minas do Leão
1244 Morrinhos do Sul
1250 Mostardas
1350 Osório
1365 Palmares do Sul
1395 Pantano Grande
1417 Pedras Altas
1420 Pedro Osório
1440 Pelotas
1450 Pinheiro Machado
1460 Piratini
1490 Porto Alegre
1560 Rio Grande
1730 Santa Vitória do Palmar
1840 São Jerônimo
1850 São José do Norte
1880 São Lourenço do Sul
2035 Sentinela do Sul
2055 Sertão Santana
2110 Tapes
2135 Tavares
2143 Terra de Areia
2150 Torres
2160 Tramandaí
2166 Três Cachoeiras
2183 Três Forquilhas
2232 Turuçu
2300 Viamão
2380 Xangri-lá

🔢 Informe o número da *Chave*:"""
        bot.send_message(message.chat.id, texto, parse_mode="Markdown")

    elif message.text == '🗼 Poste':
        contexto_usuario[message.chat.id] = 'POSTE'
        bot.send_message(message.chat.id, "🔢 Informe o número do Poste:")

    elif message.text == '⚡ Transformador':
        contexto_usuario[message.chat.id] = 'TRAFO'
        texto = """⚠️ *Atenção*: o número do Transformador é formado por 9 dígitos, sendo:
- Os *4 primeiros* correspondem ao código IBGE da cidade;
- Os *5 últimos* são os números que constam na placa do poste;
- Se não houver 5 números na placa, complete com zeros à esquerda.

📍 *Exemplo*:
Se a cidade é *Alvorada* e a placa tem o número *465*, então o número do trafo será *006000465*.

🏙️ *Códigos IBGE das Cidades*:
0060 Alvorada
0063 Amaral Ferrador
0085 Arambaré
0105 Arroio do Sal
0107 Arroio do Padre
0110 Arroio dos Ratos
0130 Arroio Grande
0160 Bagé
0163 Balneário Pinhal
0175 Barão do Triunfo
0190 Barra do Ribeiro
0270 Butiá
0350 Camaquã
0435 Candiota
0450 Canguçu
0463 Capão da Canoa
0466 Capão do Leão
0467 Capivari do Sul
0471 Carrá
0512 Cerrito
0517 Cerro Grande do Sul
0535 Charqueadas
0543 Chuí
0544 Chuvisca
0545 Cidreira
0605 Cristal
0650 Dom Feliciano
0655 Dom Pedro de Alcântara
0660 Dom Pedrito
0676 Eldorado do Sul
0690 Encruzilhada do Sul
0710 Herval
0930 Guaíba
0965 Hulha Negra
1033 Imbé
1065 Itati
1100 Jaguarão
1150 Lavras do Sul
1173 Mampituba
1177 Maquiné
1198 Mariana Pimentel
1244 Morrinhos do Sul
1250 Mostardas
1350 Osório
1365 Palmares do Sul
1395 Pantano Grande
1417 Pedras Altas
1420 Pedro Osório
1440 Pelotas
1450 Pinheiro Machado
1460 Piratini
1490 Porto Alegre
1560 Rio Grande
1730 Santa Vitória do Palmar
1840 São Jerônimo
1850 São José do Norte
1880 São Lourenço do Sul
2035 Sentinela do Sul
2055 Sertão Santana
2110 Tapes
2135 Tavares
2143 Terra de Areia
2150 Torres
2160 Tramandaí
2166 Três Cachoeiras
2183 Três Forquilhas
2232 Turuçu
2300 Viamão
2380 Xangri-lá

🔢 Informe o número do Transformador:"""
        bot.send_message(message.chat.id, texto, parse_mode="Markdown")


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
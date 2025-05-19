import telebot
import time
import sqlite3
import random
import datetime
from chave import *

chave = chave_telegram
bot = telebot.TeleBot(chave)

def msg_numero(s):
    try:
        valor = int(s)
        return valor > 0
    except ValueError:
        return False

def buscar_numero(numero):
    conn = sqlite3.connect(local)
    cursor = conn.cursor()
    
    cursor.execute("SELECT LATITUDE, LONGITUDE FROM dados WHERE UC = ?", (numero,))
    resultado = cursor.fetchone()
    
    conn.close()
    
    if resultado:
        latitude, longitude = resultado
        return latitude, longitude
    else:
        return None, None

@bot.message_handler(func=lambda mensagem: msg_numero(mensagem.text))
def link(mensagem):
    numero = int(mensagem.text) 
    latitude, longitude = buscar_numero(numero)
    
    if latitude is not None and longitude is not None:
        link = f'https://www.google.com/maps/search/?api=1&query={latitude},{longitude}'
        bot.send_message(mensagem.chat.id, f"Segue o link de acordo com as coordenadas encontradas para a UC {numero} no sistema CS:\n\n{link}")
    else:
        bot.send_message(mensagem.chat.id, f"UC {numero} não encontrada ou não possui coordenadas!")

def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def boas_vindas(mensagem):
    if mensagem.text.lower() == '/start':
        bot.send_message(mensagem.chat.id, f"""Olá, {mensagem.from_user.first_name}, aqui é o Bot de Atendimento de coordenadas Norte e Sul! Estou pronto para lhe enviar o link do Google Maps!
                              
Digite apenas os números da UC para obter o link no Google Maps.

#Dica: Não use espaço e símbolos!
                 """)
    else:
        bot.send_message(mensagem.chat.id, f"""Olá, {mensagem.from_user.first_name}, aqui é o Bot de Atendimento de coordenadas Norte e Sul! Estou pronto para lhe enviar o link do Google Maps!
                              
Digite apenas os números da UC para obter o link no Google Maps.

#Dica: Não use espaço e símbolos!
                 """)

# Início do controle principal
def iniciar_bot():
    print(f"Bot iniciado em {datetime.datetime.now()}")

    while True:
        try:
            bot.polling(none_stop=False, timeout=60)
        except Exception as e:
            print(f"Erro durante execução: {e}")
            espera = min(300, 5 + random.randint(1, 30))  # espera entre 6 e 35s
            print(f"Aguardando {espera} segundos antes de tentar novamente...")
            time.sleep(espera)

if __name__ == '__main__':
    iniciar_bot()

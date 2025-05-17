import telebot
import time
import sqlite3
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
        bot.send_message(mensagem.chat.id, f"Segue o link de acordo com as coordenadas encontradas para a UC {numero} no sistema CS:\n \n {link}")
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

# Variável global para controle de tempo
inicio_execucao = time.time()
tempo_reinicio = 4 * 3600  # Reinicia a cada 4 horas (ajuste conforme necessário)

print(f"Bot iniciado em {datetime.datetime.now()}")

while True:
    try:
        # Verifica se é hora de reiniciar
        tempo_atual = time.time()
        tempo_decorrido = tempo_atual - inicio_execucao
        
        if tempo_decorrido >= tempo_reinicio:
            print(f"Reinício programado após {tempo_decorrido/3600:.2f} horas de execução - {datetime.datetime.now()}")
            # Força uma exceção para reiniciar o loop
            raise Exception("Reinício programado")
        
        # Tempo restante até o próximo reinício
        tempo_restante = tempo_reinicio - tempo_decorrido
        print(f"Bot em execução. Próximo reinício em {tempo_restante/3600:.2f} horas - {datetime.datetime.now()}")
        
        # Executa o polling por um período limitado e depois verifica o tempo novamente
        bot.polling(none_stop=True, timeout=60)
        
    except Exception as e:
        if str(e) == "Reinício programado":
            print("Reiniciando o bot conforme programado...")
            inicio_execucao = time.time()  # Reseta o tempo de execução
            time.sleep(1)  # Pequena pausa antes de reiniciar
        else:
            print(f"Erro na conexão: {e}")
            time.sleep(5)  # Espera 5 segundos antes de tentar novamente
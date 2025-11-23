import telebot
import json
import time
import random
import os
from datetime import datetime
from telebot.types import BotCommand, ReplyKeyboardMarkup, KeyboardButton, Message 
from token_bot import token
# IMPORTAÇÃO ATUALIZADA
from controllers.controller import gerador_coordenada, gerar_html_alimentador
from daos.uc_dao import UCDao
from daos.chave_dao import ChaveDao
from daos.poste_dao import PosteDao
from daos.trafo_dao import TrafoDao

bot = telebot.TeleBot(token)

# 🔥 Armazena o contexto do usuário
contexto_usuario = {}

# 📊 Função para registrar contagem
def registrar_consulta(tipo: str) -> None:
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    caminho = 'contagem.json'

    if os.path.exists(caminho):
        with open(caminho, 'r') as file:
            contagem = json.load(file)
    else:
        contagem = {}

    if data_hoje not in contagem:
        # Garante que todas as chaves existam na inicialização
        contagem[data_hoje] = {"UC": 0, "POSTE": 0, "CHAVE": 0, "TRAFO": 0, "MAPA_KML": 0}

    # Garante que a chave MAPA_KML exista para arquivos antigos
    if "MAPA_KML" not in contagem[data_hoje]:
         contagem[data_hoje]["MAPA_KML"] = 0

    contagem[data_hoje][tipo] += 1

    with open(caminho, 'w') as file:
        json.dump(contagem, file, indent=4)

# ✅ Menu fixo no chat
bot.set_my_commands([
    BotCommand("menu", "Abrir o menu"),
])

# --- FUNÇÕES DE LISTAGEM DE MAPAS (NOVO) ---

def listar_arquivos_kml(pasta: str) -> list[str]:
    # Retorna uma lista de nomes de arquivos .kml na pasta especificada
    if not os.path.isdir(pasta):
        return []
    arquivos_kml = [f for f in os.listdir(pasta) if f.endswith('.kml')]
    return arquivos_kml

def teclado_kml(arquivos: list[str]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # Lista no máximo 6 botões por linha para melhor visualização
    for i in range(0, len(arquivos), 3):
        markup.row(*[KeyboardButton(f) for f in arquivos[i:i+3]])

    markup.add(KeyboardButton('⬅️ Cancelar'))
    return markup


# ✅ Cria o teclado com botões (NOVO BOTÃO)
def teclado_opcoes() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton('🔌 UC'),
        KeyboardButton('🔑 Chave'),
        KeyboardButton('🗼 Poste'),
        KeyboardButton('⚡ Transformador')
    )
    # NOVO BOTÃO ADICIONADO AQUI
    markup.add(
        KeyboardButton('🗺️ Mapa Equipamentos')
    )
    return markup


# 🚀 Comando menu
@bot.message_handler(commands=['menu', 'start']) # type: ignore
def menu(message: Message) -> None:
    # Limpa o contexto ao abrir o menu principal
    contexto_usuario.pop(message.chat.id, None)
    bot.send_message(
        message.chat.id,
        f"👋 Olá, {message.from_user.first_name}!\nEscolha uma das opções abaixo:",
        reply_markup=teclado_opcoes()
    )


# 🔘 Quando clica numa opção do menu (FLUXO PARA LISTAGEM DE MAPAS)
@bot.message_handler(func=lambda m: m.text in ['🔌 UC', '🔑 Chave', '🗼 Poste', '⚡ Transformador', '🗺️ Mapa Equipamentos']) # type: ignore
def escolher_busca(message: Message) -> None:
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
... (Códigos IBGE) ...
🔢 Informe o número da *Chave*:"""
        bot.send_message(message.chat.id, texto, parse_mode="Markdown")

    elif message.text == '🗼 Poste':
        contexto_usuario[message.chat.id] = 'POSTE'
        bot.send_message(message.chat.id, "🔢 Informe o número do Poste:")

    elif message.text == '⚡ Transformador':
        contexto_usuario[message.chat.id] = 'TRAFO'
        texto = """⚠️ *Atenção*: o número do Transformador é formado por 9 dígitos, sendo:
... (Códigos IBGE) ...
🔢 Informe o número do Transformador:"""
        bot.send_message(message.chat.id, texto, parse_mode="Markdown")
    
    elif message.text == '🗺️ Mapa Equipamentos':
        # Mude para o novo fluxo de listagem de mapas
        arquivos_kml = listar_arquivos_kml('kml') # Onde 'kml' é a pasta
        
        if arquivos_kml:
            contexto_usuario[message.chat.id] = 'SELECIONAR_KML'
            bot.send_message(
                message.chat.id, 
                "🗺️ Escolha o mapa KML que deseja visualizar:", 
                reply_markup=teclado_kml(arquivos_kml)
            )
        else:
            bot.send_message(message.chat.id, "❌ Não encontrei nenhum arquivo *.kml* na pasta 'kml/'. Verifique se a pasta existe e contém arquivos.", parse_mode="Markdown")


# NOVO HANDLER: Processa a seleção do arquivo KML
@bot.message_handler(func=lambda m: contexto_usuario.get(m.chat.id) == 'SELECIONAR_KML' and m.text.endswith('.kml')) # type: ignore
def processar_selecao_kml(message: Message) -> None:
    nome_arquivo_kml = message.text
    
    mensagem_aguarde = bot.send_message(message.chat.id, f"⏳ Gerando o mapa para **{nome_arquivo_kml}**...", parse_mode="Markdown")
    
    try:
        # Chama a função do controller com o nome do arquivo KML
        caminho_arquivo = gerar_html_alimentador(nome_arquivo_kml) 

        if caminho_arquivo and os.path.exists(caminho_arquivo):
            # Envia o arquivo
            with open(caminho_arquivo, 'rb') as arquivo:
                bot.send_document(
                    message.chat.id,
                    arquivo,
                    caption=f"✅ Mapa '{nome_arquivo_kml}' gerado.",
                    reply_markup=teclado_opcoes(),
                    parse_mode="Markdown"
                )
            
            # Remove o arquivo temporário
            os.remove(caminho_arquivo)
            
            # Registra
            registrar_consulta('MAPA_KML')
            
        else:
            bot.send_message(message.chat.id, f"❌ Erro ao gerar o mapa para {nome_arquivo_kml}.", reply_markup=teclado_opcoes(), parse_mode="Markdown")

    except Exception as e:
        print(f"Erro ao processar mapa KML: {e}")
        bot.send_message(message.chat.id, "❌ Ocorreu um erro interno ao gerar o mapa. Verifique a sintaxe do KML.", reply_markup=teclado_opcoes())
    
    finally:
        bot.delete_message(message.chat.id, mensagem_aguarde.message_id)
        contexto_usuario.pop(message.chat.id, None)


# 🔍 Processa o número informado (MANTER O CÓDIGO EXISTENTE)
@bot.message_handler(func=lambda m: m.text.isdigit()) # type: ignore
def processar_numero(message: Message) -> None:
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
        bot.send_message(message.chat.id, f"📍 Coordenadas encontradas:\n{resultado}", reply_markup=teclado_opcoes())
    else:
        bot.send_message(message.chat.id, f"❌ {resultado}", reply_markup=teclado_opcoes())

    # 🔢 Atualiza contagem
    registrar_consulta(contexto)

    # 🔄 Limpa o contexto após responder
    contexto_usuario.pop(message.chat.id, None)

# Handler para cancelar e voltar
@bot.message_handler(func=lambda m: m.text == '⬅️ Cancelar') # type: ignore
def cancelar_selecao(message: Message) -> None:
    menu(message)


# ❌ Mensagem padrão para qualquer coisa fora do fluxo
@bot.message_handler(func=lambda m: True) # type: ignore
def fallback(message: Message) -> None:
    bot.send_message(
        message.chat.id,
        "❗Selecione uma das opções no meu menu. Aperte: /menu",
        reply_markup=teclado_opcoes()
    )


# 🔄 Inicialização robusta
def iniciar_bot()-> None:
    print("🚀 Bot iniciado e rodando...")
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print(f"Erro durante polling: {e}")
            time.sleep(min(30, 5 + random.randint(1, 15)))


if __name__ == '__main__':
    iniciar_bot()
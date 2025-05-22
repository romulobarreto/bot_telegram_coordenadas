from controllers.controller import gerador_coordenada
from daos.uc_dao import UCDao
import telebot
from token_bot import *

chave = token
bot = telebot.Telebot(chave)

class UCView:
    @staticmethod
    def buscar_uc():
        # Solicita input da UC ao usuário
        pass
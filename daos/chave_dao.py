import sqlite3
from models.chave import Chave

class ChaveDao:
    @staticmethod
    def buscar_chave(numero: str) -> tuple[bool, str]:
        conn = sqlite3.connect("database/chave.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT 
            LATITUDE,
            LONGITUDE
        FROM 
            CHAVE
        WHERE 
            CHAVE = ?
        """, (numero,))

        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            latitude, longitude = resultado
            return True, Chave(numero=numero, latitude=latitude, longitude=longitude)
        else:
            return False, "⚠️ Chave incorreta ou não possui coordenadas cadastradas no banco."  
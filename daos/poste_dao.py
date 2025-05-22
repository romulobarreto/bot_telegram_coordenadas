import sqlite3
from models.poste import Poste

class PosteDao:
    @staticmethod
    def buscar_poste(numero: str) -> tuple[bool, str]:
        conn = sqlite3.connect("database/poste.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT 
            LATITUDE,
            LONGITUDE
        FROM 
            POSTE
        WHERE 
            POSTE = ?
        """, (numero,))

        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            latitude, longitude = resultado
            return True, Poste(numero=numero, latitude=latitude, longitude=longitude)
        else:
            return False, "⚠️ Poste incorreto ou não possui coordenadas cadastradas no banco."
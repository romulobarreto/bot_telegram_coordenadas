import sqlite3
from models.trafo import Trafo

class TrafoDao:
    @staticmethod
    def buscar_trafo(numero: str) -> tuple[bool, str]:
        conn = sqlite3.connect("database/trafo.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT 
            LATITUDE,
            LONGITUDE
        FROM 
            TRAFO
        WHERE 
            TRANSFORMADOR = ?
        """, (numero,))

        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            latitude, longitude = resultado
            return True, Trafo(numero=numero, latitude=latitude, longitude=longitude)
        else:
            return False, "⚠️ Transformador incorreto ou não possui coordenadas cadastradas no banco."
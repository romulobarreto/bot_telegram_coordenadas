import sqlite3
from models.uc import UC

class UCDao:
    @staticmethod
    def buscar_uc(numero: str) -> tuple[bool, str]:
        conn = sqlite3.connect("database/uc.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT 
            LATITUDE,
            LONGITUDE
        FROM 
            UC
        WHERE 
            UC = ?
        """, (numero,))

        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            latitude, longitude = resultado
            return True, UC(numero=numero, latitude=latitude, longitude=longitude)
        else:
            return False, "⚠️ UC incorreta ou não possui coordenadas cadastradas no banco."
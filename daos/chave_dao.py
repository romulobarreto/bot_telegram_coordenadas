import sqlite3
import os
from models.chave import Chave

class ChaveDao:
    @staticmethod
    def buscar_chave(numero: str) -> tuple[bool, str | Chave]:
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(BASE_DIR, "..", "database", "chave.db")

            conn = sqlite3.connect(db_path)
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
                if latitude is None and longitude is None:
                    return False, "⚠️ CHAVE sem coordenadas cadastradas."
                else:
                    return True, Chave(numero=numero, latitude=latitude, longitude=longitude)
            else:
                return False, "⚠️ CHAVE incorreta."  
        except Exception as e:
            return False, f"❌ Erro ao acessar o banco: {str(e)}"
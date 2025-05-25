import sqlite3
import os
from models.poste import Poste

class PosteDao:
    @staticmethod
    def buscar_poste(numero: str) -> tuple[bool, str | Poste]:
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(BASE_DIR, "..", "database", "poste.db")

            conn = sqlite3.connect(db_path)
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
                if latitude is None and longitude is None:
                    return False, "⚠️ POSTE sem coordenadas cadastradas."
                else:
                    return True, Poste(numero=numero, latitude=latitude, longitude=longitude)
            else:
                return False, "⚠️ Poste incorreto."
        except Exception as e:
            return False, f"❌ Erro ao acessar o banco: {str(e)}"
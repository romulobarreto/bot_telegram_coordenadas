import sqlite3
import os
from models.uc import UC

class UCDao:
    @staticmethod
    def buscar_uc(numero: str) -> tuple[bool, str | UC]:
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(BASE_DIR, "..", "database", "uc.db")

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT LATITUDE, LONGITUDE FROM UC WHERE UC = ?
            """, (numero,))

            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                latitude, longitude = resultado
                if latitude is None and longitude is None:
                    return False, "⚠️ UC sem coordenadas cadastradas."
                else:
                    return True, UC(numero=numero, latitude=latitude, longitude=longitude)
            else:
                return False, "⚠️ UC incorreta."
        except Exception as e:
            return False, f"❌ Erro ao acessar o banco: {str(e)}"

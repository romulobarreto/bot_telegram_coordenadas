import sqlite3
import os
from models.trafo import Trafo

class TrafoDao:
    @staticmethod
    def buscar_trafo(numero: str) -> tuple[bool, str | Trafo]:
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(BASE_DIR, "..", "database", "trafo.db")
            
            conn = sqlite3.connect(db_path)
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
                if latitude is None and longitude is None:
                    return False, "⚠️ TRAFO sem coordenadas cadastradas."
                return True, Trafo(numero=numero, latitude=latitude, longitude=longitude)
            else:
                return False, "⚠️ TRAFO incorreto."
        except Exception as e:
            return False, f"❌ Erro ao acessar o banco: {str(e)}"
import mysql.connector
from config.db_config import ConectorConfig

class DB:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection and self.connection.is_connected():
            return self.connection
        try:
            self.connection = mysql.connector.connect(**ConectorConfig)
            return self.connection
        except Exception as e:
            print(f"Erro fatal ao conectar no banco: {e}")
            return None

    def select(self, query, params=None):
        """
        Use APENAS para ler dados (SELECT).
        Retorna uma lista de dicionários ou lista vazia se der erro.
        """
        conn = self.get_connection()
        if not conn: return []

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro no SELECT: {e}")
            print(f"Query tentada: {query}")
            return []
        finally:
            cursor.close()

    def execute(self, query, params=None):
        """
        Use para INSERT, UPDATE, DELETE.
        Faz o commit automático. 
        RETORNA: O número de linhas afetadas (int) ou None se der erro.
        """
        conn = self.get_connection()
        if not conn: return None 

        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            
            linhas_afetadas = cursor.rowcount 
            
            conn.commit() 
            
            return linhas_afetadas 
            
        except Exception as e:
            conn.rollback() 
            print(f"Erro no EXECUTE: {e}")
            return None
        finally:
            cursor.close()

db_service = DB()
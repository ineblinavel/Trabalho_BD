import mysql.connector.pooling
import logging
from config.db_config import ConectorConfig

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Database:
    """
    Gerenciador de banco de dados usando Connection Pooling.
    Isso permite múltiplas requisições simultâneas sem quebrar a conexão.
    """
    def __init__(self, pool_name="app_pool", pool_size=5):
        try:
            # Cria um pool de conexões ao iniciar a aplicação
            self.pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name=pool_name,
                pool_size=pool_size,
                **ConectorConfig
            )
            logging.info(f"Pool de conexões '{pool_name}' criado com sucesso ({pool_size} conexões).")
        except mysql.connector.Error as e:
            logging.error(f"Erro ao criar pool de conexões: {e}")
            raise

    def get_connection(self):
        """Pega uma conexão emprestada do pool."""
        try:
            conn = self.pool.get_connection()
            if not conn.is_connected():
                conn.reconnect(attempts=3, delay=2)
            return conn
        except mysql.connector.Error as e:
            logging.error(f"Falha ao obter conexão do pool: {e}")
            raise

    def fetch_all(self, query: str, params: tuple = None) -> list:
        conn = None
        try:
            conn = self.get_connection() # Pega conexão
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except mysql.connector.Error as e:
            logging.error(f"Erro no fetch_all: {e}\nQuery: {query}")
            return []
        finally:
            if conn:
                conn.close() # IMPORTANTE: Devolve a conexão para o pool

    def fetch_one(self, query: str, params: tuple = None) -> dict | None:
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except mysql.connector.Error as e:
            logging.error(f"Erro no fetch_one: {e}\nQuery: {query}")
            return None
        finally:
            if conn:
                conn.close() # Devolve a conexão para o pool

    def execute_query(self, query: str, params: tuple = None, fetch_last_id: bool = False) -> int | None:
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit() # Confirma a transação

                if fetch_last_id:
                    return cursor.lastrowid
                return cursor.rowcount
        except mysql.connector.Error as e:
            logging.error(f"Erro no execute_query: {e}\nQuery: {query}")
            if conn: # Tenta desfazer se der erro
                try: conn.rollback()
                except: pass
            return None
        finally:
            if conn:
                conn.close() # Devolve a conexão para o pool
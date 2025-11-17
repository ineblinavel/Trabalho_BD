import mysql.connector
from mysql.connector import Error
from config.db_config import ConectorConfig
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("database_queries.log"), logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

class DB:
    def __init__(self):
        self._connection = None

    def get_connection(self):
        if self._connection is not None and self._connection.is_connected():
            return self._connection
        try:
            conn = mysql.connector.connect(**ConectorConfig)
            self.connection = conn
            return conn
        except Error as e:
            logger.error(f"Error connecting to database: {e}")
            self.connection = None
            return None
        
    def execute_query(self, query, params=None, fetch=False, commit = False):
        conn = self.get_connection()
        if not conn:
            raise ConnectionError("Falha na conexão com o banco de dados. Verifique host/senha.")

        cursor = conn.cursor(dictionary=True) 
        result = None
        
        log_message = f"Executando query: {query.strip()[:100]}..."
        if params:
            log_message += f" com parâmetros: {params}"
        logger.info(log_message)
        try:
            cursor.execute(query, params)
            if fetch:
                result = cursor.fetchall()
            if commit:
                conn.commit()
                logger.info("Transação commitada.")
            
        except Error as e:
            conn.rollback()
            logger.error(f"Erro no comando SQL: {e}\nQuery: {query.strip()[:100]}...")
            raise e 
            
        finally:
            cursor.close()
        return result
    

db_service = DB()
def get_connection():
    return db_service.get_connection()
import mysql.connector
import time
import logging
from config.db_config import ConectorConfig

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Database:
    """
    Classe de gerenciamento de conexão com o banco de dados MySQL,
    projetada para resiliência em um ambiente de contêineres.
    """
    def __init__(self, max_retries: int = 5, delay: int = 5):
        """
        Inicializa a classe Database.

        Args:
            max_retries (int): Número máximo de tentativas de conexão.
            delay (int): Atraso em segundos entre as tentativas.
        """
        self.max_retries = max_retries
        self.delay = delay
        self.connection = self._connect()

    def _connect(self):
        """
        Estabelece a conexão com o banco de dados, com múltiplas tentativas.
        """
        for attempt in range(self.max_retries):
            try:
                conn = mysql.connector.connect(**ConectorConfig)
                if conn.is_connected():
                    logging.info("Conexão com o banco de dados estabelecida com sucesso.")
                    return conn
            except mysql.connector.Error as e:
                logging.warning(
                    f"Tentativa {attempt + 1} de {self.max_retries}: Falha ao conectar ao banco de dados. "
                    f"Tentando novamente em {self.delay} segundos. Erro: {e}"
                )
                time.sleep(self.delay)
        
        logging.error("Não foi possível conectar ao banco de dados após múltiplas tentativas.")
        raise ConnectionError("Falha ao conectar no banco de dados.")

    def get_connection(self):
        """
        Retorna a conexão ativa, reconectando se necessário.
        """
        if self.connection is None or not self.connection.is_connected():
            logging.info("Conexão perdida. Tentando reconectar...")
            self.connection = self._connect()
        return self.connection

    def fetch_all(self, query: str, params: tuple = None) -> list:
        """
        Executa uma consulta SELECT e retorna todos os resultados.

        Args:
            query (str): A consulta SQL a ser executada.
            params (tuple, optional): Parâmetros para a consulta.

        Returns:
            list: Uma lista de dicionários representando as linhas, ou uma lista vazia.
        """
        conn = self.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except mysql.connector.Error as e:
            logging.error(f"Erro ao executar fetch_all: {e}\nQuery: {query}")
            return []

    def fetch_one(self, query: str, params: tuple = None) -> dict | None:
        """
        Executa uma consulta SELECT e retorna o primeiro resultado.

        Args:
            query (str): A consulta SQL a ser executada.
            params (tuple, optional): Parâmetros para a consulta.

        Returns:
            dict | None: Um dicionário representando a primeira linha, ou None se não houver resultado.
        """
        conn = self.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except mysql.connector.Error as e:
            logging.error(f"Erro ao executar fetch_one: {e}\nQuery: {query}")
            return None

    def execute_query(self, query: str, params: tuple = None, fetch_last_id: bool = False) -> int | None:
        """
        Executa uma consulta de modificação (INSERT, UPDATE, DELETE).

        Args:
            query (str): A consulta SQL a ser executada.
            params (tuple, optional): Parâmetros para a consulta.
            fetch_last_id (bool): Se True, retorna o ID do último registro inserido.

        Returns:
            int | None: O ID do último registro inserido (se solicitado) ou o número
                         de linhas afetadas. Retorna None em caso de erro.
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                if fetch_last_id:
                    return cursor.lastrowid
                return cursor.rowcount
        except mysql.connector.Error as e:
            logging.error(f"Erro ao executar a query: {e}\nQuery: {query}")
            conn.rollback()
            return None

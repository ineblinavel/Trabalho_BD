import mysql.connector
from mysql.connector import Error
from config.db_config import ConectorConfig

def get_connection():
    try:
        conn = mysql.connector.connect(**ConectorConfig)
        return conn
    except Error as e:
        print(f"Erro na conexão: {e}")
        return None

def setup_database(script_file):
    conn = get_connection()
    if not conn:
        print("Falha na conexão. Verifique host/senha.")
        return

    cursor = conn.cursor()
    
    print("Lendo script SQL...")
    with open(script_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    commands = sql_script.split(';')
    
    for command in commands:
        if command.strip():
            try:
                cursor.execute(command)
                print(f"Executado: {command[:40]}...")
            except Error as e:
                print(f"Erro no comando: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Banco de dados configurado com sucesso!")
if __name__ == "__main__":
    setup_database('./scripts/Script.sql')
    setup_database('./scripts/Populate.sql')
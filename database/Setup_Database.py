from database.Database import get_connection
def drop_all_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

    cursor.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'GerenciamentoHospital';
    """)

    tables = cursor.fetchall()

    for (table,) in tables:
        print("Dropping table:", table)
        cursor.execute(f"DROP TABLE IF EXISTS `{table}`;")

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    conn.commit()
    cursor.close()
    conn.close()

def run_sql(file):
    conn = get_connection()
    if not conn:
        print("Falha na conexão. Verifique host/senha.")
        return

    cursor = conn.cursor()
    
    with open(file, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    commands = sql_script.split(';')
    
    for command in commands:
        if command.strip():
            try:
                cursor.execute(command)
            except Exception as e:
                print(f"Erro no comando: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()

def setup_database():
    drop_all_tables()
    run_sql('./sql/Script.sql')
    run_sql('./sql/Populate.sql')



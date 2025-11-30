from database.Database import Database

class LogSalarioRepository:
    def __init__(self, db: Database):
        self.db = db

    def get_all_logs(self, crm=None) -> list:
        query = """
            SELECT l.*, m.nome_medico 
            FROM LogSalario l
            JOIN Medicos m ON l.crm_medico = m.crm
        """
        params = []
        
        if crm:
            query += " WHERE l.crm_medico LIKE %s"
            params.append(f"%{crm}%")
            
        query += " ORDER BY l.data_alteracao DESC"
        
        return self.db.fetch_all(query, tuple(params))

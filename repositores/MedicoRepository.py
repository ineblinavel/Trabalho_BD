from database.Database import db_service

class MedicoRepository:
    def find_all(self):
        query = "SELECT * FROM Medicos;"
        results = db_service.execute_query(query, fetch=True)
        return results
    def find_by_crm(self, crm):
        query = "SELECT * FROM Medicos WHERE crm = %s;"
        params = (crm,)
        results = db_service.execute_query(query, params=params, fetch=True)
        return results[0] if results else None
    def save(self, crm, nome, cpf, salario):
        query = """
        INSERT INTO Medicos (crm, nome_medico, cpf, salario) 
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            nome_medico = VALUES(nome_medico),
            cpf = VALUES(cpf),
            salario = VALUES(salario);
        """
        params = (crm, nome, cpf, salario)
        try:
            db_service.execute_query(query, params=params, commit=True)
            return True
        except Exception as e:
            print(f"Erro ao salvar médico: {e}")
            return False
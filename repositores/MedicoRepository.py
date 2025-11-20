from database.Database import db_service

class MedicoRepository:
    def find_all(self):
        """
        Retorna todos os médicos cadastrados no banco de dados.
        """
        query = "SELECT * FROM Medicos;"
        results = db_service.select(query)
        return results

    def find_by_crm(self, crm):
        """
        crm: str
        Retorna um médico pelo CRM.
        Retorna None se o médico não for encontrado.
        """
        query = "SELECT * FROM Medicos WHERE crm = %s;"
        params = (crm,)
        results = db_service.select(query, params=params)
        return results[0] if results else None

    def save(self, crm, nome, cpf, salario):
        """
        Salva um médico no banco de dados (Insert ou Update).
        Retorna True se a operação for bem-sucedida.
        """
        query = """
        INSERT INTO Medicos (crm, nome_medico, cpf, salario) 
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            nome_medico = VALUES(nome_medico),
            cpf = VALUES(cpf),
            salario = VALUES(salario);
        """
        params = (crm, nome, cpf, salario)
        
        result = db_service.execute(query, params=params)
        
        if result is None:
            print("Erro ao salvar médico: Falha na execução do SQL.")
            return False
            
        return True

    def delete(self, crm):
        """
        Deleta (desativa) um médico pelo CRM.
        Retorna True se um registro foi efetivamente alterado.
        Retorna False se o médico não existia, já estava inativo ou houve erro.
        """
        query = "UPDATE Medicos SET ativo = FALSE WHERE crm = %s;"
        
        linhas_afetadas = db_service.execute(query, params=(crm,))
        
        if linhas_afetadas is None:
            return False
            
        if linhas_afetadas > 0:
            return True
        else:
            print(f"Aviso: Nenhum médico ativo encontrado com o CRM {crm}.")
            return False
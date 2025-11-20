from database.Database import db_service

class MedicoRepository:
    def find_all(self):
        """
        Retorna todos os médicos ativos cadastrados no banco de dados.
        """
        query = "SELECT * FROM Medicos WHERE ativo = TRUE;"
        results = db_service.select(query)
        return results

    def find_by(self, value, key="crm", ativo = True):
        """
        Retorna um médico baseado em um campo específico (padrão é 'crm').
        """
        possible_keys = ["crm", "nome_medico", "cpf"]
        if key not in possible_keys:
            raise ValueError(f"Chave inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM Medicos WHERE {key} = %s AND ativo = %s;"
        results = db_service.select(query, params=(value, ativo))
        if key == "nome_medico":
            return results if results else []
        return results[0] if results else None
    
    def create(self, crm, nome_medico, cpf, salario):
        """
        Cria (INSERT) um novo médico.
        Retorna True se a criação foi bem-sucedida, False caso contrário.
        """
        query = """
        INSERT INTO Medicos (crm, nome_medico, cpf, salario, ativo)
        VALUES (%s, %s, %s, %s, TRUE);
        """
        params = (crm, nome_medico, cpf, salario)
        
        result = db_service.execute(query, params=params)
        return result is not None
    def update(self, crm, nome_medico=None, cpf=None, salario=None):
        """
        Atualiza (UPDATE) os dados de um médico baseado no CRM.
        Apenas os campos fornecidos serão atualizados.
        Retorna True se a atualização foi bem-sucedida, False caso contrário.
        """
        fields = []
        params = []
        
        if nome_medico is not None:
            fields.append("nome_medico = %s")
            params.append(nome_medico)
        if cpf is not None:
            fields.append("cpf = %s")
            params.append(cpf)
        if salario is not None:
            fields.append("salario = %s")
            params.append(salario)
        
        if not fields:
            return False  # Nenhum campo para atualizar
        
        params.append(crm)
        query = f"UPDATE Medicos SET {', '.join(fields)} WHERE crm = %s;"
        
        linhas = db_service.execute(query, params=params)
        
        return linhas is not None
    
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
    def medico_historico(self):
        """
        Retorna todos os médicos, incluindo os inativos.
        """
        query = "SELECT * FROM Medicos"
        results = db_service.select(query)
        return results if results else None
    def medicos_inativos(self):
        """
        Retorna todos os médicos inativos.
        """
        query = "SELECT * FROM Medicos WHERE ativo = FALSE;"
        results = db_service.select(query)
        return results if results else None
    
    def reactivate_medico(self, crm):
        """
        Reativa um médico pelo CRM.
        Retorna True se um registro foi efetivamente alterado.
        Retorna False se o médico não existia, já estava ativo ou houve erro.
        """
        query = "UPDATE Medicos SET ativo = TRUE WHERE crm = %s;"
        
        linhas_afetadas = db_service.execute(query, params=(crm,))
        
        if linhas_afetadas is None:
            return False
            
        if linhas_afetadas > 0:
            return True
        else:
            print(f"Aviso: Nenhum médico inativo encontrado com o CRM {crm}.")
            return False
    def medicos_salario(self, piso = 0, teto = 1000000):
        """
        Retorna todos os médicos com salário dentro de um intervalo especificado.
        """
        query = "SELECT * FROM Medicos WHERE salario BETWEEN %s AND %s AND ativo = TRUE;"
        results = db_service.select(query, params=(piso, teto))
        return results
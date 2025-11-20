from database.Database import db_service
from datetime import datetime

class AgendaMedicoRepository:

    def find_all(self):
        query = "SELECT * FROM AgendaMedico;"
        return db_service.select(query)

    def find_by(self, value, key="id_agenda"):
        possible_keys = ["id_agenda", "crm_medico", "data"]
        if key not in possible_keys:
            raise ValueError(f"Chave inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM AgendaMedico WHERE {key} = %s;"
        results = db_service.select(query, params=(value,))
        if key == "data":
            return results if results else []
        return results if results else None


    def create(self, crm, data, inicio, fim, duracao):
        """
        Cria (INSERT) uma nova agenda.
        """
        if not self._validar_dados(data, inicio, fim):
            return False

        query = """
        INSERT INTO AgendaMedico (crm_medico, data, inicio_platao, fim_platao, duracao_slot_minutos)
        VALUES (%s, %s, %s, %s, %s);
        """
        params = (crm, data, inicio, fim, duracao)
        
        result = db_service.execute(query, params=params)
        return result is not None

    def update(self, id_agenda, data, inicio, fim, duracao):
        """
        Atualiza (UPDATE) uma agenda existente baseada no ID.
        Permite mudar até a data se necessário.
        """
        if not self._validar_dados(data, inicio, fim):
            return False

        query = """
        UPDATE AgendaMedico 
        SET data = %s, 
            inicio_platao = %s, 
            fim_platao = %s, 
            duracao_slot_minutos = %s
        WHERE id_agenda = %s;
        """
        params = (data, inicio, fim, duracao, id_agenda)
        
        linhas = db_service.execute(query, params=params)
        
        return linhas is not None

    def delete(self, id_agenda):
        """
        Deleta pelo ID 
        retorna True se deletou, False se não encontrou ou erro.
        """
        query = "DELETE FROM AgendaMedico WHERE id_agenda = %s;"
        linhas = db_service.execute(query, params=(id_agenda,))
        return linhas is not None and linhas > 0

    def _validar_dados(self, data, inicio, fim):
        """Função auxiliar para não repetir código de validação"""
        try:
            datetime.strptime(data, '%Y-%m-%d')
            datetime.strptime(inicio, '%H:%M:%S')
            datetime.strptime(fim, '%H:%M:%S')
            return True
        except ValueError:
            print("Erro de validação: Formatos de data/hora inválidos.")
            return False
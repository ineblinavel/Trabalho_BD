from database.Database import db_service
from datetime import datetime

class ConsultaRepository:
    
    def find_all(self):
        """
        Retorna todas as consultas cadastradas.
        """
        query = "SELECT * FROM Consulta;"
        return db_service.select(query)

    def find_by(self, value, key="id_consulta"):
        """
        Método universal de busca.
        Keys suportadas: 'id_consulta', 'crm_medico', 'id_paciente', 'cpf_paciente'.
        
        Retorno:
        - Lista [] se a chave for 'crm_medico', 'id_paciente' ou 'cpf_paciente'.
        - Objeto {} ou None se a chave for 'id_consulta' (única).
        """
        possible_keys = ["id_consulta", "crm_medico", "id_paciente", "cpf_paciente"]
        
        if key not in possible_keys:
            print(f"Erro: Chave '{key}' inválida. Use: {possible_keys}")
            return None

        if key == "cpf_paciente":
            query_paciente = "SELECT id_paciente FROM Paciente WHERE cpf = %s;"
            paciente = db_service.select(query_paciente, params=(value,))
            
            if not paciente:
                return [] 
            
            key = "id_paciente"
            value = paciente[0]['id_paciente']

        query = f"SELECT * FROM Consulta WHERE {key} = %s;"
        results = db_service.select(query, params=(value,))

        if key == "id_consulta":
            return results[0] if results else None
        else:
            return results if results else []

    def create(self, crm_medico, cpf_paciente, data_consulta, hora_consulta, valor):
        """
        Cria uma nova consulta.
        """
        query_paciente = "SELECT id_paciente FROM Paciente WHERE cpf = %s;"
        paciente = db_service.select(query_paciente, params=(cpf_paciente,))
        
        if not paciente:
            print(f"Erro: Paciente com CPF {cpf_paciente} não encontrado.")
            return False
            
        id_paciente = paciente[0]['id_paciente']
        # Validação de Data/Hora
        try:
            data_hora_str = f"{data_consulta} {hora_consulta}"
            datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("Erro: Formato de data/hora inválido.")
            return False

        query = """
        INSERT INTO Consulta (crm_medico, diagnostico, status, valor, data_hora_agendamento, id_paciente)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        params = (crm_medico, "Sem Diagnóstico", "A", valor, data_hora_str, id_paciente)
        
        return db_service.execute(query, params=params) is not None

    def update(self, id_consulta, status=None, diagnostico=None, data=None, hora=None):
        """
        Atualiza dados da consulta (Status, Diagnóstico ou Reagendamento).
        """
        fields = []
        params = []
        
        if status is not None:
            fields.append("status = %s")
            params.append(status)
        if diagnostico is not None:
            fields.append("diagnostico = %s")
            params.append(diagnostico)
            
        if data is not None and hora is not None:
            try:
                data_hora_str = f"{data} {hora}"
                datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S")
                fields.append("data_hora_agendamento = %s")
                params.append(data_hora_str)
            except ValueError:
                print("Erro: Data/Hora inválidas para atualização.")
                return False
        
        if not fields:
            return False
        
        params.append(id_consulta)
        
        query = f"UPDATE Consulta SET {', '.join(fields)} WHERE id_consulta = %s;"
        return db_service.execute(query, params=params) is not None

    def delete(self, id_consulta):
        """
        Cancela a consulta.
        """
        query = "DELETE FROM Consulta WHERE id_consulta = %s;"
        linhas = db_service.execute(query, params=(id_consulta,))
        return linhas is not None and linhas > 0
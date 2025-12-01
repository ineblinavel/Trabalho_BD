from database.Database import Database

class ConsultasRepository:
    """
    Classe responsável pela persistência de dados relacionados às consultas médicas.
    """

    def __init__(self, db: Database):
        """
        Inicializa uma instância de ConsultasRepository.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def create(self, crm: str, id_paciente: int, data_hora: str) -> dict:
        """
        Agenda uma nova consulta médica utilizando a stored procedure SP_AgendarConsulta.

        Args:
            crm (str): CRM do médico responsável.
            id_paciente (int): ID do paciente.
            data_hora (str): Data e hora da consulta no formato 'YYYY-MM-DD HH:MM:SS'.

        Returns:
            dict: Um dicionário com o resultado da operação.
        """
        query = "CALL SP_AgendarConsulta(%s, %s, %s)"
        params = (crm, id_paciente, data_hora)
        self.db.execute_query(query, params)
        return {"message": "Consulta agendada com sucesso."}

    def get_all(self) -> list:
        """
        Busca todas as consultas agendadas.

        Returns:
            list: Uma lista de dicionários, onde cada dicionário representa uma consulta.
        """
        query = "SELECT * FROM Consulta"
        return self.db.fetch_all(query)

    def get_by_id(self, id_consulta: int) -> dict:
        """
        Busca uma consulta específica pelo seu ID.

        Args:
            id_consulta (int): O ID da consulta a ser buscada.

        Returns:
            dict: Um dicionário representando a consulta encontrada, ou None se não for encontrada.
        """
        query = "SELECT * FROM Consulta WHERE id_consulta = %s"
        params = (id_consulta,)
        return self.db.fetch_one(query, params)

    def get_by_medico(self, crm: str) -> list:
        """
        Busca todas as consultas de um médico específico.

        Args:
            crm (str): CRM do médico cujas consultas serão buscadas.

        Returns:
            list: Uma lista de dicionários, onde cada dicionário representa uma consulta do médico.
        """
        query = """
            SELECT c.*, p.nome_paciente as nome_paciente 
            FROM Consulta c
            JOIN Paciente p ON c.id_paciente = p.id_paciente
            WHERE c.crm_medico = %s
            ORDER BY c.data_hora_agendamento DESC
        """
        return self.db.fetch_all(query, (crm,))

    def update(self, id_consulta: int, status: str = None, data_hora: str = None, diagnostico: str = None) -> dict:
        """
        Atualiza informações de uma consulta existente.

        Args:
            id_consulta (int): O ID da consulta a ser atualizada.
            status (str, optional): O novo status da consulta.
            data_hora (str, optional): A nova data e hora da consulta.

        Returns:
            dict: Um dicionário com o resultado da operação.
        """
        query = "UPDATE Consulta SET"
        params = []

        if status:
            query += " status = %s,"
            params.append(status)

        if data_hora:
            query += " data_hora_agendamento = %s,"
            params.append(data_hora)
            
        if diagnostico:
            query += " diagnostico = %s,"
            params.append(diagnostico)

        query = query.rstrip(',') + " WHERE id_consulta = %s"
        params.append(id_consulta)

        self.db.execute_query(query, tuple(params))
        return {"message": "Consulta atualizada com sucesso."}

    def delete(self, id_consulta: int) -> dict:
        """
        Remove uma consulta do banco de dados.

        Args:
            id_consulta (int): O ID da consulta a ser removida.

        Returns:
            dict: Um dicionário com o resultado da operação.
        """
        query = "DELETE FROM Consulta WHERE id_consulta = %s"
        params = (id_consulta,)
        self.db.execute_query(query, params)
        return {"message": "Consulta removida com sucesso."}

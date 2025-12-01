from database.Database import Database
from datetime import datetime

class ExameRepository:
    """
    Classe de repositório para gerenciar as operações de persistência de dados dos exames.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de exames.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def find_all(self) -> list:
        """
        Busca todos os exames cadastrados.

        Returns:
            list: Uma lista de dicionários, cada um representando um exame.
        """
        query = "SELECT * FROM Exame;"
        return self.db.fetch_all(query)

    def find_all_with_details(self) -> list:
        """
        Busca todos os exames com detalhes (nomes).
        """
        query = """
            SELECT e.*, p.nome_paciente, m.nome_medico as nome_medico_responsavel,
                   te.nome_do_exame, re.resultado_obtido, re.data_resultado
            FROM Exame e
            JOIN Paciente p ON e.id_paciente = p.id_paciente
            JOIN Medicos m ON e.crm_medico_responsavel = m.crm
            JOIN TipoExame te ON e.id_tipo_exame = te.id_tipo_exame
            LEFT JOIN ResultadoExame re ON e.id_exame = re.id_exame
            ORDER BY e.data_solicitacao DESC;
        """
        return self.db.fetch_all(query)

    def find_by(self, value, key: str = "id_exame") -> list | dict | None:
        """
        Busca exames por um campo e valor específicos.

        Args:
            value: O valor a ser buscado.
            key (str): O campo pelo qual buscar (e.g., "id_exame", "id_paciente", "status").

        Returns:
            list | dict | None: Um dicionário se a busca for por 'id_exame', uma lista
                                 para outras chaves, ou None se nada for encontrado.
        """
        possible_keys = ["id_exame", "crm_medico_responsavel", "id_paciente", "id_tipo_exame", "status"]
        if key not in possible_keys:
            raise ValueError(f"Chave de busca inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM Exame WHERE {key} = %s;"
        results = self.db.fetch_all(query, params=(value,))

        if key == "id_exame":
            return results[0] if results else None
        return results

    def create(self, status: str, crm_medico_responsavel: str, data_solicitacao: str, id_paciente: int, id_tipo_exame: int, data_coleta: str = None) -> dict:
        """
        Cria uma nova solicitação de exame.

        Args:
            status (str): Status inicial do exame (e.g., 'A' para Agendado).
            crm_medico_responsavel (str): CRM do médico que solicitou o exame.
            data_solicitacao (str): Data da solicitação ('YYYY-MM-DD').
            id_paciente (int): ID do paciente.
            id_tipo_exame (int): ID do tipo de exame.
            data_coleta (str, optional): Data da coleta ('YYYY-MM-DD').

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        self._validate_date(data_solicitacao)
        if data_coleta:
            self._validate_date(data_coleta)

        query = """
        INSERT INTO Exame (status, crm_medico_responsavel, data_coleta, data_solicitacao, id_paciente, id_tipo_exame)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        params = (status, crm_medico_responsavel, data_coleta, data_solicitacao, id_paciente, id_tipo_exame)
        self.db.execute_query(query, params=params)
        return {"message": "Exame criado com sucesso."}

    def update(self, id_exame: int, **kwargs) -> dict:
        """
        Atualiza os dados de um exame.

        Args:
            id_exame (int): O ID do exame a ser atualizado.
            **kwargs: Campos a serem atualizados (e.g., status='R').

        Returns:
            dict: Dicionário com mensagem de sucesso ou aviso.
        """
        fields = []
        params = []
        
        for key, value in kwargs.items():
            if key in ["status", "crm_medico_responsavel", "data_coleta", "data_solicitacao", "id_paciente", "id_tipo_exame"]:
                if key in ["data_coleta", "data_solicitacao"] and value:
                    self._validate_date(value)
                fields.append(f"{key} = %s")
                params.append(value)

        if not fields:
            return {"message": "Nenhum dado fornecido para atualização."}
        
        params.append(id_exame)
        query = f"UPDATE Exame SET {', '.join(fields)} WHERE id_exame = %s;"
        self.db.execute_query(query, params=tuple(params))
        return {"message": "Exame atualizado com sucesso."}

    def find_by_solicitation_date(self, start_date: str, end_date: str) -> list:
        """
        Busca exames por período de data de solicitação.

        Args:
            start_date (str): Data de início do período ('YYYY-MM-DD').
            end_date (str): Data de fim do período ('YYYY-MM-DD').

        Returns:
            list: Lista de exames encontrados no período.
        """
        query = "SELECT * FROM Exame WHERE data_solicitacao BETWEEN %s AND %s;"
        params = (start_date, end_date)
        return self.db.fetch_all(query, params=params)

    def find_by_paciente_and_status(self, id_paciente: int, status: str) -> list:
        """
        Busca exames de um paciente com um status específico.

        Args:
            id_paciente (int): ID do paciente.
            status (str): Status do exame a ser buscado.

        Returns:
            list: Lista de exames encontrados.
        """
        query = "SELECT * FROM Exame WHERE id_paciente = %s AND status = %s;"
        params = (id_paciente, status)
        return self.db.fetch_all(query, params=params)

    def find_by_medico(self, crm: str) -> list:
        """
        Busca exames solicitados por um médico específico, incluindo detalhes.

        Args:
            crm (str): CRM do médico.

        Returns:
            list: Lista de exames encontrados com detalhes.
        """
        query = """
            SELECT e.*, p.nome_paciente, te.nome_do_exame, re.resultado_obtido
            FROM Exame e
            JOIN Paciente p ON e.id_paciente = p.id_paciente
            JOIN TipoExame te ON e.id_tipo_exame = te.id_tipo_exame
            LEFT JOIN ResultadoExame re ON e.id_exame = re.id_exame
            WHERE e.crm_medico_responsavel = %s
            ORDER BY e.data_solicitacao DESC;
        """
        return self.db.fetch_all(query, params=(crm,))

    def find_with_details_by_id(self, id_exame: int) -> dict | None:
        """
        Busca um exame e seus detalhes (paciente, médico, tipo, resultado) por ID.

        Args:
            id_exame (int): O ID do exame a ser buscado.

        Returns:
            dict | None: Um dicionário com os detalhes do exame ou None se não encontrado.
        """
        query = """
            SELECT e.*, p.nome_paciente, m.nome_medico as nome_medico_responsavel,
                   te.nome_do_exame, re.resultado_obtido, re.data_resultado
            FROM Exame e
            JOIN Paciente p ON e.id_paciente = p.id_paciente
            JOIN Medicos m ON e.crm_medico_responsavel = m.crm
            JOIN TipoExame te ON e.id_tipo_exame = te.id_tipo_exame
            LEFT JOIN ResultadoExame re ON e.id_exame = re.id_exame
            WHERE e.id_exame = %s;
        """
        results = self.db.fetch_all(query, params=(id_exame,))
        return results[0] if results else None

    def delete(self, id_exame: int) -> dict:
        """
        Deleta um exame pelo seu ID.

        Args:
            id_exame (int): O ID do exame a ser deletado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM Exame WHERE id_exame = %s;"
        self.db.execute_query(query, params=(id_exame,))
        return {"message": "Exame deletado com sucesso."}

    def _validate_date(self, date_string: str):
        """Valida o formato de uma string de data."""
        try:
            if date_string:
                datetime.strptime(date_string, '%Y-%m-%d')
        except (ValueError, TypeError):
            raise ValueError(f"Formato de data inválido: '{date_string}'. Use 'YYYY-MM-DD'.")
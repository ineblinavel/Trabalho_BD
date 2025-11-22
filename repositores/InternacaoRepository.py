from database.Database import Database
from datetime import datetime

class InternacaoRepository:
    """
    Classe de repositório para gerenciar as operações de persistência
    de dados das internações.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de internações.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def find_all(self) -> list:
        """
        Busca todas as internações cadastradas.

        Returns:
            list: Uma lista de dicionários, cada um representando uma internação.
        """
        query = "SELECT * FROM Internacao;"
        return self.db.fetch_all(query)

    def find_by(self, value, key: str = "id_internacao") -> list | dict | None:
        """
        Busca internações por um campo e valor específicos.

        Args:
            value: O valor a ser buscado.
            key (str): O campo pelo qual buscar (e.g., "id_internacao", "id_paciente").

        Returns:
            list | dict | None: Um dicionário se a busca for por 'id_internacao', uma
                                 lista para outras chaves, ou None se nada for encontrado.
        """
        possible_keys = ["id_internacao", "id_paciente", "crm_medico", "corem_enfermeiro", "id_quarto"]
        if key not in possible_keys:
            raise ValueError(f"Chave de busca inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM Internacao WHERE {key} = %s;"
        results = self.db.fetch_all(query, params=(value,))

        if key == "id_internacao":
            return results[0] if results else None
        return results

    def create(self, id_paciente: int, crm_medico: str, corem_enfermeiro: str, **kwargs) -> dict:
        """
        Cria um novo registro de internação.

        Args:
            id_paciente (int): ID do paciente.
            crm_medico (str): CRM do médico responsável.
            corem_enfermeiro (str): COREM do enfermeiro responsável.
            **kwargs: Outros campos como 'id_quarto', 'data_admissao', 'data_alta_prevista'.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        data_admissao = kwargs.get("data_admissao")
        data_alta_prevista = kwargs.get("data_alta_prevista")
        self._validate_dates({"data_admissao": data_admissao, "data_alta_prevista": data_alta_prevista})

        query = """
        INSERT INTO Internacao (id_paciente, crm_medico, corem_enfermeiro, id_quarto, data_admissao, data_alta_prevista, data_alta_efetiva)
        VALUES (%s, %s, %s, %s, %s, %s, NULL);
        """
        params = (id_paciente, crm_medico, corem_enfermeiro, kwargs.get("id_quarto"), data_admissao, data_alta_prevista)
        self.db.execute_query(query, params=params)
        return {"message": "Internação criada com sucesso."}

    def update(self, id_internacao: int, **kwargs) -> dict:
        """
        Atualiza os dados de uma internação.

        Args:
            id_internacao (int): O ID da internação a ser atualizada.
            **kwargs: Campos a serem atualizados (e.g., id_quarto=5).

        Returns:
            dict: Dicionário com mensagem de sucesso ou aviso.
        """
        date_fields = ["data_admissao", "data_alta_prevista", "data_alta_efetiva"]
        dates_to_validate = {key: value for key, value in kwargs.items() if key in date_fields}
        self._validate_dates(dates_to_validate)

        fields = []
        params = []
        for key, value in kwargs.items():
            if key in ["id_paciente", "crm_medico", "corem_enfermeiro", "id_quarto"] + date_fields:
                fields.append(f"{key} = %s")
                params.append(value)

        if not fields:
            return {"message": "Nenhum dado fornecido para atualização."}
        
        params.append(id_internacao)
        query = f"UPDATE Internacao SET {', '.join(fields)} WHERE id_internacao = %s;"
        self.db.execute_query(query, params=tuple(params))
        return {"message": "Internação atualizada com sucesso."}

    def realizar_alta(self, id_internacao: int, data_alta_efetiva: str) -> dict:
        """
        Executa a alta de um paciente chamando a procedure SP_RealizarAltaPaciente.

        Args:
            id_internacao (int): O ID da internação para dar alta.
            data_alta_efetiva (str): A data efetiva da alta no formato 'YYYY-MM-DD'.
        
        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        self._validate_dates({"data_alta_efetiva": data_alta_efetiva})
        query = "CALL SP_RealizarAltaPaciente(%s, %s);"
        params = (id_internacao, data_alta_efetiva)
        self.db.execute_query(query, params)
        return {"message": "Alta do paciente realizada com sucesso."}

    def find_active(self) -> list:
        """
        Encontra todas as internações ativas (sem data de alta efetiva).

        Returns:
            list: Lista de internações ativas.
        """
        query = "SELECT * FROM Internacao WHERE data_alta_efetiva IS NULL;"
        return self.db.fetch_all(query)

    def find_by_admission_date(self, start_date: str, end_date: str) -> list:
        """
        Busca internações por período de data de admissão.

        Args:
            start_date (str): Data de início do período ('YYYY-MM-DD').
            end_date (str): Data de fim do período ('YYYY-MM-DD').

        Returns:
            list: Lista de internações encontradas no período.
        """
        query = "SELECT * FROM Internacao WHERE data_admissao BETWEEN %s AND %s;"
        params = (start_date, end_date)
        return self.db.fetch_all(query, params=params)

    def delete(self, id_internacao: int) -> dict:
        """
        Deleta uma internação pelo seu ID.

        Args:
            id_internacao (int): O ID da internação a ser deletada.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM Internacao WHERE id_internacao = %s;"
        self.db.execute_query(query, params=(id_internacao,))
        return {"message": "Internação deletada com sucesso."}

    def _validate_dates(self, dates: dict):
        """Valida o formato de uma ou mais strings de data."""
        for key, value in dates.items():
            try:
                if value:
                    datetime.strptime(value, '%Y-%m-%d')
            except (ValueError, TypeError):
                raise ValueError(f"Formato de data inválido para '{key}': '{value}'. Use 'YYYY-MM-DD'.")
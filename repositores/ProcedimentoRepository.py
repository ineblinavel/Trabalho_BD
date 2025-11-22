from database.Database import Database

class ProcedimentoRepository:
    """
    Classe de repositório para gerenciar as operações de persistência
    de dados dos procedimentos médicos.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de procedimentos.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def find_all(self) -> list:
        """
        Busca todos os procedimentos cadastrados.

        Returns:
            list: Uma lista de dicionários, cada um representando um procedimento.
        """
        query = "SELECT * FROM Procedimento;"
        return self.db.fetch_all(query)

    def find_by(self, value, key: str = "id_procedimento") -> list | dict | None:
        """
        Busca procedimentos por um campo e valor específicos.

        Args:
            value: O valor a ser buscado.
            key (str): O campo pelo qual buscar (e.g., "id_procedimento", "id_paciente").

        Returns:
            list | dict | None: Um dicionário se a busca for por 'id_procedimento', uma
                                 lista para outras chaves, ou None se nada for encontrado.
        """
        possible_keys = ["id_procedimento", "crm_medico", "id_paciente", "nome_procedimento"]
        if key not in possible_keys:
            raise ValueError(f"Chave de busca inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM Procedimento WHERE {key} = %s;"
        params = (value,)

        if key == "nome_procedimento":
            query = f"SELECT * FROM Procedimento WHERE {key} LIKE %s;"
            params = (f"%{value}%",)

        results = self.db.fetch_all(query, params=params)

        if key == "id_procedimento":
            return results[0] if results else None
        return results

    def create(self, crm_medico: str, id_paciente: int, nome_procedimento: str, custo: float) -> dict:
        """
        Cria um novo registro de procedimento.

        Args:
            crm_medico (str): CRM do médico que realizou o procedimento.
            id_paciente (int): ID do paciente.
            nome_procedimento (str): Nome do procedimento.
            custo (float): Custo do procedimento.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "INSERT INTO Procedimento (nome_procedimento, custo, crm_medico, id_paciente) VALUES (%s, %s, %s, %s);"
        params = (nome_procedimento, custo, crm_medico, id_paciente)
        self.db.execute_query(query, params=params)
        return {"message": "Procedimento criado com sucesso."}

    def update(self, id_procedimento: int, **kwargs) -> dict:
        """
        Atualiza os dados de um procedimento.

        Args:
            id_procedimento (int): O ID do procedimento a ser atualizado.
            **kwargs: Campos a serem atualizados (e.g., custo=150.0).

        Returns:
            dict: Dicionário com mensagem de sucesso ou aviso.
        """
        fields = []
        params = []
        
        for key, value in kwargs.items():
            if key in ["nome_procedimento", "custo", "crm_medico", "id_paciente"]:
                fields.append(f"{key} = %s")
                params.append(value)

        if not fields:
            return {"message": "Nenhum dado fornecido para atualização."}
        
        params.append(id_procedimento)
        query = f"UPDATE Procedimento SET {', '.join(fields)} WHERE id_procedimento = %s;"
        self.db.execute_query(query, params=tuple(params))
        return {"message": "Procedimento atualizado com sucesso."}

    def find_by_custo_range(self, min_custo: float, max_custo: float) -> list:
        """
        Busca procedimentos dentro de um intervalo de custo.

        Args:
            min_custo (float): Custo mínimo.
            max_custo (float): Custo máximo.

        Returns:
            list: Lista de procedimentos encontrados no intervalo.
        """
        query = "SELECT * FROM Procedimento WHERE custo BETWEEN %s AND %s;"
        params = (min_custo, max_custo)
        return self.db.fetch_all(query, params=params)

    def delete(self, id_procedimento: int) -> dict:
        """
        Deleta um procedimento pelo seu ID.

        Args:
            id_procedimento (int): O ID do procedimento a ser deletado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM Procedimento WHERE id_procedimento = %s;"
        self.db.execute_query(query, params=(id_procedimento,))
        return {"message": "Procedimento deletado com sucesso."}
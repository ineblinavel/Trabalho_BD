from database.Database import Database

class PrescricaoRepository:
    """
    Classe de repositório para gerenciar as operações de persistência
    de dados das prescrições médicas.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de prescrições.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def find_all(self) -> list:
        """
        Busca todas as prescrições cadastradas.

        Returns:
            list: Uma lista de dicionários, cada um representando uma prescrição.
        """
        query = "SELECT * FROM Prescricao;"
        return self.db.fetch_all(query)

    def find_by(self, value: int, key: str = "id_prescricao") -> list | dict | None:
        """
        Busca prescrições por um campo e valor específicos.

        Args:
            value (int): O valor a ser buscado.
            key (str): O campo pelo qual buscar (e.g., "id_prescricao", "id_consulta").

        Returns:
            list | dict | None: Um dicionário se a busca for por 'id_prescricao', uma
                                 lista para outras chaves, ou None se nada for encontrado.
        """
        possible_keys = ["id_prescricao", "id_consulta", "id_medicamento"]
        if key not in possible_keys:
            raise ValueError(f"Chave de busca inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM Prescricao WHERE {key} = %s;"
        results = self.db.fetch_all(query, params=(value,))

        if key == "id_prescricao":
            return results[0] if results else None
        return results

    def create(self, id_consulta: int, id_medicamento: int, quantidade_prescrita: int, **kwargs) -> dict:
        """
        Cria uma nova prescrição de medicamento para uma consulta.

        Args:
            id_consulta (int): ID da consulta associada.
            id_medicamento (int): ID do medicamento prescrito.
            quantidade_prescrita (int): Quantidade do medicamento.
            **kwargs: Campos opcionais como 'dosagem' e 'frequencia_uso'.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = """
        INSERT INTO Prescricao (id_consulta, id_medicamento, quantidade_prescrita, dosagem, frequencia_uso)
        VALUES (%s, %s, %s, %s, %s);
        """
        params = (id_consulta, id_medicamento, quantidade_prescrita, kwargs.get("dosagem"), kwargs.get("frequencia_uso"))
        self.db.execute_query(query, params=params)
        return {"message": "Prescrição criada com sucesso."}

    def update(self, id_prescricao: int, **kwargs) -> dict:
        """
        Atualiza os dados de uma prescrição.
        Não permite alterar os IDs da consulta ou do medicamento.

        Args:
            id_prescricao (int): O ID da prescrição a ser atualizada.
            **kwargs: Campos a serem atualizados (e.g., 'dosagem', 'frequencia_uso').

        Returns:
            dict: Dicionário com mensagem de sucesso ou aviso.
        """
        fields = []
        params = []
        
        for key, value in kwargs.items():
            if key in ["quantidade_prescrita", "dosagem", "frequencia_uso"]:
                fields.append(f"{key} = %s")
                params.append(value)

        if not fields:
            return {"message": "Nenhum dado fornecido para atualização."}
        
        params.append(id_prescricao)
        query = f"UPDATE Prescricao SET {', '.join(fields)} WHERE id_prescricao = %s;"
        self.db.execute_query(query, params=tuple(params))
        return {"message": "Prescrição atualizada com sucesso."}

    def delete(self, id_prescricao: int) -> dict:
        """
        Deleta uma prescrição pelo seu ID.

        Args:
            id_prescricao (int): O ID da prescrição a ser deletada.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM Prescricao WHERE id_prescricao = %s;"
        self.db.execute_query(query, params=(id_prescricao,))
        return {"message": "Prescrição deletada com sucesso."}

    def delete_by_consulta_and_medicamento(self, id_consulta: int, id_medicamento: int) -> dict:
        """
        Deleta uma prescrição específica pela combinação de consulta e medicamento.

        Args:
            id_consulta (int): ID da consulta.
            id_medicamento (int): ID do medicamento.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM Prescricao WHERE id_consulta = %s AND id_medicamento = %s;"
        params = (id_consulta, id_medicamento)
        self.db.execute_query(query, params=params)
        return {"message": "Prescrição específica deletada com sucesso."}

    def find_by_consulta_with_details(self, id_consulta: int) -> list:
        """
        Busca prescrições de uma consulta com detalhes do medicamento.
        """
        query = """
            SELECT p.*, m.nome_comercial, m.fabricante
            FROM Prescricao p
            JOIN Medicamentos m ON p.id_medicamento = m.id_medicamento
            WHERE p.id_consulta = %s
        """
        return self.db.fetch_all(query, (id_consulta,))
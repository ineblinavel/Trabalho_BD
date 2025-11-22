from database.Database import Database

class MedicamentoRepository:
    """
    Classe de repositório para gerenciar as operações de persistência
    de dados dos medicamentos.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de medicamentos.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def find_all(self) -> list:
        """
        Busca todos os medicamentos cadastrados.

        Returns:
            list: Uma lista de dicionários, cada um representando um medicamento.
        """
        query = "SELECT * FROM Medicamento;"
        return self.db.fetch_all(query)

    def find_by(self, value: str, key: str = "id_medicamento") -> list | dict | None:
        """
        Busca medicamentos por um campo e valor específicos.

        Args:
            value (str): O valor a ser buscado.
            key (str): O campo pelo qual buscar (e.g., "id_medicamento", "nome_comercial").

        Returns:
            list | dict | None: Um dicionário se a busca for por 'id_medicamento', uma
                                 lista para outras chaves, ou None se nada for encontrado.
        """
        possible_keys = ["id_medicamento", "fabricante", "nome_comercial"]
        if key not in possible_keys:
            raise ValueError(f"Chave de busca inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM Medicamento WHERE {key} = %s;"
        params = (value,)
        
        if key in ["fabricante", "nome_comercial"]:
            query = f"SELECT * FROM Medicamento WHERE {key} LIKE %s;"
            params = (f"%{value}%",)

        results = self.db.fetch_all(query, params=params)

        if key == "id_medicamento":
            return results[0] if results else None
        return results

    def create(self, nome_comercial: str, fabricante: str = None) -> dict:
        """
        Cria um novo registro de medicamento.

        Args:
            nome_comercial (str): Nome comercial do medicamento.
            fabricante (str, optional): Nome do fabricante.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "INSERT INTO Medicamento (fabricante, nome_comercial) VALUES (%s, %s);"
        params = (fabricante, nome_comercial)
        self.db.execute_query(query, params=params)
        return {"message": "Medicamento criado com sucesso."}

    def update(self, id_medicamento: int, **kwargs) -> dict:
        """
        Atualiza os dados de um medicamento existente.

        Args:
            id_medicamento (int): O ID do medicamento a ser atualizado.
            **kwargs: Campos a serem atualizados (e.g., fabricante="Novo Fabricante").

        Returns:
            dict: Dicionário com mensagem de sucesso ou aviso.
        """
        fields = []
        params = []
        
        for key, value in kwargs.items():
            if key in ["fabricante", "nome_comercial"]:
                fields.append(f"{key} = %s")
                params.append(value)

        if not fields:
            return {"message": "Nenhum dado fornecido para atualização."}
        
        params.append(id_medicamento)
        query = f"UPDATE Medicamento SET {', '.join(fields)} WHERE id_medicamento = %s;"
        self.db.execute_query(query, params=tuple(params))
        return {"message": "Medicamento atualizado com sucesso."}

    def delete(self, id_medicamento: int) -> dict:
        """
        Deleta um medicamento pelo seu ID.

        Args:
            id_medicamento (int): O ID do medicamento a ser deletado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM Medicamento WHERE id_medicamento = %s;"
        self.db.execute_query(query, params=(id_medicamento,))
        return {"message": "Medicamento deletado com sucesso."}
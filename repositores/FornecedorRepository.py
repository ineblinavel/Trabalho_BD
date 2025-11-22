from database.Database import Database

class FornecedorRepository:
    """
    Classe de repositório para gerenciar as operações de persistência
    de dados dos fornecedores.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de fornecedores.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def find_all(self) -> list:
        """
        Busca todos os fornecedores cadastrados.

        Returns:
            list: Uma lista de dicionários, cada um representando um fornecedor.
        """
        query = "SELECT * FROM Fornecedor;"
        return self.db.fetch_all(query)

    def find_by(self, value: str, key: str = "cnpj") -> list | dict | None:
        """
        Busca fornecedores por um campo e valor específicos.

        Args:
            value (str): O valor a ser buscado.
            key (str): O campo pelo qual buscar (e.g., "cnpj", "nome_empresa").

        Returns:
            list | dict | None: Um dicionário se a busca for por 'cnpj', uma lista para
                                 'nome_empresa', ou None se nada for encontrado.
        """
        possible_keys = ["cnpj", "nome_empresa"]
        if key not in possible_keys:
            raise ValueError(f"Chave de busca inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM Fornecedor WHERE {key} = %s;"
        params = (value,)
        
        if key == "nome_empresa":
            query = f"SELECT * FROM Fornecedor WHERE {key} LIKE %s;"
            params = (f"%{value}%",)

        results = self.db.fetch_all(query, params=params)

        if key == "cnpj":
            return results[0] if results else None
        return results

    def create(self, cnpj: str, nome_empresa: str = None) -> dict:
        """
        Cria um novo registro de fornecedor.

        Args:
            cnpj (str): CNPJ do fornecedor (identificador único).
            nome_empresa (str, optional): Nome da empresa fornecedora.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "INSERT INTO Fornecedor (cnpj, nome_empresa) VALUES (%s, %s);"
        params = (cnpj, nome_empresa)
        self.db.execute_query(query, params=params)
        return {"message": "Fornecedor criado com sucesso."}

    def update(self, cnpj: str, **kwargs) -> dict:
        """
        Atualiza os dados de um fornecedor existente.

        Args:
            cnpj (str): O CNPJ do fornecedor a ser atualizado.
            **kwargs: Campos a serem atualizados (e.g., nome_empresa="Novo Nome").

        Returns:
            dict: Dicionário com mensagem de sucesso ou aviso.
        """
        fields = []
        params = []
        
        for key, value in kwargs.items():
            if key in ["nome_empresa"]:
                fields.append(f"{key} = %s")
                params.append(value)

        if not fields:
            return {"message": "Nenhum dado fornecido para atualização."}
        
        params.append(cnpj)
        query = f"UPDATE Fornecedor SET {', '.join(fields)} WHERE cnpj = %s;"
        self.db.execute_query(query, params=tuple(params))
        return {"message": "Fornecedor atualizado com sucesso."}

    def delete(self, cnpj: str) -> dict:
        """
        Deleta um fornecedor pelo seu CNPJ.

        Args:
            cnpj (str): O CNPJ do fornecedor a ser deletado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM Fornecedor WHERE cnpj = %s;"
        self.db.execute_query(query, params=(cnpj,))
        return {"message": "Fornecedor deletado com sucesso."}
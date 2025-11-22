from database.Database import Database

class TipoExameRepository:
    """
    Classe de repositório para gerenciar os tipos de exames disponíveis.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de tipos de exame.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def find_all(self) -> list:
        """
        Busca todos os tipos de exames cadastrados.

        Returns:
            list: Uma lista de dicionários, cada um representando um tipo de exame.
        """
        query = "SELECT * FROM TipoExame;"
        return self.db.fetch_all(query)

    def find_by(self, value: str, key: str = "id_tipo_exame") -> list | dict | None:
        """
        Busca tipos de exame por um campo e valor específicos.

        Args:
            value (str): O valor a ser buscado.
            key (str): O campo pelo qual buscar (e.g., "id_tipo_exame", "nome_do_exame").

        Returns:
            list | dict | None: Um dicionário se a busca for por ID, uma lista para
                                 outras chaves, ou None se nada for encontrado.
        """
        possible_keys = ["id_tipo_exame", "nome_do_exame"]
        if key not in possible_keys:
            raise ValueError(f"Chave de busca inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM TipoExame WHERE {key} = %s;"
        params = (value,)

        if key == "nome_do_exame":
            query = f"SELECT * FROM TipoExame WHERE {key} LIKE %s;"
            params = (f"%{value}%",)
        
        results = self.db.fetch_all(query, params=params)

        if key == "id_tipo_exame":
            return results[0] if results else None
        return results

    def create(self, nome_do_exame: str, preco: float, descricao: str = None) -> dict:
        """
        Cria um novo tipo de exame.

        Args:
            nome_do_exame (str): Nome do exame (e.g., 'Hemograma Completo').
            preco (float): Preço do exame.
            descricao (str, optional): Descrição do tipo de exame.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "INSERT INTO TipoExame (nome_do_exame, descricao, preco) VALUES (%s, %s, %s);"
        params = (nome_do_exame, descricao, preco)
        self.db.execute_query(query, params=params)
        return {"message": "Tipo de exame criado com sucesso."}

    def update(self, id_tipo_exame: int, **kwargs) -> dict:
        """
        Atualiza os dados de um tipo de exame.

        Args:
            id_tipo_exame (int): O ID do tipo de exame a ser atualizado.
            **kwargs: Campos a serem atualizados (e.g., preco=100.0).

        Returns:
            dict: Dicionário com mensagem de sucesso ou aviso.
        """
        fields = []
        params = []
        
        for key, value in kwargs.items():
            if key in ["nome_do_exame", "descricao", "preco"]:
                fields.append(f"{key} = %s")
                params.append(value)
        
        if not fields:
            return {"message": "Nenhum dado fornecido para atualização."}
        
        params.append(id_tipo_exame)
        query = f"UPDATE TipoExame SET {', '.join(fields)} WHERE id_tipo_exame = %s;"
        self.db.execute_query(query, params=tuple(params))
        return {"message": "Tipo de exame atualizado com sucesso."}

    def find_by_price_range(self, min_price: float, max_price: float) -> list:
        """
        Busca tipos de exame dentro de um intervalo de preço.

        Args:
            min_price (float): Preço mínimo.
            max_price (float): Preço máximo.

        Returns:
            list: Lista de tipos de exame encontrados.
        """
        query = "SELECT * FROM TipoExame WHERE preco BETWEEN %s AND %s;"
        params = (min_price, max_price)
        return self.db.fetch_all(query, params=params)

    def delete(self, id_tipo_exame: int) -> dict:
        """
        Deleta um tipo de exame pelo seu ID.

        Args:
            id_tipo_exame (int): O ID do tipo de exame a ser deletado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM TipoExame WHERE id_tipo_exame = %s;"
        self.db.execute_query(query, params=(id_tipo_exame,))
        return {"message": "Tipo de exame deletado com sucesso."}
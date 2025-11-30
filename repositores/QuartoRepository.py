from database.Database import Database

class QuartoRepository:
    """
    Classe de repositório para gerenciar as operações de persistência
    de dados dos quartos do hospital.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de quartos.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def get_mapa_leitos(self) -> list:
        """
        Busca o status atual de todos os quartos usando a View V_QuartosStatus.
        """
        query = "SELECT * FROM V_QuartosStatus"
        return self.db.fetch_all(query)

    def get_all(self) -> list:
        """
        Busca todos os quartos cadastrados no sistema.

        Returns:
            list: Uma lista de dicionários representando todos os quartos.
        """
        query = "SELECT * FROM Quarto"
        return self.db.fetch_all(query)

    def get_by_id(self, num_quarto: int) -> dict:
        """
        Busca um quarto específico pelo seu número.

        Args:
            num_quarto (int): O número do quarto a ser buscado.

        Returns:
            dict: Um dicionário com os dados do quarto ou None se não encontrado.
        """
        query = "SELECT * FROM Quarto WHERE num_quarto = %s"
        params = (num_quarto,)
        return self.db.fetch_one(query, params)

    def create(self, num_quarto: int, tipo_de_quarto: str, valor_diaria: float) -> dict:
        """
        Cria um novo quarto no banco de dados.

        Args:
            num_quarto (int): Número do novo quarto.
            tipo_de_quarto (str): Tipo do quarto (e.g., 'Individual', 'Duplo').
            valor_diaria (float): Valor da diária do quarto.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "INSERT INTO Quarto (num_quarto, tipo_de_quarto, valor_diaria) VALUES (%s, %s, %s)"
        params = (num_quarto, tipo_de_quarto, valor_diaria)
        self.db.execute_query(query, params)
        return {"message": "Quarto criado com sucesso."}

    def update(self, num_quarto: int, tipo_de_quarto: str = None, valor_diaria: float = None) -> dict:
        """
        Atualiza os dados de um quarto.

        Args:
            num_quarto (int): Número do quarto a ser atualizado.
            tipo_de_quarto (str, optional): Novo tipo do quarto.
            valor_diaria (float, optional): Novo valor da diária.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "UPDATE Quarto SET"
        params = []

        if tipo_de_quarto is not None:
            query += " tipo_de_quarto = %s,"
            params.append(tipo_de_quarto)

        if valor_diaria is not None:
            query += " valor_diaria = %s,"
            params.append(valor_diaria)

        query = query.rstrip(',') + " WHERE num_quarto = %s"
        params.append(num_quarto)

        if len(params) > 1:
            self.db.execute_query(query, tuple(params))
            return {"message": f"Quarto {num_quarto} atualizado com sucesso."}

        return {"message": "Nenhum dado fornecido para atualização."}
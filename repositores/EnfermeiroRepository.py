from database.Database import Database

class EnfermeiroRepository:
    """
    Classe de repositório para gerenciar as operações de persistência
    de dados dos enfermeiros.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de enfermeiros.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def find_all(self) -> list:
        """
        Busca todos os enfermeiros cadastrados.

        Returns:
            list: Uma lista de dicionários, cada um representando um enfermeiro.
        """
        query = "SELECT * FROM Enfermeiro;"
        return self.db.fetch_all(query)

    def find_by(self, value: str, key: str = "corem") -> list | dict | None:
        """
        Busca enfermeiros por um campo e valor específicos.

        Args:
            value (str): O valor a ser buscado.
            key (str): O campo pelo qual buscar (e.g., "corem", "cpf", "nome_enfermeiro").

        Returns:
            list | dict | None: Um dicionário se a busca for por 'corem' ou 'cpf',
                                 uma lista para 'nome_enfermeiro', ou None se nada for encontrado.
        """
        possible_keys = ["corem", "cpf", "nome_enfermeiro"]
        if key not in possible_keys:
            raise ValueError(f"Chave de busca inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM Enfermeiro WHERE {key} = %s;"
        params = (value,)
        
        if key == "nome_enfermeiro":
            query = f"SELECT * FROM Enfermeiro WHERE {key} LIKE %s;"
            params = (f"%{value}%",)

        results = self.db.fetch_all(query, params=params)
        
        if key in ["corem", "cpf"]:
            return results[0] if results else None
        return results

    def create(self, corem: str, cpf: str, nome_enfermeiro: str) -> dict:
        """
        Cria um novo registro de enfermeiro.

        Args:
            corem (str): COREM do enfermeiro (identificador único).
            cpf (str): CPF do enfermeiro.
            nome_enfermeiro (str): Nome completo do enfermeiro.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "INSERT INTO Enfermeiro (corem, cpf, nome_enfermeiro) VALUES (%s, %s, %s);"
        params = (corem, cpf, nome_enfermeiro)
        self.db.execute_query(query, params=params)
        return {"message": "Enfermeiro criado com sucesso."}

    def update(self, corem: str, **kwargs) -> dict:
        """
        Atualiza os dados de um enfermeiro existente.

        Args:
            corem (str): O COREM do enfermeiro a ser atualizado.
            **kwargs: Campos a serem atualizados (e.g., nome_enfermeiro="Novo Nome").

        Returns:
            dict: Dicionário com mensagem de sucesso ou aviso se nenhum dado for fornecido.
        """
        fields = []
        params = []
        
        for key, value in kwargs.items():
            if key in ["cpf", "nome_enfermeiro"]:
                fields.append(f"{key} = %s")
                params.append(value)
        
        if not fields:
            return {"message": "Nenhum dado fornecido para atualização."}
        
        params.append(corem)
        
        query = f"UPDATE Enfermeiro SET {', '.join(fields)} WHERE corem = %s;"
        
        self.db.execute_query(query, params=tuple(params))
        return {"message": "Enfermeiro atualizado com sucesso."}

    def delete(self, corem: str) -> dict:
        """
        Deleta um enfermeiro pelo seu COREM.

        Args:
            corem (str): O COREM do enfermeiro a ser deletado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM Enfermeiro WHERE corem = %s;"
        self.db.execute_query(query, params=(corem,))
        return {"message": "Enfermeiro deletado com sucesso."}

    def find_by_corem_with_details(self, corem: str) -> dict | None:
        """
        Busca um enfermeiro pelo COREM, incluindo a senha do usuário.

        Args:
            corem (str): O COREM do enfermeiro.

        Returns:
            dict | None: Dados do enfermeiro com senha, ou None.
        """
        query = """
            SELECT e.*, u.password
            FROM Enfermeiro e
            LEFT JOIN Usuarios u ON e.corem = u.referencia_id
            WHERE e.corem = %s;
        """
        return self.db.fetch_one(query, params=(corem,))
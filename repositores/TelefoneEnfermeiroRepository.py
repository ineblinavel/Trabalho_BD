from database.Database import Database

class TelefoneEnfermeiroRepository:
    """
    Classe de repositório para gerenciar os telefones dos enfermeiros.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de telefones de enfermeiros.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def find_all(self) -> list:
        """
        Busca todos os telefones de enfermeiros cadastrados.

        Returns:
            list: Uma lista de dicionários, cada um representando um telefone.
        """
        query = "SELECT * FROM TelefoneEnfermeiro;"
        return self.db.fetch_all(query)

    def find_by(self, value: str, key: str = "id_telefone_enfermeiro") -> list | dict | None:
        """
        Busca telefones por um campo e valor específicos.

        Args:
            value (str): O valor a ser buscado.
            key (str): O campo pelo qual buscar (e.g., "id_telefone_enfermeiro", "corem_enfermeiro").

        Returns:
            list | dict | None: Um dicionário se a busca for por ID, uma lista para COREM,
                                 ou None se nada for encontrado.
        """
        possible_keys = ["id_telefone_enfermeiro", "corem_enfermeiro"]
        if key not in possible_keys:
            raise ValueError(f"Chave de busca inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM TelefoneEnfermeiro WHERE {key} = %s;"
        results = self.db.fetch_all(query, params=(value,))

        if key == "id_telefone_enfermeiro":
            return results[0] if results else None
        return results

    def create(self, corem_enfermeiro: str, numero_telefone: str) -> dict:
        """
        Adiciona um novo número de telefone para um enfermeiro.

        Args:
            corem_enfermeiro (str): COREM do enfermeiro.
            numero_telefone (str): O número de telefone a ser adicionado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "INSERT INTO TelefoneEnfermeiro (corem_enfermeiro, numero_telefone) VALUES (%s, %s);"
        params = (corem_enfermeiro, numero_telefone)
        self.db.execute_query(query, params=params)
        return {"message": "Telefone de enfermeiro adicionado com sucesso."}

    def update(self, id_telefone_enfermeiro: int, numero_telefone: str) -> dict:
        """
        Atualiza um número de telefone específico.

        Args:
            id_telefone_enfermeiro (int): ID do registro de telefone a ser atualizado.
            numero_telefone (str): O novo número de telefone.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "UPDATE TelefoneEnfermeiro SET numero_telefone = %s WHERE id_telefone_enfermeiro = %s;"
        params = (numero_telefone, id_telefone_enfermeiro)
        self.db.execute_query(query, params=params)
        return {"message": "Telefone de enfermeiro atualizado com sucesso."}

    def delete(self, id_telefone_enfermeiro: int) -> dict:
        """
        Deleta um telefone pelo seu ID de registro.

        Args:
            id_telefone_enfermeiro (int): ID do registro de telefone a ser deletado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM TelefoneEnfermeiro WHERE id_telefone_enfermeiro = %s;"
        self.db.execute_query(query, params=(id_telefone_enfermeiro,))
        return {"message": "Telefone de enfermeiro deletado com sucesso."}
    
    def delete_by_corem_and_phone(self, corem_enfermeiro: str, numero_telefone: str) -> dict:
        """
        Deleta um telefone específico de um enfermeiro.

        Args:
            corem_enfermeiro (str): COREM do enfermeiro.
            numero_telefone (str): Número de telefone a ser deletado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM TelefoneEnfermeiro WHERE corem_enfermeiro = %s AND numero_telefone = %s;"
        params = (corem_enfermeiro, numero_telefone)
        self.db.execute_query(query, params=params)
        return {"message": "Telefone específico do enfermeiro foi deletado."}
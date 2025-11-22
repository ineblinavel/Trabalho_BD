from database.Database import Database

class TelefoneMedicoRepository:
    """
    Classe de repositório para gerenciar os telefones dos médicos.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de telefones de médicos.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def find_all(self) -> list:
        """
        Busca todos os telefones de médicos cadastrados.

        Returns:
            list: Uma lista de dicionários, cada um representando um telefone.
        """
        query = "SELECT * FROM TelefoneMedico;"
        return self.db.fetch_all(query)

    def find_by(self, value: str, key: str = "id_telefone_medico") -> list | dict | None:
        """
        Busca telefones por um campo e valor específicos.

        Args:
            value (str): O valor a ser buscado.
            key (str): O campo pelo qual buscar (e.g., "id_telefone_medico", "crm_medico").

        Returns:
            list | dict | None: Um dicionário se a busca for por ID, uma lista para CRM,
                                 ou None se nada for encontrado.
        """
        possible_keys = ["id_telefone_medico", "crm_medico"]
        if key not in possible_keys:
            raise ValueError(f"Chave de busca inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM TelefoneMedico WHERE {key} = %s;"
        results = self.db.fetch_all(query, params=(value,))

        if key == "id_telefone_medico":
            return results[0] if results else None
        return results

    def create(self, crm_medico: str, numero_telefone: str) -> dict:
        """
        Adiciona um novo número de telefone para um médico.

        Args:
            crm_medico (str): CRM do médico.
            numero_telefone (str): O número de telefone a ser adicionado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "INSERT INTO TelefoneMedico (crm_medico, numero_telefone) VALUES (%s, %s);"
        params = (crm_medico, numero_telefone)
        self.db.execute_query(query, params=params)
        return {"message": "Telefone de médico adicionado com sucesso."}

    def update(self, id_telefone_medico: int, numero_telefone: str) -> dict:
        """
        Atualiza um número de telefone específico.

        Args:
            id_telefone_medico (int): ID do registro de telefone a ser atualizado.
            numero_telefone (str): O novo número de telefone.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "UPDATE TelefoneMedico SET numero_telefone = %s WHERE id_telefone_medico = %s;"
        params = (numero_telefone, id_telefone_medico)
        self.db.execute_query(query, params=params)
        return {"message": "Telefone de médico atualizado com sucesso."}

    def delete(self, id_telefone_medico: int) -> dict:
        """
        Deleta um telefone pelo seu ID de registro.

        Args:
            id_telefone_medico (int): ID do registro de telefone a ser deletado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM TelefoneMedico WHERE id_telefone_medico = %s;"
        self.db.execute_query(query, params=(id_telefone_medico,))
        return {"message": "Telefone de médico deletado com sucesso."}
    
    def delete_by_crm_and_phone(self, crm_medico: str, numero_telefone: str) -> dict:
        """
        Deleta um telefone específico de um médico.

        Args:
            crm_medico (str): CRM do médico.
            numero_telefone (str): Número de telefone a ser deletado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM TelefoneMedico WHERE crm_medico = %s AND numero_telefone = %s;"
        params = (crm_medico, numero_telefone)
        self.db.execute_query(query, params=params)
        return {"message": "Telefone específico do médico foi deletado."}
from database.Database import Database

class TelefonePacienteRepository:
    """
    Classe de repositório para gerenciar os telefones dos pacientes.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de telefones de pacientes.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def find_all(self) -> list:
        """
        Busca todos os telefones de pacientes cadastrados.

        Returns:
            list: Uma lista de dicionários, cada um representando um telefone.
        """
        query = "SELECT * FROM TelefonePaciente;"
        return self.db.fetch_all(query)

    def find_by(self, value: int, key: str = "id_telefone_paciente") -> list | dict | None:
        """
        Busca telefones por um campo e valor específicos.

        Args:
            value (int): O valor a ser buscado.
            key (str): O campo pelo qual buscar (e.g., "id_telefone_paciente", "id_paciente").

        Returns:
            list | dict | None: Um dicionário se a busca for por ID do telefone, uma
                                 lista para ID do paciente, ou None se nada for encontrado.
        """
        possible_keys = ["id_telefone_paciente", "id_paciente"]
        if key not in possible_keys:
            raise ValueError(f"Chave de busca inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM TelefonePaciente WHERE {key} = %s;"
        results = self.db.fetch_all(query, params=(value,))

        if key == "id_telefone_paciente":
            return results[0] if results else None
        return results

    def create(self, id_paciente: int, numero_telefone: str) -> dict:
        """
        Adiciona um novo número de telefone para um paciente.

        Args:
            id_paciente (int): ID do paciente.
            numero_telefone (str): O número de telefone a ser adicionado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "INSERT INTO TelefonePaciente (id_paciente, numero_telefone) VALUES (%s, %s);"
        params = (id_paciente, numero_telefone)
        self.db.execute_query(query, params=params)
        return {"message": "Telefone de paciente adicionado com sucesso."}

    def update(self, id_telefone_paciente: int, numero_telefone: str) -> dict:
        """
        Atualiza um número de telefone específico.

        Args:
            id_telefone_paciente (int): ID do registro de telefone a ser atualizado.
            numero_telefone (str): O novo número de telefone.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "UPDATE TelefonePaciente SET numero_telefone = %s WHERE id_telefone_paciente = %s;"
        params = (numero_telefone, id_telefone_paciente)
        self.db.execute_query(query, params=params)
        return {"message": "Telefone de paciente atualizado com sucesso."}

    def delete(self, id_telefone_paciente: int) -> dict:
        """
        Deleta um telefone pelo seu ID de registro.

        Args:
            id_telefone_paciente (int): ID do registro de telefone a ser deletado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM TelefonePaciente WHERE id_telefone_paciente = %s;"
        self.db.execute_query(query, params=(id_telefone_paciente,))
        return {"message": "Telefone de paciente deletado com sucesso."}
    
    def delete_by_patient_and_phone(self, id_paciente: int, numero_telefone: str) -> dict:
        """
        Deleta um telefone específico de um paciente.

        Args:
            id_paciente (int): ID do paciente.
            numero_telefone (str): Número de telefone a ser deletado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM TelefonePaciente WHERE id_paciente = %s AND numero_telefone = %s;"
        params = (id_paciente, numero_telefone)
        self.db.execute_query(query, params=params)
        return {"message": "Telefone específico do paciente foi deletado."}
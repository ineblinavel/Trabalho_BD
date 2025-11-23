from database.Database import Database

class PacienteRepository:
    """
    Classe de repositório para gerenciar as operações de persistência
    de dados dos pacientes.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de pacientes.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def get_historico_completo(self, id_paciente: int) -> list:
        """
        Busca o histórico clínico completo de um paciente a partir da view V_HistoricoClinico.

        O histórico inclui consultas, internações, procedimentos e exames.

        Args:
            id_paciente (int): O ID do paciente para o qual o histórico será buscado.

        Returns:
            list: Uma lista de dicionários, onde cada dicionário representa um
                  evento no histórico do paciente, ordenado pela data do evento.
        """
        query = "SELECT * FROM V_HistoricoClinico WHERE id_paciente = %s ORDER BY data_evento DESC"
        params = (id_paciente,)
        return self.db.fetch_all(query, params)

    def update_foto(self, id_paciente: int, foto_data: bytes) -> dict:
        """
        Atualiza a foto de um paciente no banco de dados.

        Args:
            id_paciente (int): O ID do paciente a ter a foto atualizada.
            foto_data (bytes): Os dados binários da imagem (foto).

        Returns:
            dict: Um dicionário com a mensagem de resultado da operação.
        """
        query = "UPDATE Paciente SET foto = %s WHERE id_paciente = %s"
        params = (foto_data, id_paciente)
        self.db.execute_query(query, params)
        return {"message": "Foto do paciente atualizada com sucesso."}

    def get_foto(self, id_paciente: int) -> bytes:
        """
        Recupera a foto de um paciente do banco de dados.

        Args:
            id_paciente (int): O ID do paciente cuja foto será recuperada.

        Returns:
            bytes: Os dados binários da imagem (foto) ou None se não houver foto.
        """
        query = "SELECT foto FROM Paciente WHERE id_paciente = %s"
        params = (id_paciente,)
        result = self.db.fetch_one(query, params)
        return result['foto'] if result and result['foto'] else None

    def get_all(self) -> list:
        """
        Busca todos os pacientes cadastrados.

        Returns:
            list: Uma lista de dicionários, cada um representando um paciente.
        """
        query = "SELECT id_paciente, nome_paciente, cpf, data_nascimento, endereco FROM Paciente"
        return self.db.fetch_all(query)

    def get_by_id(self, id_paciente: int) -> dict:
        """
        Busca um paciente específico pelo seu ID.

        Args:
            id_paciente (int): O ID do paciente a ser buscado.

        Returns:
            dict: Um dicionário com os dados do paciente ou None se não encontrado.
                  A foto não é incluída nesta busca por performance.
        """
        query = "SELECT id_paciente, nome_paciente, cpf, data_nascimento, endereco FROM Paciente WHERE id_paciente = %s"
        params = (id_paciente,)
        return self.db.fetch_one(query, params)

    def create(self, nome: str, cpf: str, data_nascimento: str, endereco: str) -> dict:
        """
        Cria um novo paciente no banco de dados.

        Args:
            nome (str): Nome completo do paciente.
            cpf (str): CPF do paciente.
            data_nascimento (str): Data de nascimento no formato 'YYYY-MM-DD'.
            endereco (str): Endereço do paciente.

        Returns:
            dict: Um dicionário contendo o ID do paciente inserido.
        """
        query = "INSERT INTO Paciente (nome_paciente, cpf, data_nascimento, endereco) VALUES (%s, %s, %s, %s)"
        params = (nome, cpf, data_nascimento, endereco)
        last_id = self.db.execute_query(query, params, fetch_last_id=True)
        return {"id_paciente": last_id}
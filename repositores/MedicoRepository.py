from database.Database import Database

class MedicoRepository:
    """
    Classe de repositório para gerenciar as operações de persistência
    de dados dos médicos.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de médicos.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def find_all(self, include_inactive: bool = False) -> list:
        """
        Busca todos os médicos cadastrados. Por padrão, busca apenas médicos ativos.

        Args:
            include_inactive (bool): Se True, inclui médicos inativos na busca.

        Returns:
            list: Uma lista de dicionários, cada um representando um médico.
        """
        query = "SELECT * FROM Medicos"
        if not include_inactive:
            query += " WHERE ativo = TRUE"
        return self.db.fetch_all(query)

    def find_by(self, value: str, key: str = "crm", active_only: bool = True) -> list | dict | None:
        """
        Busca médicos por um campo e valor específicos.

        Args:
            value (str): O valor a ser buscado.
            key (str): O campo pelo qual buscar (e.g., "crm", "cpf", "nome_medico").
            active_only (bool): Se True, busca apenas entre os médicos ativos.

        Returns:
            list | dict | None: Um dicionário se a busca for por 'crm' ou 'cpf', uma
                                 lista para 'nome_medico', ou None se nada for encontrado.
        """
        possible_keys = ["crm", "nome_medico", "cpf"]
        if key not in possible_keys:
            raise ValueError(f"Chave de busca inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM Medicos WHERE {key} = %s"
        params = [value]
        
        if active_only:
            query += " AND ativo = TRUE"

        results = self.db.fetch_all(query, params=tuple(params))
        
        if key in ["crm", "cpf"]:
            return results[0] if results else None
        return results
    
    def create(self, crm: str, nome_medico: str, cpf: str, salario: float) -> dict:
        """
        Cria um novo registro de médico, definindo-o como ativo.

        Args:
            crm (str): CRM do médico (identificador único).
            nome_medico (str): Nome completo do médico.
            cpf (str): CPF do médico.
            salario (float): Salário do médico.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "INSERT INTO Medicos (crm, nome_medico, cpf, salario, ativo) VALUES (%s, %s, %s, %s, TRUE);"
        params = (crm, nome_medico, cpf, salario)
        self.db.execute_query(query, params=params)
        return {"message": "Médico criado com sucesso."}

    def update(self, crm: str, **kwargs) -> dict:
        """
        Atualiza os dados de um médico existente.

        Args:
            crm (str): O CRM do médico a ser atualizado.
            **kwargs: Campos a serem atualizados (e.g., salario=20000.00).

        Returns:
            dict: Dicionário com mensagem de sucesso ou aviso.
        """
        fields = []
        params = []
        
        for key, value in kwargs.items():
            if key in ["nome_medico", "cpf", "salario"]:
                fields.append(f"{key} = %s")
                params.append(value)
        
        if not fields:
            return {"message": "Nenhum dado fornecido para atualização."}
        
        params.append(crm)
        query = f"UPDATE Medicos SET {', '.join(fields)} WHERE crm = %s;"
        self.db.execute_query(query, params=tuple(params))
        return {"message": "Médico atualizado com sucesso."}
    
    def find_by_crm_with_phones(self, crm: str) -> dict | None:
        """
        Busca um médico pelo CRM e agrega seus telefones em uma lista.
        Também busca a senha do usuário associado.

        Args:
            crm (str): O CRM do médico a ser buscado.

        Returns:
            dict | None: Dicionário com os dados do médico e uma lista de telefones,
                         ou None se não for encontrado.
        """
        query = """
            SELECT m.*, u.password, GROUP_CONCAT(tm.numero_telefone) as telefones
            FROM Medicos m
            LEFT JOIN TelefoneMedico tm ON m.crm = tm.crm_medico
            LEFT JOIN Usuarios u ON m.crm = u.referencia_id
            WHERE m.crm = %s
            GROUP BY m.crm, u.password;
        """
        result = self.db.fetch_one(query, params=(crm,))
        if result and result.get('telefones'):
            result['telefones'] = result['telefones'].split(',')
        elif result:
            result['telefones'] = []
            
        return result

    def deactivate(self, crm: str) -> dict:
        """
        Desativa um médico (soft delete) pelo seu CRM.

        Args:
            crm (str): O CRM do médico a ser desativado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "UPDATE Medicos SET ativo = FALSE WHERE crm = %s AND ativo = TRUE;"
        self.db.execute_query(query, params=(crm,))
        return {"message": f"Médico com CRM {crm} desativado."}
    
    def reactivate(self, crm: str) -> dict:
        """
        Reativa um médico previamente desativado.

        Args:
            crm (str): O CRM do médico a ser reativado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "UPDATE Medicos SET ativo = TRUE WHERE crm = %s AND ativo = FALSE;"
        self.db.execute_query(query, params=(crm,))
        return {"message": f"Médico com CRM {crm} reativado."}

    def find_by_salary_range(self, min_salary: float = 0, max_salary: float = 1000000) -> list:
        """
        Busca médicos ativos com salário dentro de um intervalo específico.

        Args:
            min_salary (float): O piso salarial do intervalo.
            max_salary (float): O teto salarial do intervalo.

        Returns:
            list: Lista de médicos encontrados.
        """
        query = "SELECT * FROM Medicos WHERE salario BETWEEN %s AND %s AND ativo = TRUE;"
        return self.db.fetch_all(query, params=(min_salary, max_salary))

    def delete(self, crm: str) -> dict:
        """
        Remove um médico do banco de dados.

        Args:
            crm (str): O CRM do médico a ser removido.

        Returns:
            dict: Um dicionário com a mensagem de resultado da operação.
        """
        query = "DELETE FROM Medicos WHERE crm = %s"
        params = (crm,)
        self.db.execute_query(query, params)
        return {"message": "Médico removido com sucesso."}

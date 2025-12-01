from database.Database import Database
from datetime import datetime

class ResultadoExameRepository:
    """
    Classe de repositório para gerenciar os resultados dos exames.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de resultados de exames.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def find_all(self) -> list:
        """
        Busca todos os resultados de exames cadastrados.

        Returns:
            list: Uma lista de dicionários, cada um representando um resultado.
        """
        query = "SELECT * FROM ResultadoExame;"
        return self.db.fetch_all(query)

    def find_by(self, value: int, key: str = "id_resultado_exame") -> list | dict | None:
        """
        Busca resultados de exame por um campo e valor específicos.

        Args:
            value (int): O valor a ser buscado.
            key (str): O campo pelo qual buscar (e.g., "id_resultado_exame", "id_exame").

        Returns:
            list | dict | None: Um dicionário se a busca for por 'id_resultado_exame',
                                 uma lista se for por 'id_exame', ou None se nada for encontrado.
        """
        possible_keys = ["id_resultado_exame", "id_exame"]
        if key not in possible_keys:
            raise ValueError(f"Chave de busca inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM ResultadoExame WHERE {key} = %s;"
        results = self.db.fetch_all(query, params=(value,))

        if key == "id_resultado_exame":
            return results[0] if results else None
        return results

    def create(self, id_exame: int, resultado_obtido: str, data_resultado: str) -> dict:
        """
        Cria um novo resultado de exame chamando a Stored Procedure SP_RegistrarResultadoExame.

        Args:
            id_exame (int): ID do exame associado.
            resultado_obtido (str): O texto com o resultado do exame.
            data_resultado (str): Data em que o resultado foi emitido ('YYYY-MM-DD').

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        self._validate_date(data_resultado)
        
        # Chama a Procedure que faz o INSERT e o UPDATE do status
        query = "CALL SP_RegistrarResultadoExame(%s, %s, %s);"
        params = (id_exame, resultado_obtido, data_resultado)
        self.db.execute_query(query, params=params)
        
        return {"message": "Resultado de exame registrado com sucesso."}

    def update(self, id_resultado_exame: int, **kwargs) -> dict:
        """
        Atualiza os dados de um resultado de exame.

        Args:
            id_resultado_exame (int): O ID do resultado a ser atualizado.
            **kwargs: Campos a serem atualizados (e.g., resultado_obtido="...").

        Returns:
            dict: Dicionário com mensagem de sucesso ou aviso.
        """
        fields = []
        params = []
        
        for key, value in kwargs.items():
            if key in ["resultado_obtido", "data_resultado", "id_exame"]:
                if key == "data_resultado" and value:
                    self._validate_date(value)
                fields.append(f"{key} = %s")
                params.append(value)

        if not fields:
            return {"message": "Nenhum dado fornecido para atualização."}
        
        params.append(id_resultado_exame)
        query = f"UPDATE ResultadoExame SET {', '.join(fields)} WHERE id_resultado_exame = %s;"
        self.db.execute_query(query, params=tuple(params))
        return {"message": "Resultado de exame atualizado com sucesso."}

    def delete(self, id_resultado_exame: int) -> dict:
        """
        Deleta um resultado de exame pelo seu ID.

        Args:
            id_resultado_exame (int): O ID do resultado a ser deletado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM ResultadoExame WHERE id_resultado_exame = %s;"
        self.db.execute_query(query, params=(id_resultado_exame,))
        return {"message": "Resultado de exame deletado com sucesso."}

    def _validate_date(self, date_string: str):
        """Valida o formato de uma string de data."""
        try:
            if date_string:
                datetime.strptime(date_string, '%Y-%m-%d')
        except (ValueError, TypeError):
            raise ValueError(f"Formato de data inválido: '{date_string}'. Use 'YYYY-MM-DD'.")
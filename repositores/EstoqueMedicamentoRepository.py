from database.Database import Database
from datetime import datetime

class EstoqueMedicamentoRepository:
    """
    Classe de repositório para gerenciar o estoque de medicamentos.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de estoque de medicamentos.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def find_all(self) -> list:
        """
        Busca todos os itens no estoque de medicamentos.

        Returns:
            list: Uma lista de dicionários, cada um representando um item do estoque.
        """
        query = "SELECT * FROM EstoqueMedicamento;"
        return self.db.fetch_all(query)

    def find_by(self, value, key: str = "id_estoque_medicamento") -> list | dict | None:
        """
        Busca itens no estoque por um campo e valor específicos.

        Args:
            value: O valor a ser buscado.
            key (str): O campo pelo qual buscar (e.g., "id_estoque_medicamento", "id_medicamento").

        Returns:
            list | dict | None: Um dicionário se a busca for por 'id_estoque_medicamento',
                                 uma lista para outras chaves, ou None se nada for encontrado.
        """
        possible_keys = ["id_estoque_medicamento", "id_medicamento", "cnpj_fornecedor"]
        if key not in possible_keys:
            raise ValueError(f"Chave de busca inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM EstoqueMedicamento WHERE {key} = %s;"
        results = self.db.fetch_all(query, params=(value,))

        if key == "id_estoque_medicamento":
            return results[0] if results else None
        return results

    def create(self, data_validade: str, preco_unitario: float, quantidade: int, id_medicamento: int, cnpj_fornecedor: str) -> dict:
        """
        Adiciona um novo lote de medicamento ao estoque.

        Args:
            data_validade (str): Data de validade do lote ('YYYY-MM-DD').
            preco_unitario (float): Preço por unidade do medicamento.
            quantidade (int): Quantidade de unidades no lote.
            id_medicamento (int): ID do medicamento.
            cnpj_fornecedor (str): CNPJ do fornecedor.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        self._validate_date(data_validade)
        query = """
        INSERT INTO EstoqueMedicamento (data_validade, preco_unitario, quantidade, id_medicamento, cnpj_fornecedor)
        VALUES (%s, %s, %s, %s, %s);
        """
        params = (data_validade, preco_unitario, quantidade, id_medicamento, cnpj_fornecedor)
        self.db.execute_query(query, params=params)
        return {"message": "Item adicionado ao estoque com sucesso."}

    def update(self, id_estoque_medicamento: int, **kwargs) -> dict:
        """
        Atualiza informações de um item no estoque.

        Args:
            id_estoque_medicamento (int): ID do item de estoque a ser atualizado.
            **kwargs: Campos a serem atualizados (e.g., quantidade=100).

        Returns:
            dict: Dicionário com mensagem de sucesso ou aviso.
        """
        fields = []
        params = []
        
        for key, value in kwargs.items():
            if key in ["data_validade", "preco_unitario", "quantidade", "id_medicamento", "cnpj_fornecedor"]:
                if key == "data_validade" and value:
                    self._validate_date(value)
                fields.append(f"{key} = %s")
                params.append(value)

        if not fields:
            return {"message": "Nenhum dado fornecido para atualização."}
        
        params.append(id_estoque_medicamento)
        query = f"UPDATE EstoqueMedicamento SET {', '.join(fields)} WHERE id_estoque_medicamento = %s;"
        self.db.execute_query(query, params=tuple(params))
        return {"message": "Item de estoque atualizado com sucesso."}

    def find_expired(self) -> list:
        """
        Encontra todos os itens no estoque que já passaram da data de validade.

        Returns:
            list: Lista de itens vencidos no estoque.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        query = "SELECT * FROM EstoqueMedicamento WHERE data_validade < %s;"
        return self.db.fetch_all(query, params=(today,))

    def find_low_stock(self, threshold: int = 10) -> list:
        """
        Encontra todos os itens no estoque com quantidade abaixo de um limite.

        Args:
            threshold (int): O limite de quantidade para considerar como estoque baixo.

        Returns:
            list: Lista de itens com estoque baixo.
        """
        query = "SELECT * FROM EstoqueMedicamento WHERE quantidade < %s;"
        return self.db.fetch_all(query, params=(threshold,))

    def delete(self, id_estoque_medicamento: int) -> dict:
        """
        Deleta um item do estoque pelo seu ID.

        Args:
            id_estoque_medicamento (int): ID do item a ser deletado.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM EstoqueMedicamento WHERE id_estoque_medicamento = %s;"
        self.db.execute_query(query, params=(id_estoque_medicamento,))
        return {"message": "Item de estoque deletado com sucesso."}

    def _validate_date(self, date_string: str):
        """Valida o formato de uma string de data."""
        try:
            if date_string:
                datetime.strptime(date_string, '%Y-%m-%d')
        except (ValueError, TypeError):
            raise ValueError(f"Formato de data inválido: '{date_string}'. Use 'YYYY-MM-DD'.")
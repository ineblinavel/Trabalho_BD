from database.Database import Database

class RelatoriosRepository:
    """
    Classe de repositório para gerar relatórios complexos a partir
    de views e agregações no banco de dados.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório de relatórios.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def get_faturamento_mensal(self, ano: int = None, mes: int = None) -> list:
        """
        Busca os dados de faturamento mensal a partir da view V_FaturamentoMensal.
        
        O faturamento é agrupado por ano, mês e tipo (Consulta, Internação, etc.).

        Args:
            ano (int, optional): Filtra o resultado por um ano específico.
            mes (int, optional): Filtra o resultado por um mês específico. 
                                 Requer que o 'ano' também seja fornecido.

        Returns:
            list: Uma lista de dicionários, onde cada dicionário representa uma
                  linha de faturamento agregado.
        """
        query = "SELECT ano, mes, tipo, total FROM V_FaturamentoMensal"
        params = []
        conditions = []

        if ano:
            conditions.append("ano = %s")
            params.append(ano)
        
        if ano and mes:
            conditions.append("mes = %s")
            params.append(mes)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        query += " ORDER BY ano, mes, tipo"

        return self.db.fetch_all(query, tuple(params))

    
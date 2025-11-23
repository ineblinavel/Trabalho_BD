from repositores.RelatoriosRepository import RelatoriosRepository

class RelatoriosService:
    def __init__(self, repo: RelatoriosRepository):
        self.repo = repo

    def get_faturamento(self, ano: int = None, mes: int = None):
        if mes is not None:
            if not (1 <= mes <= 12):
                raise ValueError("O mês deve estar entre 1 e 12.")
            
            if ano is None:
                raise ValueError("Para filtrar por mês, é necessário informar o ano.")

        return self.repo.get_faturamento_mensal(ano, mes)
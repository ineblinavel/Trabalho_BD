from repositores.RelatoriosRepository import RelatoriosRepository

class RelatoriosService:
    def __init__(self, repo: RelatoriosRepository):
        self.repo = repo

    def get_faturamento(self, ano: int = None, mes: int = None):
        return self.repo.get_faturamento_mensal(ano, mes)
from repositores.TipoExameRepository import TipoExameRepository

class TipoExameService:
    def __init__(self, repo: TipoExameRepository):
        self.repo = repo

    def get_all(self):
        return self.repo.find_all()

    def get_by_id(self, id_tipo: int):
        return self.repo.find_by(id_tipo, key="id_tipo_exame")

    def create(self, nome: str, preco: float, descricao: str = None):
        return self.repo.create(nome, preco, descricao)

    def update(self, id_tipo: int, data: dict):
        return self.repo.update(id_tipo, **data)

    def delete(self, id_tipo: int):
        return self.repo.delete(id_tipo)
from repositores.TelefoneEnfermeiroRepository import TelefoneEnfermeiroRepository

class TelefoneEnfermeiroService:
    def __init__(self, repo: TelefoneEnfermeiroRepository):
        self.repo = repo

    def get_all(self):
        return self.repo.find_all()

    def get_by_corem(self, corem: str):
        return self.repo.find_by(corem, key="corem_enfermeiro")

    def get_by_id(self, id_telefone: int):
        return self.repo.find_by(id_telefone, key="id_telefone_enfermeiro")

    def create(self, corem_enfermeiro: str, numero_telefone: str):
        return self.repo.create(corem_enfermeiro, numero_telefone)

    def update(self, id_telefone: int, numero_telefone: str):
        return self.repo.update(id_telefone, numero_telefone)

    def delete(self, id_telefone: int):
        return self.repo.delete(id_telefone)
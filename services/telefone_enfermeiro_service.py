from repositores.TelefoneEnfermeiroRepository import TelefoneEnfermeiroRepository
from repositores.EnfermeiroRepository import EnfermeiroRepository

class TelefoneEnfermeiroService:
    def __init__(self, repo: TelefoneEnfermeiroRepository, enfermeiro_repo: EnfermeiroRepository):
        self.repo = repo
        self.enfermeiro_repo = enfermeiro_repo

    def get_all(self):
        return self.repo.find_all()

    def get_by_corem(self, corem: str):
        return self.repo.find_by(corem, key="corem_enfermeiro")

    def get_by_id(self, id_telefone: int):
        return self.repo.find_by(id_telefone, key="id_telefone_enfermeiro")

    def create(self, corem_enfermeiro: str, numero_telefone: str):
        enfermeiro = self.enfermeiro_repo.find_by(corem_enfermeiro, key="corem")
        if not enfermeiro:
            raise ValueError(f"Enfermeiro com COREM {corem_enfermeiro} não encontrado.")

        return self.repo.create(corem_enfermeiro, numero_telefone)

    def update(self, id_telefone: int, numero_telefone: str):
        if not self.repo.find_by(id_telefone, key="id_telefone_enfermeiro"):
             raise ValueError(f"Registro de telefone {id_telefone} não encontrado.")
             
        return self.repo.update(id_telefone, numero_telefone)

    def delete(self, id_telefone: int):
        return self.repo.delete(id_telefone)

    def delete_specific(self, corem: str, numero: str):
        return self.repo.delete_by_corem_and_phone(corem, numero)
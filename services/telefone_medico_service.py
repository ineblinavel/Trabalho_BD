from repositores.TelefoneMedicoRepository import TelefoneMedicoRepository
from repositores.MedicoRepository import MedicoRepository

class TelefoneMedicoService:
    def __init__(self, repo: TelefoneMedicoRepository, medico_repo: MedicoRepository):
        self.repo = repo
        self.medico_repo = medico_repo

    def get_all(self):
        return self.repo.find_all()

    def get_by_crm(self, crm: str):
        return self.repo.find_by(crm, key="crm_medico")

    def get_by_id(self, id_telefone: int):
        return self.repo.find_by(id_telefone, key="id_telefone_medico")

    def create(self, crm_medico: str, numero_telefone: str):
        medico = self.medico_repo.find_by(crm_medico, key="crm")
        if not medico:
            raise ValueError(f"Médico com CRM {crm_medico} não encontrado.")

        return self.repo.create(crm_medico, numero_telefone)

    def update(self, id_telefone: int, numero_telefone: str):
        if not self.repo.find_by(id_telefone, key="id_telefone_medico"):
             raise ValueError(f"Registro de telefone {id_telefone} não encontrado.")
             
        return self.repo.update(id_telefone, numero_telefone)

    def delete(self, id_telefone: int):
        return self.repo.delete(id_telefone)

    def delete_specific(self, crm: str, numero: str):
        return self.repo.delete_by_crm_and_phone(crm, numero)
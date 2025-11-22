from repositores.MedicoRepository import MedicoRepository

class MedicoService:
    def __init__(self, medico_repo: MedicoRepository):
        self.medico_repo = medico_repo

    def create_medico(self, crm: str, nome_medico: str, cpf: str, salario: float):
        # Business logic, like validation, could be added here in the future.
        return self.medico_repo.create(crm, nome_medico, cpf, salario)

    def get_all_medicos(self):
        return self.medico_repo.find_all()

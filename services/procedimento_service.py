from repositores.ProcedimentoRepository import ProcedimentoRepository

class ProcedimentoService:
    def __init__(self, repo: ProcedimentoRepository):
        self.repo = repo

    def get_all(self):
        return self.repo.find_all()

    def get_by_id(self, id_procedimento: int):
        return self.repo.find_by(id_procedimento, key="id_procedimento")

    def create(self, crm_medico: str, id_paciente: int, nome_procedimento: str, custo: float):
        return self.repo.create(crm_medico, id_paciente, nome_procedimento, custo)

    def update(self, id_procedimento: int, data: dict):
        update_data = {k: v for k, v in data.items() if v is not None}
        return self.repo.update(id_procedimento, **update_data)

    def delete(self, id_procedimento: int):
        return self.repo.delete(id_procedimento)
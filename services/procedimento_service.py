from repositores.ProcedimentoRepository import ProcedimentoRepository
from repositores.MedicoRepository import MedicoRepository
from repositores.PacienteRepository import PacienteRepository

class ProcedimentoService:
    def __init__(self, repo: ProcedimentoRepository, medico_repo: MedicoRepository, paciente_repo: PacienteRepository):
        self.repo = repo
        self.medico_repo = medico_repo
        self.paciente_repo = paciente_repo

    def get_all(self):
        return self.repo.find_all()

    def get_by_id(self, id_procedimento: int):
        return self.repo.find_by(id_procedimento, key="id_procedimento")

    def create(self, crm_medico: str, id_paciente: int, nome_procedimento: str, custo: float):
        if custo < 0:
            raise ValueError("O custo do procedimento não pode ser negativo.")
        
        medico = self.medico_repo.find_by(crm_medico, key="crm")
        if not medico:
            raise ValueError(f"Médico com CRM {crm_medico} não encontrado.")

        paciente = self.paciente_repo.get_by_id(id_paciente)
        if not paciente:
             raise ValueError(f"Paciente com ID {id_paciente} não encontrado.")

        return self.repo.create(crm_medico, id_paciente, nome_procedimento, custo)

    def update(self, id_procedimento: int, data: dict):
        update_data = {k: v for k, v in data.items() if v is not None}
        
        if 'custo' in update_data:
            try:
                custo = float(update_data['custo'])
                if custo < 0:
                    raise ValueError("O custo do procedimento não pode ser negativo.")
            except ValueError:
                 raise ValueError("O valor do custo é inválido.")

        return self.repo.update(id_procedimento, **update_data)

    def delete(self, id_procedimento: int):
        return self.repo.delete(id_procedimento)
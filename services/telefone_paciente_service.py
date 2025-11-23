from repositores.TelefonePacienteRepository import TelefonePacienteRepository
from repositores.PacienteRepository import PacienteRepository

class TelefonePacienteService:
    def __init__(self, repo: TelefonePacienteRepository, paciente_repo: PacienteRepository):
        self.repo = repo
        self.paciente_repo = paciente_repo

    def get_all(self):
        return self.repo.find_all()

    def get_by_paciente(self, id_paciente: int):
        return self.repo.find_by(id_paciente, key="id_paciente")

    def get_by_id(self, id_telefone: int):
        return self.repo.find_by(id_telefone, key="id_telefone_paciente")

    def create(self, id_paciente: int, numero_telefone: str):
        paciente = self.paciente_repo.get_by_id(id_paciente)
        if not paciente:
            raise ValueError(f"Paciente com ID {id_paciente} não encontrado.")

        return self.repo.create(id_paciente, numero_telefone)

    def update(self, id_telefone: int, numero_telefone: str):
        if not self.repo.find_by(id_telefone, key="id_telefone_paciente"):
             raise ValueError(f"Registro de telefone {id_telefone} não encontrado.")
             
        return self.repo.update(id_telefone, numero_telefone)

    def delete(self, id_telefone: int):
        return self.repo.delete(id_telefone)

    def delete_specific(self, id_paciente: int, numero: str):
        return self.repo.delete_by_patient_and_phone(id_paciente, numero)
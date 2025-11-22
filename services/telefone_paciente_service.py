from repositores.TelefonePacienteRepository import TelefonePacienteRepository

class TelefonePacienteService:
    def __init__(self, repo: TelefonePacienteRepository):
        self.repo = repo

    def get_all(self):
        return self.repo.find_all()

    def get_by_paciente(self, id_paciente: int):
        return self.repo.find_by(id_paciente, key="id_paciente")

    def get_by_id(self, id_telefone: int):
        return self.repo.find_by(id_telefone, key="id_telefone_paciente")

    def create(self, id_paciente: int, numero_telefone: str):
        return self.repo.create(id_paciente, numero_telefone)

    def update(self, id_telefone: int, numero_telefone: str):
        return self.repo.update(id_telefone, numero_telefone)

    def delete(self, id_telefone: int):
        return self.repo.delete(id_telefone)
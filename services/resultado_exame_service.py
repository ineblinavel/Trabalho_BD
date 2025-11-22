from repositores.ResultadoExameRepository import ResultadoExameRepository

class ResultadoExameService:
    def __init__(self, repo: ResultadoExameRepository):
        self.repo = repo

    def get_all(self):
        return self.repo.find_all()

    def get_by_exame(self, id_exame: int):
        return self.repo.find_by(id_exame, key="id_exame")

    def create(self, id_exame: int, resultado: str, data_resultado: str):
        # Chama a procedure SP_RegistrarResultadoExame via repositorio
        return self.repo.create(id_exame, resultado, data_resultado)

    def update(self, id_resultado: int, data: dict):
        return self.repo.update(id_resultado, **data)
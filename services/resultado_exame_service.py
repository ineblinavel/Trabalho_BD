from repositores.ResultadoExameRepository import ResultadoExameRepository
from repositores.ExameRepository import ExameRepository

class ResultadoExameService:
    def __init__(self, repo: ResultadoExameRepository, exame_repo: ExameRepository):
        self.repo = repo
        self.exame_repo = exame_repo

    def get_all(self):
        return self.repo.find_all()

    def get_by_exame(self, id_exame: int):
        return self.repo.find_by(id_exame, key="id_exame")

    def create(self, id_exame: int, resultado: str, data_resultado: str):
        if not resultado or not resultado.strip():
            raise ValueError("O texto do resultado do exame é obrigatório.")

        exame = self.exame_repo.find_by(id_exame, key="id_exame")
        if not exame:
            raise ValueError(f"Exame com ID {id_exame} não encontrado.")

        resultados_existentes = self.repo.find_by(id_exame, key="id_exame")
        if resultados_existentes:
            raise ValueError(f"O exame {id_exame} já possui um resultado registrado.")

        return self.repo.create(id_exame, resultado, data_resultado)

    def update(self, id_resultado_exame: int, data: dict):
        if not self.repo.find_by(id_resultado_exame, key="id_resultado_exame"):
            raise ValueError(f"Resultado de exame {id_resultado_exame} não encontrado.")

        update_data = {k: v for k, v in data.items() if v is not None}
        return self.repo.update(id_resultado_exame, **update_data)

    def delete(self, id_resultado_exame: int):
        return self.repo.delete(id_resultado_exame)
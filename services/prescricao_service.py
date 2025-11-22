from repositores.PrescricaoRepository import PrescricaoRepository

class PrescricaoService:
    def __init__(self, prescricao_repo: PrescricaoRepository):
        self.prescricao_repo = prescricao_repo

    def get_all_prescricoes(self):
        return self.prescricao_repo.find_all()

    def get_prescricao_by_id(self, id_prescricao: int):
        return self.prescricao_repo.find_by(id_prescricao, key="id_prescricao")

    def get_prescricoes_by_consulta(self, id_consulta: int):
        return self.prescricao_repo.find_by(id_consulta, key="id_consulta")

    def create_prescricao(self, id_consulta: int, id_medicamento: int, quantidade: int, dosagem: str, frequencia: str):
        # Validações de negócio podem ser adicionadas aqui
        return self.prescricao_repo.create(
            id_consulta=id_consulta,
            id_medicamento=id_medicamento,
            quantidade_prescrita=quantidade,
            dosagem=dosagem,
            frequencia_uso=frequencia
        )

    def update_prescricao(self, id_prescricao: int, data: dict):
        # Remove chaves nulas ou vazias para não sobrescrever erradamente
        update_data = {k: v for k, v in data.items() if v is not None}
        return self.prescricao_repo.update(id_prescricao, **update_data)

    def delete_prescricao(self, id_prescricao: int):
        return self.prescricao_repo.delete(id_prescricao)
from repositores.PrescricaoRepository import PrescricaoRepository
from repositores.ConsultasRepository import ConsultasRepository
from repositores.MedicamentoRepository import MedicamentoRepository
from services.estoquemedicamento_service import EstoqueMedicamentoService

class PrescricaoService:
    def __init__(self,
                 prescricao_repo: PrescricaoRepository,
                 consulta_repo: ConsultasRepository,
                 medicamento_repo: MedicamentoRepository,
                 estoque_service: EstoqueMedicamentoService):
        self.prescricao_repo = prescricao_repo
        self.consulta_repo = consulta_repo
        self.medicamento_repo = medicamento_repo
        self.estoque_service = estoque_service

    def get_all_prescricoes(self):
        return self.prescricao_repo.find_all()

    def get_prescricao_by_id(self, id_prescricao: int):
        return self.prescricao_repo.find_by(id_prescricao, key="id_prescricao")

    def get_prescricoes_by_consulta(self, id_consulta: int):
        return self.prescricao_repo.find_by(id_consulta, key="id_consulta")

    def create_prescricao(self, id_consulta: int, id_medicamento: int, quantidade: int, dosagem: str, frequencia: str):

        # Quantidade deve ser positiva
        if quantidade <= 0:
            raise ValueError("A quantidade prescrita deve ser maior que zero.")

        # Verificar se a Consulta existe
        consulta = self.consulta_repo.get_by_id(id_consulta)
        if not consulta:
            raise ValueError(f"Consulta com ID {id_consulta} não encontrada.")

        # Verificar se o Medicamento existe
        medicamento = self.medicamento_repo.find_by(id_medicamento, key="id_medicamento")
        if not medicamento:
            raise ValueError(f"Medicamento com ID {id_medicamento} não encontrado.")

        # Verificar duplicidade (Mesmo remédio na mesma consulta)
        prescricoes_existentes = self.prescricao_repo.find_by(id_consulta, key="id_consulta")

        if prescricoes_existentes:
            if isinstance(prescricoes_existentes, dict):
                prescricoes_existentes = [prescricoes_existentes]

            for p in prescricoes_existentes:
                if p['id_medicamento'] == id_medicamento:
                    nome_medicamento = medicamento.get('nome_comercial', 'Unknown')
                    raise ValueError(f"O medicamento '{nome_medicamento}' (ID {id_medicamento}) já foi prescrito nesta consulta.")

        self.estoque_service.consumir_por_medicamento(id_medicamento, quantidade)

        return self.prescricao_repo.create(
            id_consulta=id_consulta,
            id_medicamento=id_medicamento,
            quantidade_prescrita=quantidade,
            dosagem=dosagem,
            frequencia_uso=frequencia
        )

    def update_prescricao(self, id_prescricao: int, data: dict):
        update_data = {k: v for k, v in data.items() if v is not None}
        return self.prescricao_repo.update(id_prescricao, **update_data)

    def delete_prescricao(self, id_prescricao: int):
        return self.prescricao_repo.delete(id_prescricao)

    def delete_prescricao_specific(self, id_consulta: int, id_medicamento: int):
        return self.prescricao_repo.delete_by_consulta_and_medicamento(id_consulta, id_medicamento)
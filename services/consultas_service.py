from repositores.ConsultasRepository import ConsultasRepository
from repositores.MedicoRepository import MedicoRepository
from repositores.PacienteRepository import PacienteRepository

class ConsultasService:
    def __init__(self, consulta_repo: ConsultasRepository, medico_repo: MedicoRepository, paciente_repo: PacienteRepository):
        self.consulta_repo = consulta_repo
        self.medico_repo = medico_repo
        self.paciente_repo = paciente_repo

    def get_consultas_by_medico(self, crm: str) -> list:
        return self.consulta_repo.get_by_medico(crm)

    def create_consulta(self, crm: str, id_paciente: int, data_hora: str) -> dict:
        # 1. Validação de Existência de Médico e Paciente
        if not self.medico_repo.find_by(crm):
            raise ValueError(f"Médico com CRM {crm} não encontrado ou inativo.")
        if not self.paciente_repo.get_by_id(id_paciente):
            raise ValueError(f"Paciente com ID {id_paciente} não encontrado.")

        # 2. Validação de Duplicidade (não estritamente duplicidade, mas disponibilidade de slot)
        # O repositório já usa uma procedure SP_AgendarConsulta, que deve garantir a validade
        # do agendamento (dentro do horário de plantão e não ocupado).

        # Se a stored procedure não garantir a atomicidade e validação,
        # poderíamos adicionar aqui uma verificação do slot na agenda do médico.
        # Por enquanto, confiamos na procedure.

        return self.consulta_repo.create(crm, id_paciente, data_hora)

    def get_all_consultas(self):
        return self.consulta_repo.get_all()

    def get_consulta_by_id(self, id_consulta: int):
        consulta = self.consulta_repo.get_by_id(id_consulta)
        if not consulta:
            raise ValueError(f"Consulta com ID {id_consulta} não encontrada.")
        return consulta

    def update_consulta(self, id_consulta: int, status: str = None, data_hora: str = None):
        if not self.consulta_repo.get_by_id(id_consulta):
            raise ValueError(f"Consulta com ID {id_consulta} não encontrada.")

        # Validação do status
        if status and status not in ['A', 'C', 'R']: # Exemplo: Agendada, Concluída, Remarcada
            raise ValueError("Status inválido. Use 'A', 'C' ou 'R'.")

        return self.consulta_repo.update(id_consulta, status, data_hora)

    def delete_consulta(self, id_consulta: int):
        if not self.consulta_repo.get_by_id(id_consulta):
            raise ValueError(f"Consulta com ID {id_consulta} não encontrada.")
        return self.consulta_repo.delete(id_consulta)
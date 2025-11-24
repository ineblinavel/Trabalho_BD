from repositores.ExameRepository import ExameRepository
from repositores.MedicoRepository import MedicoRepository
from repositores.PacienteRepository import PacienteRepository
from repositores.TipoExameRepository import TipoExameRepository

class ExameService:
    def __init__(self, exame_repo: ExameRepository, medico_repo: MedicoRepository, paciente_repo: PacienteRepository, tipo_exame_repo: TipoExameRepository):
        self.exame_repo = exame_repo
        self.medico_repo = medico_repo
        self.paciente_repo = paciente_repo
        self.tipo_exame_repo = tipo_exame_repo

    def create_exame(self, status: str, crm_medico_responsavel: str, data_solicitacao: str, id_paciente: int, id_tipo_exame: int, data_coleta: str = None):
        # 1. Validação de Existência de Médico, Paciente e Tipo de Exame
        if not self.medico_repo.find_by(crm_medico_responsavel):
            raise ValueError(f"Médico com CRM {crm_medico_responsavel} não encontrado ou inativo.")
        if not self.paciente_repo.get_by_id(id_paciente):
            raise ValueError(f"Paciente com ID {id_paciente} não encontrado.")
        if not self.tipo_exame_repo.find_by(id_tipo_exame):
            raise ValueError(f"Tipo de Exame com ID {id_tipo_exame} não encontrado.")

        # 2. Validação do Status
        if status not in ['A', 'C', 'R']: # Exemplo: Agendado, Coletado, Resultado
            raise ValueError("Status inválido. Use 'A', 'C' ou 'R'.")

        return self.exame_repo.create(status, crm_medico_responsavel, data_solicitacao, id_paciente, id_tipo_exame, data_coleta)

    def get_all_exames(self):
        return self.exame_repo.find_all()

    def get_exame_details_by_id(self, id_exame: int):
        exame = self.exame_repo.find_with_details_by_id(id_exame)
        if not exame:
            raise ValueError(f"Exame com ID {id_exame} não encontrado.")
        return exame

    def get_exames_by_paciente_and_status(self, id_paciente: int, status: str):
        if not self.paciente_repo.get_by_id(id_paciente):
            raise ValueError(f"Paciente com ID {id_paciente} não encontrado.")
        if status not in ['A', 'C', 'R']:
            raise ValueError("Status inválido. Use 'A', 'C' ou 'R'.")

        return self.exame_repo.find_by_paciente_and_status(id_paciente, status)

    def update_exame(self, id_exame: int, **kwargs):
        if not self.exame_repo.find_by(id_exame):
            raise ValueError(f"Exame com ID {id_exame} não encontrado.")

        # Validação de IDs externos na atualização
        if 'crm_medico_responsavel' in kwargs and not self.medico_repo.find_by(kwargs['crm_medico_responsavel']):
            raise ValueError(f"Médico com CRM {kwargs['crm_medico_responsavel']} não encontrado.")
        if 'id_paciente' in kwargs and not self.paciente_repo.get_by_id(kwargs['id_paciente']):
            raise ValueError(f"Paciente com ID {kwargs['id_paciente']} não encontrado.")
        if 'id_tipo_exame' in kwargs and not self.tipo_exame_repo.find_by(kwargs['id_tipo_exame']):
            raise ValueError(f"Tipo de Exame com ID {kwargs['id_tipo_exame']} não encontrado.")

        # Validação do Status
        if 'status' in kwargs and kwargs['status'] not in ['A', 'C', 'R']:
            raise ValueError("Status inválido. Use 'A', 'C' ou 'R'.")

        return self.exame_repo.update(id_exame, **kwargs)

    def delete_exame(self, id_exame: int):
        if not self.exame_repo.find_by(id_exame):
            raise ValueError(f"Exame com ID {id_exame} não encontrado.")
        return self.exame_repo.delete(id_exame)
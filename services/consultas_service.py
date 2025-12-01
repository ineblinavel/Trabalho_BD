from repositores.ConsultasRepository import ConsultasRepository
from repositores.MedicoRepository import MedicoRepository
from repositores.PacienteRepository import PacienteRepository
from repositores.AgendaMedicoRepository import AgendaMedicoRepository
from datetime import datetime

class ConsultasService:
    def __init__(self,
                 consulta_repo: ConsultasRepository,
                 medico_repo: MedicoRepository,
                 paciente_repo: PacienteRepository,
                 agenda_repo: AgendaMedicoRepository):
        self.consulta_repo = consulta_repo
        self.medico_repo = medico_repo
        self.paciente_repo = paciente_repo
        self.agenda_repo = agenda_repo

    def get_consultas_by_medico(self, crm: str) -> list:
        return self.consulta_repo.get_by_medico(crm)

    def create_consulta(self, crm: str, id_paciente: int, data_hora: str) -> dict:
        # 1. Validação de Existência de Médico e Paciente
        if not self.medico_repo.find_by(crm):
            raise ValueError(f"Médico com CRM {crm} não encontrado ou inativo.")
        if not self.paciente_repo.get_by_id(id_paciente):
            raise ValueError(f"Paciente com ID {id_paciente} não encontrado.")

        # 2. Validação de Agenda e Disponibilidade
        try:
            # Converte string para objeto datetime. O formato esperado é 'YYYY-MM-DD HH:MM:SS'
            # Ajuste se o seu front-end enviar com 'T' no meio
            dt_agendamento = datetime.strptime(data_hora.replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValueError("Formato de data inválido. Use AAAA-MM-DD HH:MM:SS.")

        data_str = dt_agendamento.strftime('%Y-%m-%d')
        hora_str = dt_agendamento.strftime('%H:%M:%S')

        # Verifica se o médico trabalha neste dia
        agenda = self.agenda_repo.find_by_medico_and_date(crm, data_str)
        if not agenda:
            raise ValueError(f"O médico não possui agenda configurada para a data {data_str}.")

        # Verifica se o horário é um slot válido e livre
        slots_disponiveis = self.agenda_repo.find_available_slots(agenda['id_agenda'])

        if hora_str not in slots_disponiveis:
             # Tenta dar uma mensagem de erro mais útil
             inicio = str(agenda['inicio_platao'])
             fim = str(agenda['fim_platao'])
             if not (inicio <= hora_str < fim):
                 raise ValueError(f"Horário {hora_str} fora do expediente ({inicio} - {fim}).")
             else:
                 raise ValueError(f"Horário {hora_str} indisponível. Verifique se já está ocupado ou se respeita o intervalo de {agenda['duracao_slot_minutos']} minutos.")

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
        if status and status not in ['A', 'C', 'R']:
            raise ValueError("Status inválido. Use 'A', 'C' ou 'R'.")

        return self.consulta_repo.update(id_consulta, status, data_hora)

    def delete_consulta(self, id_consulta: int):
        if not self.consulta_repo.get_by_id(id_consulta):
            raise ValueError(f"Consulta com ID {id_consulta} não encontrada.")
        return self.consulta_repo.delete(id_consulta)
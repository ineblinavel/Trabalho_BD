from repositores.AgendaMedicoRepository import AgendaMedicoRepository
from repositores.MedicoRepository import MedicoRepository

class AgendaMedicoService:
    def __init__(self, agenda_repo: AgendaMedicoRepository, medico_repo: MedicoRepository):
        self.agenda_repo = agenda_repo
        self.medico_repo = medico_repo

    def create_agenda(self, crm: str, data: str, inicio: str, fim: str, duracao: int):
        # 1. Validação de Médico (CRM)
        if not self.medico_repo.find_by(crm):
            raise ValueError(f"Médico com CRM {crm} não encontrado ou inativo.")

        # 2. Validação de Duplicidade (CRM, Data)
        agendas_do_dia = self.agenda_repo.find_by(data, key="data")
        for agenda in agendas_do_dia:
            if agenda.get('crm_medico') == crm:
                raise ValueError(f"O Médico com CRM {crm} já possui uma agenda para a data {data}.")

        # 3. Validação de Lógica de Horário
        if duracao <= 0:
            raise ValueError("A duração do slot deve ser maior que zero.")

        return self.agenda_repo.create(crm, data, inicio, fim, duracao)

    def get_all_agendas(self):
        return self.agenda_repo.find_all()

    def get_agenda_by_id(self, id_agenda: int):
        agenda = self.agenda_repo.find_by(id_agenda)
        if not agenda:
            raise ValueError(f"Agenda com ID {id_agenda} não encontrada.")
        return agenda

    def get_available_slots(self, id_agenda: int):
        return self.agenda_repo.find_available_slots(id_agenda)

    def update_agenda(self, id_agenda: int, data: str, inicio: str, fim: str, duracao: int):
        # 1. Validação de Existência
        if not self.agenda_repo.find_by(id_agenda):
            raise ValueError(f"Agenda com ID {id_agenda} não encontrada.")

        # 2. Revalidação de Duplicidade: Verifica se a mudança de data não colide com outra agenda do mesmo médico.
        agenda_antiga = self.agenda_repo.find_by(id_agenda)
        crm = agenda_antiga.get('crm_medico')
        data_antiga = agenda_antiga.get('data').strftime('%Y-%m-%d')

        if data != data_antiga:
            agendas_do_dia = self.agenda_repo.find_by(data, key="data")
            for agenda in agendas_do_dia:
                if agenda.get('crm_medico') == crm and agenda.get('id_agenda') != id_agenda:
                    raise ValueError(f"O Médico com CRM {crm} já possui uma agenda para a data {data}.")

        return self.agenda_repo.update(id_agenda, data, inicio, fim, duracao)

    def delete_agenda(self, id_agenda: int):
        # 1. Validação de Existência
        if not self.agenda_repo.find_by(id_agenda):
            raise ValueError(f"Agenda com ID {id_agenda} não encontrada.")

        return self.agenda_repo.delete(id_agenda)
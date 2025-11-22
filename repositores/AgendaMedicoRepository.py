from database.Database import Database
from datetime import datetime, timedelta

class AgendaMedicoRepository:
    """
    Classe de repositório para gerenciar a agenda dos médicos.
    """

    def __init__(self, db: Database):
        """
        Inicializa o repositório da agenda médica.

        Args:
            db (Database): Instância da classe de conexão com o banco de dados.
        """
        self.db = db

    def find_all(self) -> list:
        """
        Busca todas as agendas médicas cadastradas.

        Returns:
            list: Uma lista de dicionários representando todas as agendas.
        """
        query = "SELECT * FROM AgendaMedico;"
        return self.db.fetch_all(query)

    def find_by(self, value, key: str = "id_agenda") -> list | dict | None:
        """
        Busca agendas por um campo e valor específicos.

        Args:
            value: O valor a ser buscado.
            key (str): O campo pelo qual buscar (e.g., "id_agenda", "crm_medico", "data").

        Returns:
            list | dict | None: Um dicionário se buscar por 'id_agenda', uma lista para
                                 outras chaves, ou None se nada for encontrado.
        """
        possible_keys = ["id_agenda", "crm_medico", "data"]
        if key not in possible_keys:
            raise ValueError(f"Chave de busca inválida. Use uma das seguintes: {possible_keys}")
        
        query = f"SELECT * FROM AgendaMedico WHERE {key} = %s;"
        results = self.db.fetch_all(query, params=(value,))
        
        if key == "id_agenda":
            return results[0] if results else None
        return results

    def find_available_slots(self, id_agenda: int) -> list:
        """
        Encontra os horários de consulta disponíveis para uma agenda específica,
        excluindo horários já agendados.

        Args:
            id_agenda (int): O ID da agenda a ser verificada.

        Returns:
            list: Uma lista de strings com os horários disponíveis no formato 'HH:MM:SS'.
        """
        agenda_data = self.find_by(id_agenda)
        if not agenda_data:
            return []

        crm = agenda_data.get("crm_medico")
        data = agenda_data.get("data")
        inicio_platao = agenda_data.get("inicio_platao")
        fim_platao = agenda_data.get("fim_platao")
        duracao_slot_minutos = agenda_data.get("duracao_slot_minutos")

        if not all([crm, data, inicio_platao, fim_platao, duracao_slot_minutos]):
            return []

        query = "SELECT data_hora_agendamento FROM Consulta WHERE crm_medico = %s AND DATE(data_hora_agendamento) = %s;"
        params = (crm, data.strftime('%Y-%m-%d'))
        consultas_do_dia = self.db.fetch_all(query, params)
        
        horarios_agendados = {c.get('data_hora_agendamento').time() for c in consultas_do_dia}

        slots_disponiveis = []
        horario_atual = datetime.combine(data, inicio_platao)
        fim_platao_dt = datetime.combine(data, fim_platao)
        
        while horario_atual < fim_platao_dt:
            if horario_atual.time() not in horarios_agendados:
                slots_disponiveis.append(horario_atual.strftime('%H:%M:%S'))
            horario_atual += timedelta(minutes=duracao_slot_minutos)
            
        return slots_disponiveis

    def create(self, crm: str, data: str, inicio: str, fim: str, duracao: int) -> dict:
        """
        Cria um novo registro de agenda para um médico.

        Args:
            crm (str): CRM do médico.
            data (str): Data da agenda ('YYYY-MM-DD').
            inicio (str): Horário de início do plantão ('HH:MM:SS').
            fim (str): Horário de fim do plantão ('HH:MM:SS').
            duracao (int): Duração do slot de atendimento em minutos.

        Returns:
            dict: Dicionário com mensagem de sucesso ou erro.
        """
        if not self._validar_dados(data, inicio, fim):
            raise ValueError("Formatos de data/hora inválidos.")

        query = """
        INSERT INTO AgendaMedico (crm_medico, data, inicio_platao, fim_platao, duracao_slot_minutos)
        VALUES (%s, %s, %s, %s, %s);
        """
        params = (crm, data, inicio, fim, duracao)
        self.db.execute_query(query, params=params)
        return {"message": "Agenda criada com sucesso."}

    def update(self, id_agenda: int, data: str, inicio: str, fim: str, duracao: int) -> dict:
        """
        Atualiza uma agenda existente.

        Args:
            id_agenda (int): ID da agenda a ser atualizada.
            data (str): Nova data da agenda ('YYYY-MM-DD').
            inicio (str): Novo horário de início ('HH:MM:SS').
            fim (str): Novo horário de fim ('HH:MM:SS').
            duracao (int): Nova duração do slot em minutos.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        if not self._validar_dados(data, inicio, fim):
            raise ValueError("Formatos de data/hora inválidos.")

        query = """
        UPDATE AgendaMedico 
        SET data = %s, inicio_platao = %s, fim_platao = %s, duracao_slot_minutos = %s
        WHERE id_agenda = %s;
        """
        params = (data, inicio, fim, duracao, id_agenda)
        self.db.execute_query(query, params=params)
        return {"message": "Agenda atualizada com sucesso."}

    def delete(self, id_agenda: int) -> dict:
        """
        Deleta uma agenda pelo seu ID.

        Args:
            id_agenda (int): ID da agenda a ser deletada.

        Returns:
            dict: Dicionário com mensagem de sucesso.
        """
        query = "DELETE FROM AgendaMedico WHERE id_agenda = %s;"
        self.db.execute_query(query, params=(id_agenda,))
        return {"message": "Agenda deletada com sucesso."}

    def _validar_dados(self, data: str, inicio: str, fim: str) -> bool:
        """
        Valida os formatos de data e hora.

        Args:
            data (str): String da data.
            inicio (str): String do horário de início.
            fim (str): String do horário de fim.

        Returns:
            bool: True se os formatos são válidos, False caso contrário.
        """
        try:
            datetime.strptime(data, '%Y-%m-%d')
            datetime.strptime(inicio, '%H:%M:%S')
            datetime.strptime(fim, '%H:%M:%S')
            return True
        except (ValueError, TypeError):
            return False

from database.Database import Database
from datetime import datetime, timedelta

class AgendaMedicoRepository:
    """
    Classe de repositório para gerenciar a agenda dos médicos.
    """

    def __init__(self, db: Database):
        self.db = db

    def find_all(self) -> list:
        query = "SELECT * FROM AgendaMedico;"
        return self.db.fetch_all(query)

    def find_by(self, value, key: str = "id_agenda") -> list | dict | None:
        possible_keys = ["id_agenda", "crm_medico", "data"]
        if key not in possible_keys:
            raise ValueError(f"Chave de busca inválida. Use uma das seguintes: {possible_keys}")

        query = f"SELECT * FROM AgendaMedico WHERE {key} = %s;"
        results = self.db.fetch_all(query, params=(value,))

        if key == "id_agenda":
            return results[0] if results else None
        return results

    def find_by_medico_and_date(self, crm: str, data: str) -> dict | None:
        """
        Busca a agenda de um médico para uma data específica.
        """
        query = "SELECT * FROM AgendaMedico WHERE crm_medico = %s AND data = %s;"
        return self.db.fetch_one(query, params=(crm, data))

    def find_available_slots(self, id_agenda: int) -> list:
        """
        Retorna lista de horários (strings HH:MM:SS) disponíveis para agendamento.
        """
        agenda_data = self.find_by(id_agenda)
        if not agenda_data:
            return []

        crm = agenda_data.get("crm_medico")
        raw_data = agenda_data.get("data")
        raw_inicio = agenda_data.get("inicio_platao")
        raw_fim = agenda_data.get("fim_platao")
        duracao_slot_minutos = agenda_data.get("duracao_slot_minutos")

        # Conversores robustos
        data = self._ensure_date(raw_data)
        inicio_platao = self._ensure_time(raw_inicio)
        fim_platao = self._ensure_time(raw_fim)

        if not all([crm, data, inicio_platao, fim_platao, duracao_slot_minutos]):
            return []

        # Busca consultas JÁ MARCADAS no dia (exceto canceladas)
        # Garante que data seja string para o SQL
        data_str = data.strftime('%Y-%m-%d') if hasattr(data, 'strftime') else str(data)
        
        query = "SELECT data_hora_agendamento FROM Consulta WHERE crm_medico = %s AND DATE(data_hora_agendamento) = %s AND status != 'C';"
        params = (crm, data_str)
        consultas_do_dia = self.db.fetch_all(query, params)

        # Cria conjunto de horários ocupados para busca rápida
        horarios_agendados = set()
        for c in consultas_do_dia:
            val = c.get('data_hora_agendamento')
            if val:
                # Se for datetime, extrai time. Se for string, tenta parsear ou pegar substring
                if isinstance(val, datetime):
                    horarios_agendados.add(val.strftime('%H:%M:%S'))
                elif isinstance(val, str):
                    # Assume formato ISO ou HH:MM:SS
                    if ' ' in val: # YYYY-MM-DD HH:MM:SS
                        horarios_agendados.add(val.split(' ')[1])
                    else:
                        horarios_agendados.add(val)

        slots_disponiveis = []

        # Loop de geração de slots
        try:
            horario_atual = datetime.combine(data, inicio_platao)
            fim_platao_dt = datetime.combine(data, fim_platao)

            while horario_atual < fim_platao_dt:
                horario_str = horario_atual.strftime('%H:%M:%S')

                # Se não houver colisão, adiciona à lista
                if horario_str not in horarios_agendados:
                    slots_disponiveis.append(horario_str)

                horario_atual += timedelta(minutes=duracao_slot_minutos)
        except Exception as e:
            print(f"Erro ao gerar slots: {e}")
            return []

        return slots_disponiveis

    def _ensure_time(self, val):
        if isinstance(val, timedelta):
            return (datetime.min + val).time()
        if isinstance(val, str):
            try:
                # Tenta HH:MM:SS
                return datetime.strptime(val, "%H:%M:%S").time()
            except ValueError:
                try:
                    # Tenta H:MM:SS (sem zero à esquerda)
                    return datetime.strptime(val, "%H:%M:%S").time()
                except ValueError:
                    pass
        return val

    def _ensure_date(self, val):
        if isinstance(val, str):
            try:
                return datetime.strptime(val, "%Y-%m-%d").date()
            except ValueError:
                pass
        return val

    def create(self, crm: str, data: str, inicio: str, fim: str, duracao: int) -> dict:
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
        query = "DELETE FROM AgendaMedico WHERE id_agenda = %s;"
        self.db.execute_query(query, params=(id_agenda,))
        return {"message": "Agenda deletada com sucesso."}

    def _validar_dados(self, data: str, inicio: str, fim: str) -> bool:
        try:
            datetime.strptime(data, '%Y-%m-%d')
            datetime.strptime(inicio, '%H:%M:%S')
            datetime.strptime(fim, '%H:%M:%S')
            return True
        except (ValueError, TypeError):
            return False
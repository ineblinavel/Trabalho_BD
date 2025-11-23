from repositores.PacienteRepository import PacienteRepository
from datetime import datetime

class PacienteService:
    def __init__(self, paciente_repo: PacienteRepository):
        self.paciente_repo = paciente_repo

    def create_paciente(self, nome: str, cpf: str, data_nascimento: str, endereco: str):
        # 1. Validação de Duplicidade (CPF)
        pacientes = self.paciente_repo.get_all()
        for p in pacientes:
            if p.get('cpf') == cpf:
                raise ValueError(f"Paciente com CPF {cpf} já cadastrado.")

        # 2. Validação de Idade (Exemplo: não aceitar paciente com data futura)
        try:
            nasc = datetime.strptime(data_nascimento, '%Y-%m-%d')
            if nasc > datetime.now():
                raise ValueError("Data de nascimento não pode ser futura.")
        except ValueError as e:
            # Re-raise o erro de formato de data se for o caso
            if "não pode ser futura" in str(e):
                raise
            raise ValueError("Formato de data de nascimento inválido. Use 'YYYY-MM-DD'.")

        return self.paciente_repo.create(nome, cpf, data_nascimento, endereco)

    def get_all_pacientes(self):
        return self.paciente_repo.get_all()

    def get_paciente_by_id(self, id_paciente: int):
        paciente = self.paciente_repo.get_by_id(id_paciente)
        if not paciente:
            raise ValueError(f"Paciente com ID {id_paciente} não encontrado.")
        return paciente

    def get_paciente_historico(self, id_paciente: int):
        if not self.paciente_repo.get_by_id(id_paciente):
            raise ValueError(f"Paciente com ID {id_paciente} não encontrado.")
        return self.paciente_repo.get_historico_completo(id_paciente)

    def update_foto(self, id_paciente: int, foto_data: bytes):
        if not self.paciente_repo.get_by_id(id_paciente):
            raise ValueError(f"Paciente com ID {id_paciente} não encontrado.")
        return self.paciente_repo.update_foto(id_paciente, foto_data)

    # Nota: Não há um método `update` no repositório de Paciente, nem `delete`.
    # O `app.py` não importa um serviço de Paciente, o que sugere que o CRUD completo
    # pode não ser uma prioridade inicial, mas podemos adicionar:

    # def delete_paciente(self, id_paciente: int):
    #     if not self.paciente_repo.get_by_id(id_paciente):
    #         raise ValueError(f"Paciente com ID {id_paciente} não encontrado.")
    #     # Assumindo que você adicionou um método `delete` no PacienteRepository:
    #     return self.paciente_repo.delete(id_paciente)
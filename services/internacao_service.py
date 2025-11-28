from repositores.InternacaoRepository import InternacaoRepository
from repositores.MedicoRepository import MedicoRepository
from repositores.PacienteRepository import PacienteRepository
from repositores.EnfermeiroRepository import EnfermeiroRepository
from repositores.QuartoRepository import QuartoRepository

class InternacaoService:
    def __init__(self, internacao_repo: InternacaoRepository, medico_repo: MedicoRepository, paciente_repo: PacienteRepository, enfermeiro_repo: EnfermeiroRepository, quarto_repo: QuartoRepository):
        self.internacao_repo = internacao_repo
        self.medico_repo = medico_repo
        self.paciente_repo = paciente_repo
        self.enfermeiro_repo = enfermeiro_repo
        self.quarto_repo = quarto_repo

    def create_internacao(self, id_paciente: int, crm_medico: str, corem_enfermeiro: str, id_quarto: int = None, data_admissao: str = None, data_alta_prevista: str = None):
        # ... (Validações de existência de IDs anteriores mantêm-se iguais) ...

        # 2. Regra de Negócio: Paciente não pode ter internação ativa
        internacoes_ativas = self.internacao_repo.find_active()
        for internacao in internacoes_ativas:
            if internacao.get('id_paciente') == id_paciente:
                raise ValueError(f"Paciente já possui uma internação ativa.")

        # 3. Regra de Negócio: Quarto deve estar disponível (CORREÇÃO DE LÓGICA)
        if id_quarto:
            # Converte para int para garantir a comparação correta
            id_quarto_int = int(id_quarto)

            for internacao in internacoes_ativas:
                # Verifica se existe alguma internação ativa neste ID de quarto
                if internacao.get('id_quarto') == id_quarto_int:
                    raise ValueError(f"O Quarto selecionado (ID {id_quarto}) já está ocupado.")

        return self.internacao_repo.create(id_paciente, crm_medico, corem_enfermeiro, id_quarto=id_quarto, data_admissao=data_admissao, data_alta_prevista=data_alta_prevista)

    def get_all_internacoes(self):
        return self.internacao_repo.find_all()

    def get_internacao_by_id(self, id_internacao: int):
        internacao = self.internacao_repo.find_by(id_internacao)
        if not internacao:
            raise ValueError(f"Internação com ID {id_internacao} não encontrada.")
        return internacao

    def update_internacao(self, id_internacao: int, **kwargs):
        internacao_existente = self.internacao_repo.find_by(id_internacao)
        if not internacao_existente:
            raise ValueError(f"Internação com ID {id_internacao} não encontrada.")

        # Validação de IDs externos na atualização
        if 'crm_medico' in kwargs and not self.medico_repo.find_by(kwargs['crm_medico']):
            raise ValueError(f"Médico com CRM {kwargs['crm_medico']} não encontrado.")
        if 'corem_enfermeiro' in kwargs and not self.enfermeiro_repo.find_by(kwargs['corem_enfermeiro']):
            raise ValueError(f"Enfermeiro com COREM {kwargs['corem_enfermeiro']} não encontrado.")
        if 'id_quarto' in kwargs and kwargs['id_quarto'] and not self.quarto_repo.find_by(kwargs['id_quarto']):
            raise ValueError(f"Quarto com ID {kwargs['id_quarto']} não encontrado.")

        # Regra de Negócio: Quarto deve estar disponível (se for alterado)
        if 'id_quarto' in kwargs and kwargs['id_quarto'] and kwargs['id_quarto'] != internacao_existente.get('id_quarto'):
            internacoes_ativas = self.internacao_repo.find_active()
            for internacao in internacoes_ativas:
                if internacao.get('id_quarto') == kwargs['id_quarto'] and internacao.get('id_internacao') != id_internacao:
                    raise ValueError(f"Quarto com ID {kwargs['id_quarto']} está atualmente ocupado por outra internação.")

        return self.internacao_repo.update(id_internacao, **kwargs)

    def realizar_alta(self, id_internacao: int, data_alta_efetiva: str):
        if not self.internacao_repo.find_by(id_internacao):
            raise ValueError(f"Internação com ID {id_internacao} não encontrada.")
        return self.internacao_repo.realizar_alta(id_internacao, data_alta_efetiva)

    def delete_internacao(self, id_internacao: int):
        if not self.internacao_repo.find_by(id_internacao):
            raise ValueError(f"Internação com ID {id_internacao} não encontrada.")
        return self.internacao_repo.delete(id_internacao)

    def get_active_internacoes(self):
        """Retorna todas as internações ativas (sem data de alta efetiva)."""
        return self.internacao_repo.find_active()
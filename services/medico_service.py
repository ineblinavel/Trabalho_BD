from repositores.MedicoRepository import MedicoRepository
from repositores.UsuarioRepository import UsuarioRepository
from utils.password_generator import generate_password

class MedicoService:
    def __init__(self, medico_repo: MedicoRepository, usuario_repo: UsuarioRepository = None):
        self.medico_repo = medico_repo
        self.usuario_repo = usuario_repo

    def create_medico(self, crm: str, nome_medico: str, cpf: str, salario: float):
        # Business logic, like validation, could be added here in the future.
        result = self.medico_repo.create(crm, nome_medico, cpf, salario)
        
        senha_gerada = None
        if self.usuario_repo:
            # Verifica se já existe usuário (caso de re-cadastro ou erro anterior)
            if not self.usuario_repo.get_by_username(crm):
                senha_gerada = generate_password()
                self.usuario_repo.create_user(
                    username=crm,
                    password=senha_gerada,
                    role='medico',
                    referencia_id=crm
                )
                result['senha_gerada'] = senha_gerada
                result['message'] += f" Usuário criado. Senha: {senha_gerada}"
        
        return result

    def get_all_medicos(self, include_inactive: bool = False):
        return self.medico_repo.find_all(include_inactive=include_inactive)

    def get_medico_by_crm(self, crm: str):
        return self.medico_repo.find_by_crm_with_phones(crm)
    
    def update_medico(self, crm: str, nome_medico: str = None, cpf: str = None, salario: float = None):
        if not self.medico_repo.find_by(crm):
            raise ValueError(f"Médico com CRM {crm} não encontrado.")
        
        update_data = {}
        if nome_medico: update_data['nome_medico'] = nome_medico
        if cpf: update_data['cpf'] = cpf
        if salario is not None: update_data['salario'] = salario
        
        return self.medico_repo.update(crm, **update_data)

    def delete_medico(self, crm: str):
        # Soft delete (Desativar)
        if not self.medico_repo.find_by(crm, active_only=False):
             raise ValueError(f"Médico com CRM {crm} não encontrado.")
        return self.medico_repo.deactivate(crm)

    def reactivate_medico(self, crm: str):
        if not self.medico_repo.find_by(crm, active_only=False):
             raise ValueError(f"Médico com CRM {crm} não encontrado.")
        return self.medico_repo.reactivate(crm)

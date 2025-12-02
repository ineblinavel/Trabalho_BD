from repositores.UsuarioRepository import UsuarioRepository
from repositores.EnfermeiroRepository import EnfermeiroRepository
from repositores.MedicoRepository import MedicoRepository

class AuthService:
    def __init__(self, usuario_repo: UsuarioRepository, enfermeiro_repo: EnfermeiroRepository = None, medico_repo: MedicoRepository = None):
        self.usuario_repo = usuario_repo
        self.enfermeiro_repo = enfermeiro_repo
        self.medico_repo = medico_repo

    def login(self, username, password):
        user = self.usuario_repo.get_by_username(username)
        if not user:
            return None

        # Senha simples por enquanto (projeto atual). Em produção usar hash.
        if user['password'] != password:
            return None

        # Checa se usuário está ativo
        if 'ativo' in user and not user['ativo']:
            return {'status': 'inactive', 'user': user}

        # Tenta buscar o nome real se houver repositórios configurados
        real_name = None
        role = user.get('role')
        ref_id = user.get('referencia_id')

        if ref_id:
            if role == 'enfermeiro' and self.enfermeiro_repo:
                enf = self.enfermeiro_repo.find_by(ref_id, key='corem')
                if enf:
                    real_name = enf.get('nome_enfermeiro')
            elif role == 'medico' and self.medico_repo:
                med = self.medico_repo.find_by(ref_id, key='crm')
                if med:
                    real_name = med.get('nome_medico')
        
        if real_name:
            user['real_name'] = real_name

        return {'status': 'ok', 'user': user}

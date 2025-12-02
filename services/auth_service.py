from repositores.UsuarioRepository import UsuarioRepository

class AuthService:
    def __init__(self, usuario_repo: UsuarioRepository):
        self.usuario_repo = usuario_repo

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

        return {'status': 'ok', 'user': user}

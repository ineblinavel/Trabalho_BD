from repositores.UsuarioRepository import UsuarioRepository

class AuthService:
    def __init__(self, usuario_repo: UsuarioRepository):
        self.usuario_repo = usuario_repo

    def login(self, username, password):
        user = self.usuario_repo.get_by_username(username)
        if user and user['password'] == password: 
            return user
        return None

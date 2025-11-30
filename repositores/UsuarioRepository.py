from database.Database import Database

class UsuarioRepository:
    def __init__(self, db: Database):
        self.db = db

    def get_by_username(self, username: str):
        query = "SELECT * FROM Usuarios WHERE username = %s"
        return self.db.fetch_one(query, (username,))

    def create_user(self, username, password, role, referencia_id=None):
        query = "INSERT INTO Usuarios (username, password, role, referencia_id) VALUES (%s, %s, %s, %s)"
        self.db.execute_query(query, (username, password, role, referencia_id))

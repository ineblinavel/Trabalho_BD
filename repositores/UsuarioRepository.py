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

    def delete_by_referencia(self, referencia_id: str, role: str = None) -> dict:
        if role:
            query = "DELETE FROM Usuarios WHERE referencia_id = %s AND role = %s;"
            params = (referencia_id, role)
        else:
            query = "DELETE FROM Usuarios WHERE referencia_id = %s;"
            params = (referencia_id,)
        self.db.execute_query(query, params=params)
        return {"message": "Usuário(s) deletado(s) com sucesso."}

    def set_ativo_by_referencia(self, referencia_id: str, ativo: bool, role: str = None) -> dict:
        if role:
            query = "UPDATE Usuarios SET ativo = %s WHERE referencia_id = %s AND role = %s;"
            params = (1 if ativo else 0, referencia_id, role)
        else:
            query = "UPDATE Usuarios SET ativo = %s WHERE referencia_id = %s;"
            params = (1 if ativo else 0, referencia_id)
        self.db.execute_query(query, params=params)
        return {"message": "Campo ativo atualizado."}

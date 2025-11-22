from repositores.QuartoRepository import QuartoRepository

class QuartoService:
    def __init__(self, repo: QuartoRepository):
        self.repo = repo

    def get_all(self):
        return self.repo.get_all()

    def get_mapa_leitos(self):
        # Retorna a view com status de ocupação
        return self.repo.get_mapa_leitos()

    def get_by_id(self, num_quarto: int):
        return self.repo.get_by_id(num_quarto)

    def create(self, num_quarto: int, tipo: str, valor: float):
        return self.repo.create(num_quarto, tipo, valor)

    def update(self, num_quarto: int, data: dict):
        return self.repo.update(num_quarto, 
                                tipo_de_quarto=data.get('tipo_de_quarto'), 
                                valor_diaria=data.get('valor_diaria'))
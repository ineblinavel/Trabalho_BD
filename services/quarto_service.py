from repositores.QuartoRepository import QuartoRepository

class QuartoService:
    def __init__(self, repo: QuartoRepository):
        self.repo = repo

    def get_all(self):
        return self.repo.get_all()

    def get_mapa_leitos(self):
        return self.repo.get_mapa_leitos()

    def get_by_id(self, num_quarto: int):
        return self.repo.get_by_id(num_quarto)

    def create(self, num_quarto: int, tipo: str, valor: float):
        if valor < 0:
            raise ValueError("O valor da diária não pode ser negativo.")

        if self.repo.get_by_id(num_quarto):
            raise ValueError(f"O quarto número {num_quarto} já existe.")

        return self.repo.create(num_quarto, tipo, valor)

    def update(self, num_quarto: int, data: dict):
        if not self.repo.get_by_id(num_quarto):
            raise ValueError(f"Quarto número {num_quarto} não encontrado.")

        update_data = {k: v for k, v in data.items() if v is not None}

        if 'valor_diaria' in update_data:
            try:
                valor = float(update_data['valor_diaria'])
                if valor < 0:
                    raise ValueError("O valor da diária não pode ser negativo.")
            except ValueError:
                 raise ValueError("O valor da diária é inválido.")

        return self.repo.update(num_quarto, 
                                tipo_de_quarto=update_data.get('tipo_de_quarto'), 
                                valor_diaria=update_data.get('valor_diaria'))
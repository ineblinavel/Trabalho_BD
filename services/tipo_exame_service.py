from repositores.TipoExameRepository import TipoExameRepository

class TipoExameService:
    def __init__(self, repo: TipoExameRepository):
        self.repo = repo

    def get_all(self):
        return self.repo.find_all()

    def get_by_id(self, id_tipo: int):
        return self.repo.find_by(id_tipo, key="id_tipo_exame")

    def create(self, nome: str, preco: float, descricao: str = None):
        if not nome or not nome.strip():
            raise ValueError("O nome do exame é obrigatório.")
            
        if preco < 0:
            raise ValueError("O preço do exame não pode ser negativo.")

        return self.repo.create(nome, preco, descricao)

    def update(self, id_tipo: int, data: dict):
        if not self.repo.find_by(id_tipo, key="id_tipo_exame"):
            raise ValueError(f"Tipo de exame {id_tipo} não encontrado.")

        update_data = {k: v for k, v in data.items() if v is not None}
        
        if 'nome_do_exame' in update_data:
            if not update_data['nome_do_exame'].strip():
                raise ValueError("O nome do exame não pode ser vazio.")

        if 'preco' in update_data:
            try:
                preco = float(update_data['preco'])
                if preco < 0:
                    raise ValueError("O preço do exame não pode ser negativo.")
            except ValueError:
                 raise ValueError("O valor do preço é inválido.")

        return self.repo.update(id_tipo, **update_data)

    def delete(self, id_tipo: int):
        return self.repo.delete(id_tipo)
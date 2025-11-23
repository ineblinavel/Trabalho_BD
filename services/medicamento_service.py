from repositores.MedicamentoRepository import MedicamentoRepository

class MedicamentoService:
    def __init__(self, medicamento_repo: MedicamentoRepository):
        self.medicamento_repo = medicamento_repo

    def create_medicamento(self, nome_comercial: str, fabricante: str = None):
        # 1. Validação de Duplicidade (Nome Comercial)
        # Buscar por nome comercial e verificar se já existe um cadastro idêntico (fabricante e nome)
        medicamentos_iguais = self.medicamento_repo.find_by(nome_comercial, key="nome_comercial")
        for med in medicamentos_iguais:
            if med.get('fabricante') == fabricante:
                raise ValueError(f"Medicamento '{nome_comercial}' do fabricante '{fabricante}' já cadastrado.")

        return self.medicamento_repo.create(nome_comercial, fabricante)

    def get_all_medicamentos(self):
        return self.medicamento_repo.find_all()

    def get_medicamento_by_id(self, id_medicamento: int):
        medicamento = self.medicamento_repo.find_by(id_medicamento)
        if not medicamento:
            raise ValueError(f"Medicamento com ID {id_medicamento} não encontrado.")
        return medicamento

    def update_medicamento(self, id_medicamento: int, nome_comercial: str = None, fabricante: str = None):
        medicamento_existente = self.medicamento_repo.find_by(id_medicamento)
        if not medicamento_existente:
            raise ValueError(f"Medicamento com ID {id_medicamento} não encontrado.")

        update_data = {}
        if nome_comercial:
            update_data['nome_comercial'] = nome_comercial
        if fabricante:
            update_data['fabricante'] = fabricante

        if not update_data:
            return {"message": "Nenhum dado fornecido para atualização."}

        # 1. Validação de Duplicidade na atualização
        novo_nome = update_data.get('nome_comercial', medicamento_existente.get('nome_comercial'))
        novo_fabricante = update_data.get('fabricante', medicamento_existente.get('fabricante'))

        medicamentos_iguais = self.medicamento_repo.find_by(novo_nome, key="nome_comercial")
        for med in medicamentos_iguais:
            if med.get('fabricante') == novo_fabricante and med.get('id_medicamento') != id_medicamento:
                raise ValueError(f"Medicamento '{novo_nome}' do fabricante '{novo_fabricante}' já cadastrado para outro ID.")

        return self.medicamento_repo.update(id_medicamento, **update_data)

    def delete_medicamento(self, id_medicamento: int):
        if not self.medicamento_repo.find_by(id_medicamento):
            raise ValueError(f"Medicamento com ID {id_medicamento} não encontrado.")
        # É importante notar que o banco de dados pode restringir a deleção
        # se houver Prescricao usando este medicamento (ON DELETE RESTRICT).
        return self.medicamento_repo.delete(id_medicamento)
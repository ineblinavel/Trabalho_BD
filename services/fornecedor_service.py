from repositores.FornecedorRepository import FornecedorRepository

class FornecedorService:
    def __init__(self, fornecedor_repo: FornecedorRepository):
        self.fornecedor_repo = fornecedor_repo

    def create_fornecedor(self, cnpj: str, nome_empresa: str):
        # 1. Validação de Duplicidade (CNPJ)
        if self.fornecedor_repo.find_by(cnpj):
            raise ValueError(f"Fornecedor com CNPJ {cnpj} já cadastrado.")

        return self.fornecedor_repo.create(cnpj, nome_empresa)

    def get_all_fornecedores(self):
        return self.fornecedor_repo.find_all()

    def get_fornecedor_by_cnpj(self, cnpj: str):
        fornecedor = self.fornecedor_repo.find_by(cnpj)
        if not fornecedor:
            raise ValueError(f"Fornecedor com CNPJ {cnpj} não encontrado.")
        return fornecedor

    def update_fornecedor(self, cnpj: str, nome_empresa: str = None):
        if not self.fornecedor_repo.find_by(cnpj):
            raise ValueError(f"Fornecedor com CNPJ {cnpj} não encontrado.")

        update_data = {}
        if nome_empresa:
            update_data['nome_empresa'] = nome_empresa

        if not update_data:
            return {"message": "Nenhum dado fornecido para atualização."}

        return self.fornecedor_repo.update(cnpj, **update_data)

    def delete_fornecedor(self, cnpj: str):
        if not self.fornecedor_repo.find_by(cnpj):
            raise ValueError(f"Fornecedor com CNPJ {cnpj} não encontrado.")
        return self.fornecedor_repo.delete(cnpj)
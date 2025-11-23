from repositores.EnfermeiroRepository import EnfermeiroRepository

class EnfermeiroService:
    def __init__(self, enfermeiro_repo: EnfermeiroRepository):
        self.enfermeiro_repo = enfermeiro_repo

    def create_enfermeiro(self, corem: str, cpf: str, nome_enfermeiro: str):
        # 1. Validação de Duplicidade (COREM)
        if self.enfermeiro_repo.find_by(corem):
            raise ValueError(f"Enfermeiro com COREM {corem} já cadastrado.")

        # 2. Validação de Duplicidade (CPF)
        if self.enfermeiro_repo.find_by(cpf, key="cpf"):
            raise ValueError(f"Enfermeiro com CPF {cpf} já cadastrado.")

        return self.enfermeiro_repo.create(corem, cpf, nome_enfermeiro)

    def get_all_enfermeiros(self):
        return self.enfermeiro_repo.find_all()

    def get_enfermeiro_by_corem(self, corem: str):
        enfermeiro = self.enfermeiro_repo.find_by(corem)
        if not enfermeiro:
            raise ValueError(f"Enfermeiro com COREM {corem} não encontrado.")
        return enfermeiro

    def update_enfermeiro(self, corem: str, cpf: str = None, nome_enfermeiro: str = None):
        # 1. Validação de Existência
        if not self.enfermeiro_repo.find_by(corem):
            raise ValueError(f"Enfermeiro com COREM {corem} não encontrado.")

        # 2. Validação de Duplicidade (CPF)
        if cpf:
            enfermeiro_cpf = self.enfermeiro_repo.find_by(cpf, key="cpf")
            if enfermeiro_cpf and enfermeiro_cpf.get('corem') != corem:
                raise ValueError(f"O CPF {cpf} já está cadastrado para outro enfermeiro.")

        update_data = {}
        if cpf:
            update_data['cpf'] = cpf
        if nome_enfermeiro:
            update_data['nome_enfermeiro'] = nome_enfermeiro

        if not update_data:
            return {"message": "Nenhum dado fornecido para atualização."}

        return self.enfermeiro_repo.update(corem, **update_data)

    def delete_enfermeiro(self, corem: str):
        if not self.enfermeiro_repo.find_by(corem):
            raise ValueError(f"Enfermeiro com COREM {corem} não encontrado.")
        return self.enfermeiro_repo.delete(corem)
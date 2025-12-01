from repositores.EstoqueMedicamentoRepository import EstoqueMedicamentoRepository
from repositores.MedicamentoRepository import MedicamentoRepository
from repositores.FornecedorRepository import FornecedorRepository

class EstoqueMedicamentoService:
    def __init__(self, estoque_repo: EstoqueMedicamentoRepository, medicamento_repo: MedicamentoRepository, fornecedor_repo: FornecedorRepository):
        self.estoque_repo = estoque_repo
        self.medicamento_repo = medicamento_repo
        self.fornecedor_repo = fornecedor_repo

    def create_estoque(self, data_validade: str, preco_unitario: float, quantidade: int, id_medicamento: int, cnpj_fornecedor: str):
        # 1. Validação de Existência de Medicamento
        if not self.medicamento_repo.find_by(id_medicamento):
            raise ValueError(f"Medicamento com ID {id_medicamento} não encontrado.")

        # 2. Validação de Existência de Fornecedor
        if not self.fornecedor_repo.find_by(cnpj_fornecedor):
            raise ValueError(f"Fornecedor com CNPJ {cnpj_fornecedor} não encontrado.")

        # 3. Validação de Lógica
        if quantidade <= 0:
            raise ValueError("A quantidade em estoque deve ser maior que zero.")
        if preco_unitario <= 0:
            raise ValueError("O preço unitário deve ser maior que zero.")

        return self.estoque_repo.create(data_validade, preco_unitario, quantidade, id_medicamento, cnpj_fornecedor)

    def get_all_estoque(self):
        return self.estoque_repo.find_all()

    def get_estoque_by_id(self, id_estoque: int):
        estoque = self.estoque_repo.find_by(id_estoque)
        if not estoque:
            raise ValueError(f"Item de estoque com ID {id_estoque} não encontrado.")
        return estoque

    def get_expired_stock(self):
        return self.estoque_repo.find_expired()

    def update_estoque(self, id_estoque: int, **kwargs):
        if not self.estoque_repo.find_by(id_estoque):
            raise ValueError(f"Item de estoque com ID {id_estoque} não encontrado.")

        # 1. Validação de IDs externos na atualização
        if 'id_medicamento' in kwargs and not self.medicamento_repo.find_by(kwargs['id_medicamento']):
            raise ValueError(f"Medicamento com ID {kwargs['id_medicamento']} não encontrado.")
        if 'cnpj_fornecedor' in kwargs and not self.fornecedor_repo.find_by(kwargs['cnpj_fornecedor']):
            raise ValueError(f"Fornecedor com CNPJ {kwargs['cnpj_fornecedor']} não encontrado.")

        # 2. Validação de Lógica
        if 'quantidade' in kwargs and kwargs['quantidade'] < 0:
            raise ValueError("A quantidade não pode ser negativa.")
        if 'preco_unitario' in kwargs and kwargs['preco_unitario'] <= 0:
            raise ValueError("O preço unitário deve ser maior que zero.")

        return self.estoque_repo.update(id_estoque, **kwargs)

    def delete_estoque(self, id_estoque: int):
        if not self.estoque_repo.find_by(id_estoque):
            raise ValueError(f"Item de estoque com ID {id_estoque} não encontrado.")
        return self.estoque_repo.delete(id_estoque)

    def consumir_estoque(self, id_estoque: int, quantidade_consumida: int):
        # 1. Busca o item de estoque
        item = self.estoque_repo.find_by(id_estoque)
        if not item:
            raise ValueError(f"Item de estoque com ID {id_estoque} não encontrado.")

        quantidade_atual = item['quantidade']

        # 2. Valida se há estoque suficiente
        if quantidade_consumida <= 0:
            raise ValueError("A quantidade a ser consumida deve ser maior que zero.")

        if quantidade_atual < quantidade_consumida:
            raise ValueError(f"Estoque insuficiente. Disponível: {quantidade_atual}, Solicitado: {quantidade_consumida}.")

        # 3. Atualiza a quantidade
        nova_quantidade = quantidade_atual - quantidade_consumida
        return self.estoque_repo.update(id_estoque, quantidade=nova_quantidade)

    def consumir_por_medicamento(self, id_medicamento: int, quantidade_total: int):
        # 1. Busca lotes disponíveis (do que vence antes para o depois)
        lotes = self.estoque_repo.find_batches_by_medicamento(id_medicamento)

        # 2. Verifica se tem saldo total suficiente
        estoque_total = sum(l['quantidade'] for l in lotes)
        if estoque_total < quantidade_total:
            raise ValueError(f"Estoque insuficiente. Disponível: {estoque_total}, Solicitado: {quantidade_total}")

        # 3. Itera sobre os lotes e consome
        restante = quantidade_total
        for lote in lotes:
            if restante <= 0:
                break

            qtd_para_tirar = min(lote['quantidade'], restante)

            # Reusa o método consumir_estoque que já existe (ele faz o UPDATE)
            self.consumir_estoque(lote['id_estoque_medicamento'], qtd_para_tirar)

            restante -= qtd_para_tirar
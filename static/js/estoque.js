document.addEventListener("DOMContentLoaded", () => {
  carregarEstoque();
  verificarVencidos();
});

async function carregarEstoque() {
  try {
    const estoque = await API.get("/estoque/");
    const tbody = document.querySelector("#tabela-estoque tbody");
    tbody.innerHTML = "";

    if (estoque.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" class="text-center text-muted py-4">Nenhum item em estoque.</td></tr>`;
      return;
    }

    estoque.forEach((item) => {
      const tr = document.createElement("tr");

      // Formatação de Valores
      const validade = new Date(item.data_validade);
      const hoje = new Date();
      const isVencido = validade < hoje;

      const dataFormatada = validade.toLocaleDateString("pt-BR", {
        timeZone: "UTC",
      });
      const precoFormatado = new Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: "BRL",
      }).format(item.preco_unitario);

      // Badge de Validade
      const badgeValidade = isVencido
        ? `<span class="badge bg-danger bg-opacity-10 text-danger"><i class="bi bi-exclamation-circle"></i> Vencido (${dataFormatada})</span>`
        : `<span class="text-muted">${dataFormatada}</span>`;

      tr.innerHTML = `
                <td><span class="text-muted small">#${item.id_estoque_medicamento}</span></td>
                <td class="fw-bold text-dark">
                    <i class="bi bi-capsule text-primary me-2"></i> ID: ${item.id_medicamento}
                </td>
                <td class="small text-muted">${item.cnpj_fornecedor}</td>
                <td>
                    <span class="badge bg-light text-dark border">
                        ${item.quantidade} un
                    </span>
                </td>
                <td>${precoFormatado}</td>
                <td>${badgeValidade}</td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary border-0 me-1" onclick="consumirItem(${item.id_estoque_medicamento})" title="Consumir Item">
                        <i class="bi bi-box-arrow-down"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger border-0" onclick="deletarItem(${item.id_estoque_medicamento})" title="Excluir Lote">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            `;
      tbody.appendChild(tr);
    });
  } catch (error) {
    console.error("Erro ao carregar estoque:", error);
    document.querySelector(
      "#tabela-estoque tbody"
    ).innerHTML = `<tr><td colspan="7" class="text-center text-danger">Erro ao conectar com o servidor.</td></tr>`;
  }
}

async function verificarVencidos() {
  try {
    const vencidos = await API.get("/estoque/vencidos");
    const container = document.getElementById("alerta-vencidos-container");

    if (vencidos && vencidos.length > 0) {
      container.innerHTML = `
                <div class="alert alert-danger d-flex align-items-center shadow-sm border-0 mb-4" role="alert">
                    <i class="bi bi-exclamation-triangle-fill fs-4 me-3"></i>
                    <div>
                        <strong>Atenção Necessária!</strong>
                        <div class="small">Existem ${vencidos.length} lotes de medicamentos com a data de validade expirada. Remova-os ou regularize a situação.</div>
                    </div>
                </div>
            `;
    }
  } catch (e) {
    console.error("Erro ao verificar vencidos", e);
  }
}

async function consumirItem(id) {
  const quantidade = prompt("Quantas unidades deseja retirar do estoque?", "1");
  if (quantidade === null) return;

  const qtdNum = parseInt(quantidade);
  if (isNaN(qtdNum) || qtdNum <= 0) {
    alert("Por favor, insira uma quantidade válida.");
    return;
  }

  try {
    await API.post(`/estoque/${id}/consumir`, { quantidade: qtdNum });
    alert("Saída de estoque registrada com sucesso!");
    carregarEstoque();
  } catch (error) {
    alert("Erro ao registrar saída: " + error.message);
  }
}

async function deletarItem(id) {
  if (confirm("Tem certeza que deseja remover este lote do estoque?")) {
    try {
      await API.delete(`/estoque/${id}`);
      carregarEstoque(); // Recarrega a tabela
      verificarVencidos(); // Recarrega alertas
    } catch (error) {
      alert("Erro ao deletar: " + error.message);
    }
  }
}

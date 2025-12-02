let listaEstoqueGlobal = [];

document.addEventListener("DOMContentLoaded", () => {
  carregarEstoque();
});

async function carregarEstoque() {
  const tbody = document.querySelector("#tabela-estoque tbody");

  try {
    // 1. Busca Paralela de Dados (Estoque, Medicamentos, Fornecedores)
    const [estoque, medicamentos, fornecedores] = await Promise.all([
      API.get("/estoque/"),
      API.get("/medicamentos/"),
      API.get("/fornecedores/"),
    ]);

    // 2. Mapeamento para acesso rápido (ID -> Nome)
    const mapMedicamentos = {};
    medicamentos.forEach((m) => (mapMedicamentos[m.id_medicamento] = m));

    const mapFornecedores = {};
    fornecedores.forEach((f) => (mapFornecedores[f.cnpj] = f.nome_empresa));

    // 3. Processamento dos Dados
    listaEstoqueGlobal = estoque.map((item) => {
      const med = mapMedicamentos[item.id_medicamento] || {
        nome_comercial: "Desconhecido",
        fabricante: "-",
      };
      const nomeForn =
        mapFornecedores[item.cnpj_fornecedor] || item.cnpj_fornecedor;

      return {
        ...item,
        nome_medicamento: med.nome_comercial,
        fabricante: med.fabricante,
        nome_fornecedor: nomeForn,
        data_validade_obj: new Date(item.data_validade),
      };
    });

    renderizarTabela(listaEstoqueGlobal);
    atualizarKPIs(listaEstoqueGlobal);
  } catch (error) {
    console.error("Erro ao carregar estoque:", error);
    tbody.innerHTML = `<tr><td colspan="6" class="text-center text-danger py-4">Erro ao conectar com o servidor: ${error.message}</td></tr>`;
  }
}

function renderizarTabela(lista) {
  const tbody = document.querySelector("#tabela-estoque tbody");
  tbody.innerHTML = "";

  if (lista.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted py-5">Nenhum item encontrado.</td></tr>`;
    return;
  }

  const hoje = new Date();

  lista.forEach((item) => {
    const tr = document.createElement("tr");

    // Lógica de Status (Vencido ou Perto de Vencer)
    const diasParaVencer =
      (item.data_validade_obj - hoje) / (1000 * 60 * 60 * 24);
    let badgeValidade = `<span class="badge bg-light text-dark border"><i class="bi bi-calendar me-1"></i> ${item.data_validade_obj.toLocaleDateString(
      "pt-BR",
      { timeZone: "UTC" }
    )}</span>`;

    if (diasParaVencer < 0) {
      badgeValidade = `<span class="badge bg-danger bg-opacity-10 text-danger"><i class="bi bi-exclamation-circle me-1"></i> Vencido</span>`;
    } else if (diasParaVencer < 30) {
      badgeValidade = `<span class="badge bg-warning text-dark"><i class="bi bi-hourglass-split me-1"></i> Vence em ${Math.ceil(
        diasParaVencer
      )} dias</span>`;
    }

    // Lógica de Estoque Baixo
    let qtdDisplay = `<span class="fw-bold">${item.quantidade} un</span>`;
    if (item.quantidade < 15) {
      qtdDisplay = `<span class="text-danger fw-bold"><i class="bi bi-arrow-down-circle me-1"></i>${item.quantidade} un</span>`;
    }

    const precoFormatado = new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(item.preco_unitario);

    tr.innerHTML = `
                <td class="ps-4">
                    <div class="fw-bold text-dark">${
                      item.nome_medicamento
                    }</div>
                    <div class="small text-muted">${
                      item.fabricante || "Genérico"
                    }</div>
                </td>
                <td>
                    <div class="small text-dark">${item.nome_fornecedor}</div>
                    <div class="small text-muted" style="font-size: 0.75rem;">CNPJ: ${
                      item.cnpj_fornecedor
                    }</div>
                </td>
                <td>${badgeValidade}</td>
                <td>${qtdDisplay}</td>
                <td>${precoFormatado}</td>
                <td class="text-end pe-4">
                    <button class="btn btn-sm btn-outline-primary border-0 me-1" onclick="abrirModalConsumo(${
                      item.id_estoque_medicamento
                    })" title="Registrar Saída">
                        <i class="bi bi-box-arrow-down-left"></i>
                    </button>
                    ${USER_ROLE !== 'enfermeiro' ? `
                    <button class="btn btn-sm btn-outline-danger border-0" onclick="deletarItem(${
                      item.id_estoque_medicamento
                    })" title="Excluir Lote">
                        <i class="bi bi-trash"></i>
                    </button>` : ''}
                </td>
            `;
    tbody.appendChild(tr);
  });
}

function atualizarKPIs(lista) {
  const hoje = new Date();

  // Calcular totais
  let valorTotal = 0;
  let estoqueBaixo = 0;
  let vencidos = 0;

  lista.forEach((item) => {
    valorTotal += item.preco_unitario * item.quantidade;
    if (item.quantidade < 15) estoqueBaixo++;
    if (item.data_validade_obj < hoje) vencidos++;
  });

  // Atualizar DOM com animação simples (apenas texto)
  document.getElementById("kpi-valor-total").textContent =
    new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(valorTotal);
  document.getElementById("kpi-estoque-baixo").textContent = estoqueBaixo;
  document.getElementById("kpi-vencidos").textContent = vencidos;

  // Alerta de vencidos se houver
  const alertaContainer = document.getElementById("alerta-vencidos-container");
  if (vencidos > 0) {
    alertaContainer.innerHTML = `
            <div class="alert alert-danger d-flex align-items-center shadow-sm border-0 mb-4" role="alert">
                <i class="bi bi-exclamation-triangle-fill fs-4 me-3"></i>
                <div>
                    <strong>Ação Necessária!</strong>
                    <div class="small">Existem ${vencidos} lotes vencidos que precisam ser descartados.</div>
                </div>
            </div>
        `;
  } else {
    alertaContainer.innerHTML = "";
  }
}

// Filtro de Busca
document.getElementById("input-busca").addEventListener("keyup", (e) => {
  const termo = e.target.value.toLowerCase();
  const filtrados = listaEstoqueGlobal.filter(
    (item) =>
      item.nome_medicamento.toLowerCase().includes(termo) ||
      item.fabricante.toLowerCase().includes(termo) ||
      item.nome_fornecedor.toLowerCase().includes(termo)
  );
  renderizarTabela(filtrados);
});

// Funções do Modal de Consumo
function abrirModalConsumo(id) {
  document.getElementById("id_consumo").value = id;
  document.getElementById("qtd_consumo").value = 1;
  new bootstrap.Modal(document.getElementById("modalConsumir")).show();
}

function ajustarQtd(delta) {
  const input = document.getElementById("qtd_consumo");
  let val = parseInt(input.value) || 0;
  val += delta;
  if (val < 1) val = 1;
  input.value = val;
}

async function confirmarConsumo() {
  const id = document.getElementById("id_consumo").value;
  const qtd = parseInt(document.getElementById("qtd_consumo").value);

  if (qtd <= 0) return Swal.fire('Atenção', "Quantidade inválida.", 'warning');

  try {
    await API.post(`/estoque/${id}/consumir`, { quantidade: qtd });

    // Fechar modal
    bootstrap.Modal.getInstance(
      document.getElementById("modalConsumir")
    ).hide();

    // Feedback visual e recarga
    Swal.fire('Sucesso', "Saída registrada com sucesso!", 'success');
    carregarEstoque();
  } catch (error) {
    Swal.fire('Erro', "Erro ao registrar saída: " + error.message, 'error');
  }
}

async function deletarItem(id) {
  const result = await Swal.fire({
      title: 'Tem certeza?',
      text: "Deseja remover este lote do estoque permanentemente?",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Sim, remover!',
      cancelButtonText: 'Cancelar'
  });

  if (result.isConfirmed) {
    try {
      await API.delete(`/estoque/${id}`);
      carregarEstoque();
      Swal.fire('Removido!', 'O lote foi removido do estoque.', 'success');
    } catch (error) {
      Swal.fire('Erro', "Erro ao deletar: " + error.message, 'error');
    }
  }
}

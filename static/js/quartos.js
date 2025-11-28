document.addEventListener("DOMContentLoaded", () => {
  carregarMapaLeitos();
});

async function carregarMapaLeitos() {
  const container = document.getElementById("grid-quartos");

  try {
    // Busca quartos e internações ativas simultaneamente
    // Precisamos das internações para saber o ID da internação ao dar alta
    const [quartos, internacoes] = await Promise.all([
      API.get("/quartos/mapa"),
      API.get("/internacoes/ativas"),
    ]);

    // 1. Calcular KPIs (Indicadores do Topo)
    const total = quartos.length;
    const ocupados = quartos.filter((q) => q.status_atual === "Ocupado").length;
    const livres = total - ocupados;

    atualizarKPIs(total, livres, ocupados);

    // 2. Renderizar Cards
    container.innerHTML = ""; // Limpa o loading

    if (total === 0) {
      container.innerHTML =
        '<div class="col-12 text-center text-muted">Nenhum quarto cadastrado.</div>';
      return;
    }

    quartos.forEach((quarto) => {
      const isOcupado = quarto.status_atual === "Ocupado";

      // Encontra a internação correspondente a este quarto (se ocupado)
      // O backend retorna id_quarto ou num_quarto dependendo da view, ajustamos aqui para garantir
      const internacao = isOcupado
        ? internacoes.find(
            (i) =>
              i.id_quarto == quarto.id_quarto ||
              i.id_quarto == quarto.num_quarto
          )
        : null;

      // Definições visuais baseadas no status
      const statusColor = isOcupado ? "danger" : "success";
      const statusIcon = isOcupado
        ? "bi-person-x-fill"
        : "bi-check-circle-fill";
      const statusText = isOcupado ? "Ocupado" : "Disponível";

      // Ícone do tipo de quarto (Individual, Duplo, etc)
      let typeIcon = "bi-hospital";
      if (quarto.tipo_de_quarto.toLowerCase().includes("individual"))
        typeIcon = "bi-person";
      if (quarto.tipo_de_quarto.toLowerCase().includes("duplo"))
        typeIcon = "bi-people";

      // Formatar Moeda
      const valorFormatado = new Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: "BRL",
      }).format(quarto.valor_diaria);

      // Conteúdo Principal do Card
      const infoPrincipal = isOcupado
        ? `<div class="text-truncate fw-bold text-dark" title="${
            quarto.paciente_atual
          }">
                     <i class="bi bi-person-wheelchair text-muted me-1"></i> ${
                       quarto.paciente_atual || "Paciente"
                     }
                   </div>`
        : `<div class="text-success fw-bold">
                     ${valorFormatado} <span class="text-muted small fw-normal">/ dia</span>
                   </div>`;

      // Botão de Ação (Dar Alta ou Internar)
      let actionBtn = "";
      if (isOcupado && internacao) {
        actionBtn = `
                    <button class="btn btn-sm btn-outline-danger w-100 mt-2" onclick="darAlta(${internacao.id_internacao})">
                        <i class="bi bi-box-arrow-right"></i> Registrar Alta
                    </button>
                `;
      } else if (isOcupado && !internacao) {
        // Caso raro: Está ocupado na view, mas não achou a internação ativa (ex: erro de integridade)
        actionBtn = `<button class="btn btn-sm btn-secondary w-100 mt-2" disabled>Erro: S/ Internação</button>`;
      } else {
        actionBtn = `
                    <a href="/ui/internacoes/nova" class="btn btn-sm btn-outline-success w-100 mt-2">
                        <i class="bi bi-plus-lg"></i> Internar
                    </a>
                 `;
      }

      const card = `
                <div class="col-xl-3 col-lg-4 col-md-6">
                    <div class="card h-100 border-0 shadow-sm position-relative overflow-hidden">
                        <div class="position-absolute top-0 start-0 bottom-0 bg-${statusColor}" style="width: 4px;"></div>

                        <div class="card-body ps-4">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <h5 class="card-title mb-0 text-dark">Quarto ${quarto.num_quarto}</h5>
                                <span class="badge bg-${statusColor} bg-opacity-10 text-${statusColor} rounded-pill px-2">
                                    <i class="bi ${statusIcon} me-1"></i> ${statusText}
                                </span>
                            </div>

                            <p class="text-muted small mb-3">
                                <i class="bi ${typeIcon} me-1"></i> ${quarto.tipo_de_quarto}
                            </p>

                            <div class="mt-3 pt-3 border-top border-light">
                                ${infoPrincipal}
                                ${actionBtn}
                            </div>
                        </div>
                    </div>
                </div>
            `;
      container.innerHTML += card;
    });
  } catch (error) {
    console.error(error);
    container.innerHTML = `
            <div class="col-12 text-center text-danger py-4">
                <i class="bi bi-exclamation-triangle fs-1"></i>
                <p class="mt-2">Erro ao carregar o mapa de leitos.</p>
                <small class="text-muted">${error.message}</small>
            </div>`;
  }
}

async function darAlta(idInternacao) {
  if (
    confirm("Confirmar alta médica para este paciente? O quarto será liberado.")
  ) {
    try {
      // Pega a data de hoje no formato YYYY-MM-DD
      const dataHoje = new Date().toISOString().split("T")[0];

      await API.post(`/internacoes/${idInternacao}/alta`, {
        data_alta_efetiva: dataHoje,
      });

      alert("Alta registrada com sucesso!");
      carregarMapaLeitos(); // Recarrega a tela para atualizar o status
    } catch (error) {
      alert("Erro ao dar alta: " + error.message);
    }
  }
}

function atualizarKPIs(total, livres, ocupados) {
  const elTotal = document.getElementById("kpi-total");
  const elLivres = document.getElementById("kpi-livres");
  const elOcupados = document.getElementById("kpi-ocupados");

  if (elTotal) elTotal.textContent = total;
  if (elLivres) elLivres.textContent = livres;
  if (elOcupados) elOcupados.textContent = ocupados;
}

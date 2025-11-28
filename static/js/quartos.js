document.addEventListener("DOMContentLoaded", () => {
  carregarMapaLeitos();
});

async function carregarMapaLeitos() {
  const container = document.getElementById("grid-quartos");

  try {
    const quartos = await API.get("/quartos/mapa");

    // 1. Calcular KPIs (Indicadores)
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

      // Conteúdo condicional (Nome do paciente ou Preço)
      const infoPrincipal = isOcupado
        ? `<div class="text-truncate fw-bold text-dark" title="${quarto.paciente_atual}">
                     <i class="bi bi-person-wheelchair text-muted me-1"></i> ${quarto.paciente_atual}
                   </div>`
        : `<div class="text-success fw-bold">
                     ${valorFormatado} <span class="text-muted small fw-normal">/ dia</span>
                   </div>`;

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
            </div>`;
  }
}

function atualizarKPIs(total, livres, ocupados) {
  // Animação simples dos números
  document.getElementById("kpi-total").textContent = total;
  document.getElementById("kpi-livres").textContent = livres;
  document.getElementById("kpi-ocupados").textContent = ocupados;
}

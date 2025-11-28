document.addEventListener("DOMContentLoaded", () => {
  carregarMapaLeitos();
});

async function carregarMapaLeitos() {
  const container = document.getElementById("grid-quartos");

  try {
    // Agora só precisamos chamar o mapa, pois ele já traz o ID da internação (graças à correção no Repository)
    const quartos = await API.get("/quartos/mapa");

    // 1. Calcular KPIs
    const total = quartos.length;
    const ocupados = quartos.filter((q) => q.status_atual === "Ocupado").length;
    const livres = total - ocupados;

    atualizarKPIs(total, livres, ocupados);

    // 2. Renderizar Cards
    container.innerHTML = "";

    if (total === 0) {
      container.innerHTML =
        '<div class="col-12 text-center text-muted">Nenhum quarto cadastrado.</div>';
      return;
    }

    quartos.forEach((quarto) => {
      const isOcupado = quarto.status_atual === "Ocupado";

      // Definições visuais
      const statusColor = isOcupado ? "danger" : "success";
      const statusIcon = isOcupado
        ? "bi-person-x-fill"
        : "bi-check-circle-fill";
      const statusText = isOcupado ? "Ocupado" : "Disponível";

      let typeIcon = "bi-hospital";
      if (quarto.tipo_de_quarto.toLowerCase().includes("individual"))
        typeIcon = "bi-person";
      if (quarto.tipo_de_quarto.toLowerCase().includes("duplo"))
        typeIcon = "bi-people";

      const valorFormatado = new Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: "BRL",
      }).format(quarto.valor_diaria);

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

      // LÓGICA DO BOTÃO DE AÇÃO CORRIGIDA
      let actionBtn = "";
      if (isOcupado) {
        // Se está ocupado, o id_internacao deve vir da query do Repository
        if (quarto.id_internacao) {
          actionBtn = `
                <button class="btn btn-sm btn-outline-danger w-100 mt-2" onclick="darAlta(${quarto.id_internacao})">
                    <i class="bi bi-box-arrow-right"></i> Registrar Alta
                </button>
            `;
        } else {
          // Fallback caso algo dê errado no banco
          actionBtn = `<button class="btn btn-sm btn-secondary w-100 mt-2" disabled>Erro de Dados</button>`;
        }
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
        </div>`;
      container.innerHTML += card;
    });
  } catch (error) {
    console.error(error);
    container.innerHTML = `<div class="col-12 text-center text-danger">Erro ao carregar mapa: ${error.message}</div>`;
  }
}

async function darAlta(idInternacao) {
  if (confirm("Confirmar alta médica? O quarto será liberado.")) {
    try {
      // Usa data local YYYY-MM-DD para evitar problemas de fuso horário
      const hoje = new Date();
      const ano = hoje.getFullYear();
      const mes = String(hoje.getMonth() + 1).padStart(2, "0");
      const dia = String(hoje.getDate()).padStart(2, "0");
      const dataHoje = `${ano}-${mes}-${dia}`;

      await API.post(`/internacoes/${idInternacao}/alta`, {
        data_alta_efetiva: dataHoje,
      });

      alert("Alta registrada com sucesso!");
      carregarMapaLeitos();
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

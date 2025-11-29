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

      // Botão de Editar (Pequeno, no topo)
      const editBtn = `
        <button class="btn btn-sm btn-link text-muted p-0 position-absolute top-0 end-0 mt-2 me-2" 
                onclick="abrirModalEditarQuarto(${quarto.num_quarto}, '${quarto.tipo_de_quarto}', ${quarto.valor_diaria})">
            <i class="bi bi-pencil-square"></i>
        </button>
      `;

      const card = `
        <div class="col-xl-3 col-lg-4 col-md-6">
            <div class="card h-100 border-0 shadow-sm position-relative overflow-hidden">
                ${editBtn}
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

async function criarQuarto() {
  const num_quarto = document.getElementById("num_quarto").value;
  const tipo_de_quarto = document.getElementById("tipo_de_quarto").value;
  const valor_diaria = document.getElementById("valor_diaria").value;
  const isEdit = document.getElementById("is_edit_quarto").value === 'true';

  if (!num_quarto || !tipo_de_quarto || !valor_diaria) {
    alert("Preencha todos os campos!");
    return;
  }
  
  if (parseInt(num_quarto) <= 0) return alert("Número do quarto inválido.");
  if (parseFloat(valor_diaria) <= 0) return alert("Valor da diária deve ser positivo.");

  try {
    if (isEdit) {
        await API.put(`/quartos/${num_quarto}`, {
            tipo_de_quarto: tipo_de_quarto,
            valor_diaria: valor_diaria,
        });
        alert("Quarto atualizado com sucesso!");
    } else {
        await API.post("/quartos/", {
            num_quarto: num_quarto,
            tipo_de_quarto: tipo_de_quarto,
            valor_diaria: valor_diaria,
        });
        alert("Quarto criado com sucesso!");
    }
    
    // Fechar modal e recarregar
    const modal = bootstrap.Modal.getInstance(document.getElementById('modalNovoQuarto'));
    modal.hide();
    document.getElementById("formNovoQuarto").reset();
    document.getElementById("is_edit_quarto").value = 'false';
    document.getElementById("num_quarto").readOnly = false;
    carregarMapaLeitos();
  } catch (error) {
    alert("Erro ao salvar quarto: " + error.message);
  }
}

function abrirModalEditarQuarto(num, tipo, valor) {
    document.getElementById("num_quarto").value = num;
    document.getElementById("tipo_de_quarto").value = tipo;
    document.getElementById("valor_diaria").value = valor;
    document.getElementById("is_edit_quarto").value = 'true';
    document.getElementById("num_quarto").readOnly = true;
    
    const modal = new bootstrap.Modal(document.getElementById('modalNovoQuarto'));
    modal.show();
}

function atualizarKPIs(total, livres, ocupados) {
  const elTotal = document.getElementById("kpi-total");
  const elLivres = document.getElementById("kpi-livres");
  const elOcupados = document.getElementById("kpi-ocupados");
  if (elTotal) elTotal.textContent = total;
  if (elLivres) elLivres.textContent = livres;
  if (elOcupados) elOcupados.textContent = ocupados;
}

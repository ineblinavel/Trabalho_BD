// Variável para controle de auto-save
let autoSaveInterval;
let listaPrescricao = [];

document.addEventListener("DOMContentLoaded", async () => {
  const dataElement = document.getElementById("medico-data");
  if (!dataElement) return;

  const crm = dataElement.dataset.crm;

  if (!crm || crm === "None") {
    const container = document.getElementById("agenda-container");
    if (container) {
      container.innerHTML = `
            <div class="text-center py-5">
                <i class="bi bi-exclamation-circle text-warning icon-lg mb-3"></i>
                <p class="text-muted">CRM não identificado na sessão. Por favor, faça login novamente.</p>
            </div>
        `;
    }
    return;
  }

  await carregarAgenda(crm);
  await carregarConsultas(crm);

  carregarTiposExame();
  carregarPacientesSelect();
  carregarMedicosSelect();
});

/* ================== AGENDA MÉDICA ================== */

async function carregarAgenda(crm) {
  const container = document.getElementById("agenda-container");
  if (!container) return;

  try {
    const agendas = await API.get(`/agenda/medico/${crm}`);

    if (agendas.length === 0) {
      container.innerHTML = `
                <div class="text-center py-5">
                    <i class="bi bi-calendar-x text-muted icon-lg mb-3"></i>
                    <p class="text-muted">Nenhuma agenda configurada para este CRM.</p>
                </div>
            `;
      container.classList.remove("bg-light", "border", "border-dashed");
      return;
    }

    let html = '<div class="list-group list-group-flush text-start">';

    agendas.forEach((agenda) => {
      const dataFmt = new Date(agenda.data).toLocaleDateString("pt-BR", {
        timeZone: "UTC",
      });
      html += `
                <div class="list-group-item py-3">
                    <div class="d-flex w-100 justify-content-between align-items-center">
                        <div>
                            <h5 class="mb-1"><i class="bi bi-calendar-date me-2 text-primary"></i>${dataFmt}</h5>
                            <small class="text-muted">
                                <i class="bi bi-clock me-1"></i>${agenda.inicio_platao} às ${agenda.fim_platao}
                            </small>
                        </div>
                        <span class="badge bg-light text-dark border">
                            ${agenda.duracao_slot_minutos} min/consulta
                        </span>
                    </div>
                    <div class="mt-2">
                        <small class="text-primary cursor-pointer fw-bold" onclick="verSlots(${agenda.id_agenda})" style="cursor: pointer;">
                            <i class="bi bi-eye me-1"></i> Ver horários disponíveis
                        </small>
                    </div>
                    <div id="slots-${agenda.id_agenda}" class="mt-3 d-none p-3 bg-light rounded"></div>
                </div>
            `;
    });
    html += "</div>";

    container.innerHTML = html;
    container.classList.remove(
      "text-center",
      "py-5",
      "bg-light",
      "border",
      "border-dashed"
    );
  } catch (error) {
    console.error(error);
    container.innerHTML = `
            <div class="text-center py-5 text-danger">
                <p>Erro ao carregar agenda: ${error.message}</p>
            </div>
        `;
  }
}

async function verSlots(idAgenda) {
  const container = document.getElementById(`slots-${idAgenda}`);

  if (!container.classList.contains("d-none")) {
    container.classList.add("d-none");
    return;
  }

  container.innerHTML =
    '<div class="spinner-border spinner-border-sm text-primary"></div> Carregando...';
  container.classList.remove("d-none");

  try {
    const slots = await API.get(`/agenda/${idAgenda}/slots`);

    if (slots.length === 0) {
      container.innerHTML =
        '<small class="text-muted fst-italic">Nenhum horário livre neste plantão.</small>';
      return;
    }

    let badges = "";
    slots.forEach((slot) => {
      const hora = slot.substring(0, 5);
      badges += `<span class="badge bg-success me-2 mb-2 p-2">${hora}</span>`;
    });

    container.innerHTML = `
            <h6 class="small fw-bold text-muted mb-2">Horários Livres:</h6>
            <div class="d-flex flex-wrap">${badges}</div>
        `;
  } catch (error) {
    container.innerHTML =
      '<small class="text-danger">Erro ao carregar slots.</small>';
  }
}

// Handler do formulário de Criar Nova Agenda
const formAgenda = document.getElementById("form-agenda");
if (formAgenda) {
  formAgenda.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Pega o CRM da sessão (que está no HTML)
    const crm = document.getElementById("medico-data").dataset.crm;
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    // Monta o payload conforme esperado pelo AgendamedicoRoutes.py
    const payload = {
      crm_medico: crm,
      data: data.data,
      inicio_platao: data.inicio_platao + ":00", // Backend requer HH:MM:SS
      fim_platao: data.fim_platao + ":00", // Backend requer HH:MM:SS
      duracao_slot_minutos: parseInt(data.duracao_slot_minutos),
    };

    try {
      // Chama a rota POST /agenda/
      const response = await API.post("/agenda/", payload);

      if (response.error) {
        alert("Erro ao criar agenda: " + response.error);
      } else {
        alert("Plantão configurado com sucesso!");

        // Fecha o modal
        const modalEl = document.getElementById("modalNovoPlantao");
        const modal = bootstrap.Modal.getInstance(modalEl);
        modal.hide();

        // Limpa e Recarrega
        e.target.reset();
        carregarAgenda(crm);
      }
    } catch (error) {
      console.error(error);
      alert("Erro técnico: " + error.message);
    }
  });
}

/* ================== CONSULTAS (FILA DE ESPERA) ================== */

async function carregarConsultas(crm) {
  const container = document.getElementById("consultas-container");
  if (!container) return;

  try {
    const consultas = await API.get(`/consultas/medico/${crm}`);

    if (consultas.length === 0) {
      container.innerHTML = `
                <div class="text-center py-5">
                    <i class="bi bi-emoji-smile text-muted icon-lg mb-3"></i>
                    <p class="text-muted">Nenhuma consulta agendada por enquanto.</p>
                </div>
            `;
      return;
    }

    let html = '<div class="list-group list-group-flush text-start">';
    consultas.forEach((c) => {
      const dataObj = new Date(c.data_hora_agendamento);
      const data = dataObj.toLocaleDateString("pt-BR");
      const hora = dataObj.toLocaleTimeString("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
      });

      let statusBadge = "";
      if (c.status === "C")
        statusBadge = '<span class="badge bg-success ms-2">Concluída</span>';
      else if (c.status === "A")
        statusBadge =
          '<span class="badge bg-warning text-dark ms-2">Agendada</span>';

      let buttons = "";
      if (c.status !== "C") {
        // Passamos também o id_paciente para buscar histórico
        buttons += `
                    <button class="btn btn-sm btn-danger me-2" onclick="abrirModalAtendimento(${
                      c.id_consulta
                    }, '${c.nome_paciente}', '${c.cpf || ""}', ${
          c.id_paciente
        })">
                        <i class="bi bi-clipboard-pulse me-1"></i> Atender
                    </button>
                `;
      }
      buttons += `
                <button class="btn btn-sm btn-outline-primary" onclick="abrirModalExame(${c.id_consulta}, ${c.id_paciente})">
                    <i class="bi bi-file-medical me-1"></i> Exame
                </button>
            `;

      html += `
                <div class="list-group-item px-0 py-3">
                    <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
                        <div>
                            <div class="d-flex align-items-center mb-1">
                                <h6 class="mb-0 fw-bold">${c.nome_paciente}</h6>
                                ${statusBadge}
                            </div>
                            <small class="text-muted">
                                <i class="bi bi-calendar3 me-1"></i>${data}
                                <i class="bi bi-clock ms-2 me-1"></i>${hora}
                            </small>
                        </div>
                        <div class="d-flex">
                            ${buttons}
                        </div>
                    </div>
                </div>
            `;
    });
    html += "</div>";

    container.innerHTML = html;
    container.classList.remove(
      "text-center",
      "py-5",
      "bg-light",
      "border",
      "border-dashed"
    );
  } catch (error) {
    console.error(error);
    container.innerHTML = `<p class="text-danger text-center">Erro ao carregar consultas: ${error.message}</p>`;
  }
}

/* ================== ATENDIMENTO & PRESCRIÇÃO (MELHORADO) ================== */

// Abre o modal, carrega histórico e rascunho
async function abrirModalAtendimento(
  idConsulta,
  nomePaciente,
  cpf,
  idPaciente
) {
  document.getElementById("atend-id-consulta").value = idConsulta;
  document.getElementById("atend-id-paciente").value = idPaciente;
  document.getElementById("atend-paciente-nome").textContent = nomePaciente;
  document.getElementById("atend-paciente-cpf").textContent = `CPF: ${
    cpf || "Não informado"
  }`;

  // Recupera rascunho (Auto-Save)
  const rascunho = localStorage.getItem(`rascunho_consulta_${idConsulta}`);
  if (rascunho) {
    const dados = JSON.parse(rascunho);
    document.getElementById("atend-queixa").value = dados.queixa || "";
    document.getElementById("atend-diagnostico").value =
      dados.diagnostico || "";
  } else {
    document.getElementById("atend-queixa").value = "";
    document.getElementById("atend-diagnostico").value = "";
  }

  // Inicia Auto-Save a cada 10s
  clearInterval(autoSaveInterval);
  autoSaveInterval = setInterval(() => salvarRascunho(idConsulta), 10000);

  listaPrescricao = [];
  renderizarTabelaPrescricao();

  await carregarMedicamentosSelect();
  carregarHistoricoRapido(idPaciente);

  new bootstrap.Modal(document.getElementById("modalAtendimento")).show();
}

function salvarRascunho(idConsulta) {
  const dados = {
    queixa: document.getElementById("atend-queixa").value,
    diagnostico: document.getElementById("atend-diagnostico").value,
  };
  localStorage.setItem(
    `rascunho_consulta_${idConsulta}`,
    JSON.stringify(dados)
  );
}

async function carregarHistoricoRapido(idPaciente) {
  const container = document.getElementById("historico-rapido-container");
  if (!container) return;

  container.innerHTML =
    '<div class="text-center py-3"><div class="spinner-border spinner-border-sm text-primary"></div></div>';

  try {
    const historico = await API.get(`/pacientes/${idPaciente}/historico`);

    if (!historico || historico.length === 0) {
      container.innerHTML =
        '<div class="p-3 text-muted text-center">Nenhum registro anterior encontrado.</div>';
      return;
    }

    let html = "";
    // Mostra os 3 últimos eventos
    historico.slice(0, 3).forEach((evento) => {
      // Ajuste seguro de data
      let dataTexto = "Data inválida";
      if (evento.data_evento) {
        const dataObj = new Date(evento.data_evento);
        if (!isNaN(dataObj)) {
          dataTexto = dataObj.toLocaleDateString("pt-BR");
        }
      }

      const icon = evento.tipo === "Consulta" ? "bi-person-badge" : "bi-flask";

      html += `
                <div class="list-group-item list-group-item-action">
                    <div class="d-flex w-100 justify-content-between">
                        <small class="fw-bold text-primary"><i class="bi ${icon}"></i> ${
        evento.tipo
      }</small>
                        <small class="text-muted">${dataTexto}</small>
                    </div>
                    <p class="mb-1 small text-truncate" title="${
                      evento.descricao
                    }">${evento.descricao || "Sem descrição"}</p>
                    <small class="text-muted fst-italic">Dr(a). ${
                      evento.responsavel
                    }</small>
                </div>
            `;
    });
    container.innerHTML = html;
  } catch (error) {
    container.innerHTML =
      '<div class="p-3 text-danger text-center small">Erro ao carregar histórico.</div>';
  }
}

async function carregarMedicamentosSelect() {
  const select = document.getElementById("presc-medicamento");
  if (!select || select.options.length > 1) return;

  try {
    const meds = await API.get("/medicamentos/");
    select.innerHTML =
      '<option value="" disabled selected>Selecione...</option>';
    meds.forEach((m) => {
      select.innerHTML += `<option value="${m.id_medicamento}">${
        m.nome_comercial
      } (${m.fabricante || "Genérico"})</option>`;
    });
  } catch (e) {
    console.error("Erro ao carregar medicamentos", e);
    select.innerHTML = "<option disabled>Erro ao carregar lista</option>";
  }
}

function adicionarItemPrescricao() {
  const select = document.getElementById("presc-medicamento");
  const idMed = select.value;
  const nomeMed = select.options[select.selectedIndex]?.text;
  const qtd = document.getElementById("presc-qtd").value;
  const uso = document.getElementById("presc-uso").value;

  if (!idMed) return alert("Selecione um medicamento.");
  if (qtd <= 0) return alert("Quantidade inválida.");
  if (!uso) return alert("Informe a dosagem/frequência.");

  listaPrescricao.push({
    id_medicamento: parseInt(idMed),
    nome: nomeMed,
    quantidade_prescrita: parseInt(qtd),
    frequencia_uso: uso,
    dosagem: uso,
  });

  renderizarTabelaPrescricao();

  select.value = "";
  document.getElementById("presc-qtd").value = 1;
  document.getElementById("presc-uso").value = "";
  select.focus();
}

function renderizarTabelaPrescricao() {
  const tbody = document.querySelector("#tabela-prescricao tbody");
  if (!tbody) return;

  tbody.innerHTML = "";

  if (listaPrescricao.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="3" class="text-center text-muted small">Nenhum medicamento prescrito.</td></tr>';
    // Atualiza contador no header do card se existir
    const counter = document.getElementById("presc-count");
    if (counter) counter.textContent = "0 itens";
    return;
  }

  listaPrescricao.forEach((item, index) => {
    tbody.innerHTML += `
            <tr>
                <td><small>${item.nome}</small></td>
                <td>
                    <span class="badge bg-light text-dark border me-1">${item.quantidade_prescrita} un</span>
                    <small>${item.frequencia_uso}</small>
                </td>
                <td class="text-end">
                    <button class="btn btn-sm btn-link text-danger p-0" onclick="removerItemPrescricao(${index})">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        `;
  });

  const counter = document.getElementById("presc-count");
  if (counter) counter.textContent = `${listaPrescricao.length} itens`;
}

function removerItemPrescricao(index) {
  listaPrescricao.splice(index, 1);
  renderizarTabelaPrescricao();
}

async function finalizarAtendimento() {
  const idConsulta = document.getElementById("atend-id-consulta").value;
  const queixa = document.getElementById("atend-queixa").value.trim();
  const diag = document.getElementById("atend-diagnostico").value.trim();

  if (!diag)
    return alert("Por favor, descreva o diagnóstico antes de finalizar.");

  // Combina textos para salvar no campo único do banco
  const diagnosticoCompleto = `[Queixa]: ${queixa} \n\n[Diagnóstico]: ${diag}`;

  // Botão loading (seletor genérico para pegar o botão primário do footer do modal)
  const btnSalvar = document.querySelector(
    "#modalAtendimento .modal-footer .btn-primary"
  );
  let textoOriginal = "Concluir Atendimento";

  if (btnSalvar) {
    textoOriginal = btnSalvar.innerHTML;
    btnSalvar.disabled = true;
    btnSalvar.innerHTML =
      '<span class="spinner-border spinner-border-sm"></span> Salvando...';
  }

  try {
    // 1. Atualiza Consulta
    await API.put(`/consultas/${idConsulta}`, {
      diagnostico: diagnosticoCompleto,
      status: "C",
    });

    // 2. Salva Prescrições (Consumo de estoque é feito pelo Backend)
    for (const item of listaPrescricao) {
      await API.post("/prescricoes/", {
        id_consulta: parseInt(idConsulta),
        id_medicamento: item.id_medicamento,
        quantidade_prescrita: item.quantidade_prescrita,
        dosagem: item.dosagem,
        frequencia_uso: item.frequencia_uso,
      });
    }

    // 3. Limpeza
    localStorage.removeItem(`rascunho_consulta_${idConsulta}`);
    clearInterval(autoSaveInterval);

    alert("Atendimento finalizado com sucesso!");

    // Fecha modal e recarrega
    const modalEl = document.getElementById("modalAtendimento");
    if (modalEl) {
      const modal = bootstrap.Modal.getInstance(modalEl);
      if (modal) modal.hide();
    }
    location.reload();
  } catch (e) {
    console.error(e);
    alert("Erro ao finalizar atendimento: " + (e.message || e.error));
    if (btnSalvar) {
      btnSalvar.disabled = false;
      btnSalvar.innerHTML = textoOriginal;
    }
  }
}

/* ================== SOLICITAÇÃO DE EXAMES ================== */

async function carregarTiposExame() {
  const select = document.getElementById("tipo_exame_select");
  if (!select) return;

  try {
    const tipos = await API.get("/tipos-exame/");
    select.innerHTML =
      '<option value="" selected disabled>Selecione um exame...</option>';
    tipos.forEach((t) => {
      select.innerHTML += `<option value="${t.id_tipo_exame}">${t.nome_do_exame}</option>`;
    });
  } catch (e) {
    console.error("Erro ao carregar tipos de exame", e);
  }
}

async function carregarPacientesSelect() {
  const select = document.getElementById("solicitacao_paciente");
  if (!select) return;

  try {
    const pacientes = await API.get("/pacientes/");
    select.innerHTML =
      '<option value="" selected disabled>Selecione um paciente...</option>';
    pacientes.forEach((p) => {
      select.innerHTML += `<option value="${p.id_paciente}">${p.nome_paciente} (CPF: ${p.cpf})</option>`;
    });
  } catch (e) {
    console.error("Erro ao carregar pacientes", e);
  }
}

async function carregarMedicosSelect() {
  const select = document.getElementById("solicitacao_medico");
  if (!select) return;

  try {
    const medicos = await API.get("/medicos/medicos");
    const dataEl = document.getElementById("medico-data");
    const currentCrm = dataEl ? dataEl.dataset.crm : null;

    select.innerHTML =
      '<option value="" selected disabled>Selecione um médico...</option>';
    medicos.forEach((m) => {
      const selected = m.crm === currentCrm ? "selected" : "";
      select.innerHTML += `<option value="${m.crm}" ${selected}>${m.nome_medico}</option>`;
    });
  } catch (e) {
    console.error("Erro ao carregar médicos", e);
  }
}

function abrirModalExame(idConsulta = null, idPaciente = null) {
  document.getElementById("id_consulta_exame").value = idConsulta || "";
  const tipoSelect = document.getElementById("tipo_exame_select");
  if (tipoSelect) tipoSelect.value = "";

  const dataInput = document.getElementById("solicitacao_data");
  if (dataInput) dataInput.valueAsDate = new Date();

  const selectPac = document.getElementById("solicitacao_paciente");
  if (selectPac) {
    if (idPaciente) {
      selectPac.value = idPaciente;
      // Opcional: desabilitar se já veio preenchido
      // selectPac.disabled = true;
    } else {
      selectPac.value = "";
      selectPac.disabled = false;
    }
  }

  new bootstrap.Modal(document.getElementById("modalSolicitarExame")).show();
}

async function confirmarSolicitacaoExame() {
  const idPaciente = document.getElementById("solicitacao_paciente").value;
  const idTipo = document.getElementById("tipo_exame_select").value;
  const dataSolicitacao = document.getElementById("solicitacao_data").value;
  const crm = document.getElementById("solicitacao_medico").value;

  if (!idPaciente) return alert("Selecione um paciente.");
  if (!idTipo) return alert("Selecione um tipo de exame.");
  if (!crm) return alert("Selecione o médico responsável.");
  if (!dataSolicitacao) return alert("Informe a data da solicitação.");

  const payload = {
    status: "A",
    crm_medico_responsavel: crm,
    data_solicitacao: dataSolicitacao,
    id_paciente: parseInt(idPaciente),
    id_tipo_exame: parseInt(idTipo),
  };

  try {
    await API.post("/exames/", payload);
    alert("Exame solicitado com sucesso!");

    const modalEl = document.getElementById("modalSolicitarExame");
    const modalInstance = bootstrap.Modal.getInstance(modalEl);
    modalInstance.hide();
  } catch (error) {
    console.error(error);
    alert("Erro ao solicitar exame: " + (error.error || error.message));
  }
}

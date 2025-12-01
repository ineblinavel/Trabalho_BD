document.addEventListener("DOMContentLoaded", async () => {
  const crm = document.getElementById("medico-data").dataset.crm;

  if (!crm || crm === "None") {
    document.getElementById("agenda-container").innerHTML = `
            <div class="text-center py-5">
                <i class="bi bi-exclamation-circle text-warning icon-lg mb-3"></i>
                <p class="text-muted">CRM não identificado na sessão. Por favor, faça login novamente.</p>
            </div>
        `;
    return;
  }

  await carregarAgenda(crm);
  await carregarConsultas(crm);

  carregarTiposExame();
  carregarPacientesSelect();
  carregarMedicosSelect();
});

async function carregarAgenda(crm) {
  const container = document.getElementById("agenda-container");

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

async function carregarConsultas(crm) {
  const container = document.getElementById("consultas-container");
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
        buttons += `
                    <button class="btn btn-sm btn-danger me-2" onclick="abrirModalAtendimento(${
                      c.id_consulta
                    }, '${c.nome_paciente}', '${c.cpf || ""}')">
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

async function carregarTiposExame() {
  try {
    const tipos = await API.get("/tipos-exame/");
    const select = document.getElementById("tipo_exame_select");
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
  try {
    const pacientes = await API.get("/pacientes/");
    const select = document.getElementById("solicitacao_paciente");
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
  try {
    const medicos = await API.get("/medicos/medicos");
    const select = document.getElementById("solicitacao_medico");
    const currentCrm = document.getElementById("medico-data").dataset.crm;

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
  document.getElementById("tipo_exame_select").value = "";
  document.getElementById("solicitacao_data").valueAsDate = new Date();

  const selectPac = document.getElementById("solicitacao_paciente");
  if (idPaciente) {
    selectPac.value = idPaciente;
  } else {
    selectPac.value = "";
    selectPac.disabled = false;
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

/* ================== ATENDIMENTO & PRESCRIÇÃO ================== */

let listaPrescricao = [];

async function abrirModalAtendimento(idConsulta, nomePaciente, cpf) {
  document.getElementById("atend-id-consulta").value = idConsulta;
  document.getElementById("atend-paciente-nome").textContent = nomePaciente;
  document.getElementById("atend-paciente-cpf").textContent = `CPF: ${
    cpf || "Não informado"
  }`;
  document.getElementById("atend-diagnostico").value = "";

  listaPrescricao = [];
  renderizarTabelaPrescricao();
  await carregarMedicamentosSelect();

  new bootstrap.Modal(document.getElementById("modalAtendimento")).show();
}

async function carregarMedicamentosSelect() {
  const select = document.getElementById("presc-medicamento");
  if (select.options.length > 1) return;

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
  tbody.innerHTML = "";

  if (listaPrescricao.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="3" class="text-center text-muted small">Nenhum medicamento prescrito.</td></tr>';
    return;
  }

  listaPrescricao.forEach((item, index) => {
    tbody.innerHTML += `
            <tr>
                <td>${item.nome}</td>
                <td>
                    <span class="badge bg-light text-dark border me-1">${item.quantidade_prescrita} un</span>
                    ${item.frequencia_uso}
                </td>
                <td class="text-end">
                    <button class="btn btn-sm btn-link text-danger p-0" onclick="removerItemPrescricao(${index})">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        `;
  });
}

function removerItemPrescricao(index) {
  listaPrescricao.splice(index, 1);
  renderizarTabelaPrescricao();
}

async function finalizarAtendimento() {
  const idConsulta = document.getElementById("atend-id-consulta").value;
  const diagnostico = document.getElementById("atend-diagnostico").value.trim();

  if (!diagnostico)
    return alert("Por favor, descreva o diagnóstico antes de finalizar.");

  const btnSalvar = document.querySelector("#modalAtendimento .btn-danger");
  const textoOriginal = btnSalvar.innerHTML;
  btnSalvar.disabled = true;
  btnSalvar.innerHTML =
    '<span class="spinner-border spinner-border-sm"></span> Salvando...';

  try {
    await API.put(`/consultas/${idConsulta}`, {
      diagnostico: diagnostico,
      status: "C",
    });

    for (const item of listaPrescricao) {
      await API.post("/prescricoes/", {
        id_consulta: parseInt(idConsulta),
        id_medicamento: item.id_medicamento,
        quantidade_prescrita: item.quantidade_prescrita,
        dosagem: item.dosagem,
        frequencia_uso: item.frequencia_uso,
      });
    }

    alert("Atendimento finalizado com sucesso!");

    bootstrap.Modal.getInstance(
      document.getElementById("modalAtendimento")
    ).hide();
    location.reload();
  } catch (e) {
    console.error(e);
    alert("Erro ao finalizar atendimento: " + e.message);
    btnSalvar.disabled = false;
    btnSalvar.innerHTML = textoOriginal;
  }
}

document.getElementById("form-agenda").addEventListener("submit", async (e) => {
  e.preventDefault();

  // Pega o CRM que já está na página
  const crm = document.getElementById("medico-data").dataset.crm;

  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData.entries());

  // Adiciona o CRM e formata os segundos para o backend (HH:MM:00)
  const payload = {
    crm_medico: crm,
    data: data.data,
    inicio_platao: data.inicio_platao + ":00", // Backend espera HH:MM:SS
    fim_platao: data.fim_platao + ":00", // Backend espera HH:MM:SS
    duracao_slot_minutos: parseInt(data.duracao_slot_minutos),
  };

  try {
    // Chama a rota POST definida em agendamedico_routes.py
    const response = await API.post("/agenda/", payload);

    if (response.error) {
      alert("Erro: " + response.error);
    } else {
      alert("Plantão configurado com sucesso!");

      // Fecha o modal
      const modalElement = document.getElementById("modalNovoPlantao");
      const modal = bootstrap.Modal.getInstance(modalElement);
      modal.hide();

      // Limpa o form e recarrega a lista
      e.target.reset();
      carregarAgenda(crm);
    }
  } catch (error) {
    console.error(error);
    alert("Erro ao salvar agenda. Verifique se já existe plantão nesta data.");
  }
});

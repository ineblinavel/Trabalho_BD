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
  await carregarExames(crm);
  await carregarNomeMedico(crm);

  carregarTiposExame();
  carregarPacientesSelect();
  carregarMedicosSelect();

  // Search Listener
  const searchInput = document.getElementById("search-exames");
  if (searchInput) {
    searchInput.addEventListener("keyup", (e) => {
      filtrarExames(e.target.value);
    });
  }
});

function formatarNomeMedico(nome) {
  if (!nome) return "...";
  if (nome.startsWith("Dr. ") || nome.startsWith("Dra. ")) {
    return nome;
  }
  return `Dr(a). ${nome}`;
}

async function carregarNomeMedico(crm) {
  try {
    const medico = await API.get(`/medicos/${crm}`);
    const headerTitle = document.querySelector("h1.h3.mb-1");
    if (headerTitle && medico.nome_medico) {
      headerTitle.textContent = `Portal Médico - ${formatarNomeMedico(
        medico.nome_medico
      )}`;
    }
  } catch (e) {
    console.error("Erro ao carregar nome do médico", e);
  }
}

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

/* ================== CONSULTAS (FILA DE ESPERA & HISTÓRICO) ================== */

async function carregarConsultas(crm) {
  const containerFila = document.getElementById("consultas-container");
  const containerHist = document.getElementById("historico-container");

  if (!containerFila && !containerHist) return;

  try {
    const consultas = await API.get(`/consultas/medico/${crm}`);

    // Separação: Fila (Agendada/Outros) vs Histórico (Concluída)
    const fila = consultas.filter((c) => c.status !== "C");
    const historico = consultas.filter((c) => c.status === "C");

    // Renderiza Fila de Espera
    if (containerFila) {
      if (fila.length === 0) {
        containerFila.innerHTML = `
                <div class="text-center py-5">
                    <i class="bi bi-emoji-smile text-muted icon-lg mb-3"></i>
                    <p class="text-muted">Nenhuma consulta pendente.</p>
                </div>
            `;
        containerFila.classList.add("bg-light", "border", "border-dashed");
      } else {
        containerFila.innerHTML = renderizarListaConsultas(fila, true);
        containerFila.classList.remove(
          "text-center",
          "py-5",
          "bg-light",
          "border",
          "border-dashed"
        );
      }
    }

    // Renderiza Histórico
    if (containerHist) {
      if (historico.length === 0) {
        containerHist.innerHTML = `
                <div class="text-center py-5">
                    <i class="bi bi-clock-history text-muted icon-lg mb-3"></i>
                    <p class="text-muted">Nenhum atendimento concluído.</p>
                </div>
            `;
        containerHist.classList.add("bg-light", "border", "border-dashed");
      } else {
        containerHist.innerHTML = renderizarListaConsultas(historico, false);
        containerHist.classList.remove(
          "text-center",
          "py-5",
          "bg-light",
          "border",
          "border-dashed"
        );
      }
    }
  } catch (error) {
    console.error(error);
    const erroHtml = `<p class="text-danger text-center">Erro ao carregar consultas: ${error.message}</p>`;
    if (containerFila) containerFila.innerHTML = erroHtml;
    if (containerHist) containerHist.innerHTML = erroHtml;
  }
}

function renderizarListaConsultas(lista, isFila) {
  let html = '<div class="list-group list-group-flush text-start">';
  lista.forEach((c) => {
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
    let prescricoesHtml = "";

    if (isFila) {
      buttons += `
            <button class="btn btn-sm btn-danger me-2" onclick="abrirModalAtendimento(${
              c.id_consulta
            }, '${c.nome_paciente}', '${c.cpf || ""}', ${c.id_paciente})">
                <i class="bi bi-clipboard-pulse me-1"></i> Atender
            </button>
            <button class="btn btn-sm btn-outline-primary" onclick="abrirModalExame(${
              c.id_consulta
            }, ${c.id_paciente})">
                <i class="bi bi-file-medical me-1"></i> Exame
            </button>
        `;
    } else {
      buttons += `
            <button class="btn btn-sm btn-outline-secondary me-2" disabled>
                <i class="bi bi-check2-all me-1"></i> Finalizado
            </button>
            <button class="btn btn-sm btn-outline-primary" onclick="abrirModalEditarPrescricao(${c.id_consulta})">
                <i class="bi bi-pencil me-1"></i> Editar Prescrição
            </button>
          `;
      
      // Renderiza prescrições se houver
      if (c.prescricoes && c.prescricoes.length > 0) {
          prescricoesHtml = `
            <div class="mt-2 pt-2 border-top">
                <small class="fw-bold text-muted"><i class="bi bi-capsule me-1"></i> Prescrição:</small>
                <ul class="list-unstyled mb-0 ms-3 small text-muted">
          `;
          c.prescricoes.forEach(p => {
              prescricoesHtml += `
                <li>
                    • <strong>${p.nome_comercial}</strong> 
                    <span class="fst-italic">(${p.dosagem || 's/d'})</span> - ${p.frequencia_uso || 's/f'}
                </li>`;
          });
          prescricoesHtml += `</ul></div>`;
      }
    }

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
                            ${prescricoesHtml}
                        </div>
                        <div class="d-flex">
                            ${buttons}
                        </div>
                    </div>
                </div>
            `;
  });
  html += "</div>";
  return html;
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

    select.innerHTML = "";
    // select.innerHTML = '<option value="" selected disabled>Selecione um médico...</option>'; // Removido para forçar seleção

    let found = false;
    medicos.forEach((m) => {
      if (m.crm === currentCrm) {
        select.innerHTML += `<option value="${m.crm}" selected>${m.nome_medico}</option>`;
        found = true;
      }
    });

    if (!found) {
      select.innerHTML += `<option value="" selected disabled>Médico logado não encontrado na lista</option>`;
    }

    // Desabilita o select para impedir troca
    select.disabled = true;
  } catch (e) {
    console.error("Erro ao carregar médicos", e);
    select.innerHTML = '<option value="" disabled>Erro ao carregar</option>';
  }
}

/* ================== PLANTÃO RÁPIDO (AUTOMÁTICO) ================== */

// Inicializa o input datetime-local com a data/hora atual
document.addEventListener("DOMContentLoaded", () => {
  const inputAuto = document.getElementById("auto-data-inicio");
  if (inputAuto) {
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset()); // Ajuste fuso
    inputAuto.value = now.toISOString().slice(0, 16);
  }
});

async function criarPlantaoRapido(horasDuracao) {
  const crm = document.getElementById("medico-data").dataset.crm;
  const dataInicioInput = document.getElementById("auto-data-inicio").value;
  const slotMinutos = document.getElementById("auto-slot").value;

  if (!dataInicioInput) return alert("Selecione a data e hora de início.");
  if (!slotMinutos || slotMinutos <= 0)
    return alert("Duração do slot inválida.");

  const inicio = new Date(dataInicioInput);
  const fimTotal = new Date(inicio.getTime() + horasDuracao * 60 * 60 * 1000);

  // Lista de agendas a criar (quebradas por dia)
  const agendasParaCriar = [];

  let cursor = new Date(inicio);

  while (cursor < fimTotal) {
    // Fim do dia atual (23:59:59)
    let fimDoDia = new Date(cursor);
    fimDoDia.setHours(23, 59, 59, 999);

    // O fim deste segmento é o menor entre: fim do dia OU fim total do plantão
    let fimSegmento = fimTotal < fimDoDia ? fimTotal : fimDoDia;

    // Formata para o backend
    const dataStr = cursor.toISOString().split("T")[0];
    const horaInicioStr = cursor.toTimeString().split(" ")[0]; // HH:MM:SS
    const horaFimStr = fimSegmento.toTimeString().split(" ")[0]; // HH:MM:SS

    agendasParaCriar.push({
      crm_medico: crm,
      data: dataStr,
      inicio_platao: horaInicioStr,
      fim_platao: horaFimStr,
      duracao_slot_minutos: parseInt(slotMinutos),
    });

    // Avança o cursor para o início do próximo dia (00:00:00)
    cursor = new Date(fimDoDia.getTime() + 1000); // +1ms vira 00:00:00 do dia seguinte
  }

  if (
    !confirm(
      `Isso criará ${agendasParaCriar.length} registro(s) de agenda para cobrir as ${horasDuracao}h. Confirmar?`
    )
  ) {
    return;
  }

  // Envia requisições em sequência
  let erros = 0;
  for (const agenda of agendasParaCriar) {
    try {
      const response = await API.post("/agenda/", agenda);
      if (response.error) throw new Error(response.error);
    } catch (e) {
      console.error(e);
      erros++;
    }
  }

  if (erros > 0) {
    alert(`Processo finalizado com ${erros} erro(s). Verifique sua agenda.`);
  } else {
    alert("Plantão configurado com sucesso!");

    // Fecha modal
    const modalEl = document.getElementById("modalNovoPlantao");
    const modal = bootstrap.Modal.getInstance(modalEl);
    modal.hide();

    carregarAgenda(crm);
  }
}

/* ================== EXAMES ================== */

let todosExames = [];

async function carregarExames(crm) {
  const container = document.getElementById("exames-container");
  if (!container) return;

  try {
    // Agora busca TODOS os exames, não apenas os do médico
    const exames = await API.get(`/exames/`);
    todosExames = exames; // Salva para filtro local

    renderizarExames(exames);
  } catch (error) {
    console.error(error);
    container.innerHTML = `<p class="text-danger text-center">Erro ao carregar exames: ${error.message}</p>`;
  }
}

function renderizarExames(exames) {
  const container = document.getElementById("exames-container");
  if (!container) return;

  if (exames.length === 0) {
    container.innerHTML = `
            <div class="text-center py-5">
                <i class="bi bi-clipboard-x text-muted icon-lg mb-3"></i>
                <p class="text-muted">Nenhum exame encontrado.</p>
            </div>
        `;
    container.classList.add("bg-light", "border", "border-dashed");
    return;
  }

  let html = '<div class="list-group list-group-flush text-start">';
  exames.forEach((e) => {
    const dataSol = new Date(e.data_solicitacao).toLocaleDateString("pt-BR");
    let statusBadge = "";
    let statusText = "";
    let actionButton = "";
    let resultadoPreview = "";

    // Se tiver resultado, trata como 'R' mesmo que o status esteja desatualizado
    let statusReal = e.status;
    if (e.resultado_obtido && statusReal !== "R") {
      statusReal = "R";
    }

    switch (statusReal) {
      case "A":
        statusBadge = "bg-warning text-dark";
        statusText = "Agendado";
        actionButton = `<button class="btn btn-sm btn-outline-primary" onclick="abrirModalResultado(${e.id_exame})">
                                    <i class="bi bi-pencil-square me-1"></i> Registrar Resultado
                                </button>`;
        break;
      case "C":
        statusBadge = "bg-info text-white";
        statusText = "Coletado";
        actionButton = `<button class="btn btn-sm btn-outline-primary" onclick="abrirModalResultado(${e.id_exame})">
                                    <i class="bi bi-pencil-square me-1"></i> Registrar Resultado
                                </button>`;
        break;
      case "R":
        statusBadge = "bg-success";
        statusText = "Resultado Disponível";
        actionButton = `<button class="btn btn-sm btn-outline-success" onclick="verResultado(${e.id_exame})">
                                    <i class="bi bi-file-earmark-text me-1"></i> Ver Laudo
                                </button>`;
        break;
      default:
        statusBadge = "bg-secondary";
        statusText = e.status;
    }

    if (e.resultado_obtido) {
      resultadoPreview = `
                <div class="mt-2 p-2 bg-light rounded border border-success bg-opacity-10">
                    <small class="fw-bold text-success"><i class="bi bi-check-circle me-1"></i> Resultado:</small>
                    <p class="mb-0 small text-muted text-truncate" style="max-width: 600px;">${e.resultado_obtido}</p>
                </div>
            `;
    }

    html += `
            <div class="list-group-item px-0 py-3">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <div class="d-flex align-items-center mb-1">
                            <h6 class="mb-0 fw-bold">${e.nome_paciente}</h6>
                            <span class="badge ${statusBadge} ms-2">${statusText}</span>
                        </div>
                        <small class="text-muted">
                            <i class="bi bi-calendar3 me-1"></i> Solicitado em: ${dataSol}
                            <span class="mx-2">•</span>
                            <span class="fw-bold text-dark">${
                              e.nome_do_exame
                            }</span>
                            <span class="mx-2">•</span>
                            <span class="fst-italic">${formatarNomeMedico(
                              e.nome_medico_responsavel
                            )}</span>
                        </small>
                        ${resultadoPreview}
                    </div>
                    <div>
                        ${actionButton}
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
}

function filtrarExames(termo) {
  if (!termo) {
    renderizarExames(todosExames);
    return;
  }

  const termoLower = termo.toLowerCase();
  const filtrados = todosExames.filter(
    (e) =>
      e.nome_paciente.toLowerCase().includes(termoLower) ||
      e.nome_do_exame.toLowerCase().includes(termoLower) ||
      (e.nome_medico_responsavel &&
        e.nome_medico_responsavel.toLowerCase().includes(termoLower)) ||
      (e.status === "A" && "agendado".includes(termoLower)) ||
      (e.status === "C" && "coletado".includes(termoLower)) ||
      ((e.status === "R" || e.resultado_obtido) &&
        "resultado".includes(termoLower))
  );

  renderizarExames(filtrados);
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

async function verResultado(idExame) {
  const modalEl = document.getElementById("modalVerResultado");
  const modal = new bootstrap.Modal(modalEl);

  // Limpa campos anteriores
  document.getElementById("res-nome-exame").textContent = "Carregando...";
  document.getElementById("res-data").textContent = "...";
  document.getElementById("res-texto").textContent = "Buscando resultado...";

  modal.show();

  try {
    const exame = await API.get(`/exames/${idExame}`);

    document.getElementById("res-nome-exame").textContent =
      exame.nome_do_exame || "Exame";

    const dataRes = exame.data_resultado
      ? new Date(exame.data_resultado).toLocaleDateString("pt-BR")
      : "Data não informada";
    document.getElementById("res-data").textContent = dataRes;

    document.getElementById("res-texto").textContent =
      exame.resultado_obtido || "Nenhum resultado registrado.";
  } catch (error) {
    console.error(error);
    document.getElementById(
      "res-texto"
    ).innerHTML = `<span class="text-danger">Erro ao carregar resultado: ${error.message}</span>`;
  }
}

function abrirModalResultado(idExame) {
  document.getElementById("id_exame_resultado").value = idExame;
  document.getElementById("data_resultado").valueAsDate = new Date();
  document.querySelector("textarea[name='resultado_obtido']").value = "";

  const modal = new bootstrap.Modal(
    document.getElementById("modalRegistrarResultado")
  );
  modal.show();
}

// Handler para salvar resultado
const formResultado = document.getElementById("form-resultado");
if (formResultado) {
  formResultado.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    try {
      await API.post("/resultados-exame/", data);
      alert("Resultado registrado com sucesso!");

      // Fecha modal
      const modalEl = document.getElementById("modalRegistrarResultado");
      const modal = bootstrap.Modal.getInstance(modalEl);
      modal.hide();

      // Recarrega lista
      const crm = document.getElementById("medico-data").dataset.crm;
      carregarExames(crm);
    } catch (error) {
      alert("Erro ao registrar resultado: " + (error.message || error.error));
    }
  });
}

/* ========== INFORMAÇÕES PESSOAIS (Telefones) ========== */
document.addEventListener("DOMContentLoaded", () => {
  const personal = document.getElementById("personal-info");
  if (personal) {
    const crm = personal.dataset.crm;
    carregarTelefonesMedico(crm);

    document
      .getElementById("btn-add-telefone-medico")
      .addEventListener("click", async (e) => {
        e.preventDefault();
        const input = document.getElementById("novo-telefone-medico");
        const numero = input.value.trim();
        if (!numero) return alert("Digite um número válido");
        try {
          await API.post("/telefones/medicos/", {
            crm_medico: crm,
            numero_telefone: numero,
          });
          input.value = "";
          carregarTelefonesMedico(crm);
        } catch (err) {
          alert(
            "Erro ao adicionar telefone: " +
              (err.message || JSON.stringify(err))
          );
        }
      });
  }
});

async function carregarTelefonesMedico(crm) {
  const ul = document.getElementById("lista-telefones-medico");
  if (!ul) return;
  ul.innerHTML = '<li class="list-group-item text-muted">Carregando...</li>';
  try {
    const lista = await API.get(`/telefones/medicos/${crm}`);
    renderListaTelefonesMedico(lista || []);
  } catch (err) {
    ul.innerHTML = `<li class="list-group-item text-danger">Erro ao carregar: ${
      err.message || err
    }</li>`;
  }
}

function renderListaTelefonesMedico(lista) {
  const ul = document.getElementById("lista-telefones-medico");
  ul.innerHTML = "";
  if (!lista || lista.length === 0) {
    ul.innerHTML =
      '<li class="list-group-item text-muted">Nenhum telefone cadastrado.</li>';
    return;
  }

  lista.forEach((t) => {
    const li = document.createElement("li");
    li.className =
      "list-group-item d-flex justify-content-between align-items-center";
    li.innerHTML = `
      <span class="me-3">${t.numero_telefone}</span>
      <div class="btn-group btn-group-sm" role="group">
        <button class="btn btn-outline-secondary" onclick="editarTelefoneMedico(${
          t.id_telefone_medico
        }, '${t.numero_telefone.replace(/'/g, "\\'")}')">Editar</button>
        <button class="btn btn-danger" onclick="removerTelefoneMedico(${
          t.id_telefone_medico
        })">Remover</button>
      </div>
    `;
    ul.appendChild(li);
  });
}

async function removerTelefoneMedico(id) {
  if (!confirm("Remover telefone?")) return;
  try {
    await API.delete(`/telefones/medicos/${id}`);
    const crm = document.getElementById("personal-info").dataset.crm;
    carregarTelefonesMedico(crm);
  } catch (err) {
    alert("Erro ao remover: " + (err.message || JSON.stringify(err)));
  }
}

async function editarTelefoneMedico(id, atual) {
  const novo = prompt("Editar telefone:", atual);
  if (novo === null) return;
  try {
    await API.put(`/telefones/medicos/${id}`, { numero_telefone: novo });
    const crm = document.getElementById("personal-info").dataset.crm;
    carregarTelefonesMedico(crm);
  } catch (err) {
    alert("Erro ao editar: " + (err.message || JSON.stringify(err)));
  }
}

/* ================== EDIÇÃO DE PRESCRIÇÃO ================== */

let listaEdicaoPrescricao = [];
let idConsultaEdicao = null;

async function abrirModalEditarPrescricao(idConsulta) {
    idConsultaEdicao = idConsulta;
    listaEdicaoPrescricao = [];
    
    const modalEl = document.getElementById('modalEditarPrescricao');
    const modal = new bootstrap.Modal(modalEl);
    
    // Limpa UI
    document.querySelector('#tabela-edicao-prescricao tbody').innerHTML = '<tr><td colspan="3" class="text-center"><div class="spinner-border spinner-border-sm text-primary"></div> Carregando...</td></tr>';
    
    modal.show();
    
    try {
        // Carrega consulta com prescrições
        const consulta = await API.get(`/consultas/${idConsulta}`);
        
        if (consulta.prescricoes) {
            listaEdicaoPrescricao = consulta.prescricoes.map(p => ({
                id_prescricao: p.id_prescricao,
                id_medicamento: p.id_medicamento,
                nome: p.nome_comercial,
                quantidade_prescrita: p.quantidade_prescrita,
                frequencia_uso: p.frequencia_uso,
                dosagem: p.dosagem,
                is_deleted: false,
                is_new: false,
                is_updated: false
            }));
        }
        
        renderizarTabelaEdicaoPrescricao();
        await carregarMedicamentosEdicaoSelect();
        
    } catch (error) {
        console.error(error);
        alert('Erro ao carregar prescrições: ' + error.message);
        modal.hide();
    }
}

async function carregarMedicamentosEdicaoSelect() {
    const select = document.getElementById('edit-presc-medicamento');
    if (!select || select.options.length > 1) return;

    try {
        const meds = await API.get('/medicamentos/');
        select.innerHTML = '<option value="" disabled selected>Selecione...</option>';
        meds.forEach(m => {
            select.innerHTML += `<option value="${m.id_medicamento}">${m.nome_comercial} (${m.fabricante || 'Genérico'})</option>`;
        });
    } catch (e) {
        console.error('Erro ao carregar medicamentos', e);
        select.innerHTML = '<option disabled>Erro ao carregar lista</option>';
    }
}

function adicionarItemEdicaoPrescricao() {
    const select = document.getElementById('edit-presc-medicamento');
    const idMed = select.value;
    const nomeMed = select.options[select.selectedIndex]?.text;
    const qtd = document.getElementById('edit-presc-qtd').value;
    const uso = document.getElementById('edit-presc-uso').value;

    if (!idMed) return alert('Selecione um medicamento.');
    if (qtd <= 0) return alert('Quantidade inválida.');
    if (!uso) return alert('Informe a dosagem/frequência.');

    listaEdicaoPrescricao.push({
        id_medicamento: parseInt(idMed),
        nome: nomeMed,
        quantidade_prescrita: parseInt(qtd),
        frequencia_uso: uso,
        dosagem: uso,
        is_new: true,
        is_deleted: false
    });

    renderizarTabelaEdicaoPrescricao();

    select.value = "";
    document.getElementById('edit-presc-qtd').value = 1;
    document.getElementById('edit-presc-uso').value = "";
    select.focus();
}

function removerItemEdicaoPrescricao(index) {
    const item = listaEdicaoPrescricao[index];
    if (item.is_new) {
        listaEdicaoPrescricao.splice(index, 1);
    } else {
        item.is_deleted = true;
    }
    renderizarTabelaEdicaoPrescricao();
}

function renderizarTabelaEdicaoPrescricao() {
    const tbody = document.querySelector('#tabela-edicao-prescricao tbody');
    if (!tbody) return;

    tbody.innerHTML = '';
    
    const itensAtivos = listaEdicaoPrescricao.filter(i => !i.is_deleted);

    if (itensAtivos.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" class="text-center text-muted small">Nenhum medicamento prescrito.</td></tr>';
        return;
    }
    
    listaEdicaoPrescricao.forEach((item, index) => {
        if (item.is_deleted) return;
        
        tbody.innerHTML += `
            <tr>
                <td><small>${item.nome}</small> ${item.is_new ? '<span class="badge bg-success">Novo</span>' : ''}</td>
                <td>
                    <span class="badge bg-light text-dark border me-1">${item.quantidade_prescrita} un</span>
                    <small>${item.frequencia_uso}</small>
                </td>
                <td class="text-end">
                    <button class="btn btn-sm btn-link text-danger p-0" onclick="removerItemEdicaoPrescricao(${index})">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    });
}

async function salvarEdicaoPrescricao() {
    if (!idConsultaEdicao) return;
    
    const btnSalvar = document.getElementById('btn-salvar-edicao');
    const textoOriginal = btnSalvar.innerHTML;
    btnSalvar.disabled = true;
    btnSalvar.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Salvando...';
    
    try {
        // Processa as mudanças
        for (const item of listaEdicaoPrescricao) {
            if (item.is_deleted) {
                if (!item.is_new) {
                    await API.delete(`/prescricoes/${item.id_prescricao}`);
                }
            } else if (item.is_new) {
                await API.post('/prescricoes/', {
                    id_consulta: parseInt(idConsultaEdicao),
                    id_medicamento: item.id_medicamento,
                    quantidade_prescrita: item.quantidade_prescrita,
                    dosagem: item.dosagem,
                    frequencia_uso: item.frequencia_uso
                });
            }
        }
        
        alert('Prescrição atualizada com sucesso!');
        const modalEl = document.getElementById('modalEditarPrescricao');
        const modal = bootstrap.Modal.getInstance(modalEl);
        modal.hide();
        
        // Recarrega a lista
        const crm = document.getElementById('medico-data').dataset.crm;
        carregarConsultas(crm);
        
    } catch (error) {
        console.error(error);
        alert('Erro ao salvar alterações: ' + error.message);
    } finally {
        btnSalvar.disabled = false;
        btnSalvar.innerHTML = textoOriginal;
    }
}

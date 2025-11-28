document.addEventListener("DOMContentLoaded", async () => {
  // 1. Busca o container e o ID de forma segura
  const container = document.getElementById("timeline-container");
  if (!container) return; // Se não estiver na página certa, para.

  // Lê o atributo data-id-paciente do HTML
  const idPaciente = container.dataset.idPaciente;

  if (!idPaciente) {
    console.error("ID do paciente não encontrado.");
    return;
  }

  try {
    // 2. Carrega dados do paciente
    const paciente = await API.get(`/pacientes/${idPaciente}`);

    // Atualiza o cabeçalho (verifique se os IDs existem no seu HTML)
    const elNome = document.getElementById("paciente-nome");
    const elCpf = document.getElementById("paciente-cpf");
    const elIdade = document.getElementById("paciente-idade");

    if (elNome) elNome.textContent = paciente.nome_paciente;
    if (elCpf) elCpf.textContent = `CPF: ${paciente.cpf}`;
    if (elIdade)
      elIdade.textContent = `Nasc: ${new Date(
        paciente.data_nascimento
      ).toLocaleDateString("pt-BR", { timeZone: "UTC" })}`;

    // 3. Carrega histórico
    const historico = await API.get(`/pacientes/${idPaciente}/historico`);
    renderizarTimeline(historico);
  } catch (error) {
    console.error(error);
    container.innerHTML =
      '<p class="text-danger">Erro ao carregar prontuário.</p>';
  }
});

function renderizarTimeline(eventos) {
  const container = document.getElementById("timeline-container");
  container.innerHTML = "";

  if (!eventos || eventos.length === 0) {
    container.innerHTML =
      '<p class="text-muted ms-3">Nenhum registro histórico encontrado.</p>';
    return;
  }

  eventos.forEach((evento) => {
    // Define ícone e cor baseados no tipo (Consulta ou Exame)
    // Ajuste conforme os dados reais retornados pela sua View SQL
    const isConsulta = evento.tipo === "Consulta";
    const icon = isConsulta ? "bi-clipboard-pulse" : "bi-flask";
    const color = isConsulta ? "primary" : "warning";

    // Tratamento de data seguro
    let dataTexto = "Data inválida";
    if (evento.data_evento) {
      dataTexto = new Date(evento.data_evento).toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    }

    const item = `
            <div class="card border-0 shadow-sm mb-3 ms-3 position-relative">
                <div class="position-absolute top-0 start-0 translate-middle bg-${color} rounded-circle border border-white"
                     style="width: 16px; height: 16px; left: -18px !important; margin-top: 20px;"></div>

                <div class="card-body">
                    <div class="d-flex justify-content-between mb-2">
                        <span class="badge bg-${color} bg-opacity-10 text-${color}">
                            <i class="bi ${icon} me-1"></i> ${evento.tipo}
                        </span>
                        <small class="text-muted">${dataTexto}</small>
                    </div>

                    <h5 class="card-title h6">${
                      evento.descricao || "Sem descrição"
                    }</h5>

                    <div class="d-flex align-items-center text-muted small mt-2">
                        <i class="bi bi-person-fill me-1"></i> Dr(a). ${
                          evento.responsavel || "Não informado"
                        }
                        <span class="mx-2">•</span>
                        Status: ${evento.status || "-"}
                    </div>
                </div>
            </div>
        `;
    container.innerHTML += item;
  });
}

let listaPacientesGlobal = [];

document.addEventListener("DOMContentLoaded", () => {
  carregarPacientes();
});

async function carregarPacientes() {
  const tbody = document.querySelector("#tabela-pacientes tbody");

  try {
    const pacientes = await API.get("/pacientes/");

    // Processar dados (calcular idade)
    listaPacientesGlobal = pacientes.map((p) => {
      return {
        ...p,
        idade: calcularIdade(p.data_nascimento),
        data_nascimento_fmt: new Date(p.data_nascimento).toLocaleDateString(
          "pt-BR",
          { timeZone: "UTC" }
        ),
      };
    });

    if (listaPacientesGlobal.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" class="text-center text-muted py-5">Nenhum paciente cadastrado.</td></tr>`;
      atualizarKPIs([]);
      return;
    }

    renderizarTabela(listaPacientesGlobal);
    atualizarKPIs(listaPacientesGlobal);
  } catch (error) {
    console.error("Erro ao carregar pacientes:", error);
    tbody.innerHTML = `<tr><td colspan="5" class="text-center text-danger py-4">Erro ao conectar com o servidor: ${error.message}</td></tr>`;
  }
}

function renderizarTabela(lista) {
  const tbody = document.querySelector("#tabela-pacientes tbody");
  const contador = document.getElementById("contador-registros");

  tbody.innerHTML = "";
  contador.textContent = `Exibindo ${lista.length} registros`;

  if (lista.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" class="text-center text-muted py-4">Nenhum paciente encontrado para a busca.</td></tr>`;
    return;
  }

  lista.forEach((p) => {
    const tr = document.createElement("tr");

    // Avatar com iniciais
    const iniciais = p.nome_paciente
      .split(" ")
      .map((n) => n[0])
      .slice(0, 2)
      .join("")
      .toUpperCase();
    const corAvatar = "primary"; // Poderia ser randomizado

    tr.innerHTML = `
                <td class="ps-4">
                    <div class="d-flex align-items-center">
                        <div class="rounded-circle bg-${corAvatar} bg-opacity-10 text-${corAvatar} d-flex align-items-center justify-content-center me-3 fw-bold" style="width: 40px; height: 40px;">
                            ${iniciais}
                        </div>
                        <div>
                            <div class="fw-bold text-dark">${
                              p.nome_paciente
                            }</div>
                            <div class="small text-muted">ID: ${
                              p.id_paciente
                            }</div>
                        </div>
                    </div>
                </td>
                <td><span class="font-monospace text-secondary">${
                  p.cpf
                }</span></td>
                <td>
                    <div class="d-flex flex-column">
                        <span class="fw-bold">${p.idade} anos</span>
                        <span class="small text-muted">${
                          p.data_nascimento_fmt
                        }</span>
                    </div>
                </td>
                <td><span class="small text-muted text-truncate d-inline-block" style="max-width: 250px;">${
                  p.endereco || "-"
                }</span></td>
                <td class="text-end pe-4">
                    <button class="btn btn-sm btn-outline-info border-0 me-1" onclick="verHistorico(${
                      p.id_paciente
                    })" title="Prontuário e Histórico">
                        <i class="bi bi-clipboard2-pulse"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger border-0" onclick="deletarPaciente(${
                      p.id_paciente
                    })" title="Excluir Cadastro">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            `;
    tbody.appendChild(tr);
  });
}

function atualizarKPIs(lista) {
  const total = lista.length;
  const idosos = lista.filter((p) => p.idade >= 60).length;
  const menores = lista.filter((p) => p.idade < 18).length;

  // Atualiza com animação simples (apenas texto)
  document.getElementById("kpi-total").textContent = total;
  document.getElementById("kpi-idosos").textContent = idosos;
  document.getElementById("kpi-menores").textContent = menores;
}

// Utilitário para calcular idade
function calcularIdade(dataString) {
  const hoje = new Date();
  const nascimento = new Date(dataString);
  let idade = hoje.getFullYear() - nascimento.getFullYear();
  const m = hoje.getMonth() - nascimento.getMonth();

  // Ajuste se ainda não fez aniversário este ano
  if (m < 0 || (m === 0 && hoje.getDate() < nascimento.getDate())) {
    idade--;
  }
  return idade;
}

// Filtro de Busca
document.getElementById("input-busca").addEventListener("keyup", (e) => {
  const termo = e.target.value.toLowerCase();
  const filtrados = listaPacientesGlobal.filter(
    (p) =>
      p.nome_paciente.toLowerCase().includes(termo) || p.cpf.includes(termo)
  );
  renderizarTabela(filtrados);
});

// Ações
async function deletarPaciente(id) {
  if (
    confirm(
      "ATENÇÃO: Deseja realmente excluir este paciente? Isso pode afetar históricos de consultas e internações."
    )
  ) {
    try {
      await API.delete(`/pacientes/${id}`);
      // Remove da lista global e re-renderiza sem precisar chamar API de novo
      listaPacientesGlobal = listaPacientesGlobal.filter(
        (p) => p.id_paciente !== id
      );
      renderizarTabela(listaPacientesGlobal);
      atualizarKPIs(listaPacientesGlobal);
      alert("Paciente removido com sucesso!");
    } catch (error) {
      alert("Erro ao deletar paciente: " + error.message);
    }
  }
}

function verHistorico(id) {
  window.location.href = `/ui/pacientes/${id}/historico`;
}

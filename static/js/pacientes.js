document.addEventListener("DOMContentLoaded", () => {
  carregarPacientes();
});

async function carregarPacientes() {
  try {
    // Busca a lista na API
    const pacientes = await API.get("/pacientes/");
    const tbody = document.querySelector("#tabela-pacientes tbody");
    tbody.innerHTML = "";

    if (pacientes.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" class="text-center text-muted">Nenhum paciente encontrado.</td></tr>`;
      return;
    }

    pacientes.forEach((p) => {
      const tr = document.createElement("tr");

      // Formata data de YYYY-MM-DD para DD/MM/YYYY
      const dataNasc = new Date(p.data_nascimento).toLocaleDateString("pt-BR", {
        timeZone: "UTC",
      });

      tr.innerHTML = `
                <td><span class="fw-bold text-muted">#${
                  p.id_paciente
                }</span></td>
                <td>
                    <div class="d-flex align-items-center">
                        <div class="avatar-placeholder me-2 rounded-circle bg-light d-flex align-items-center justify-content-center" style="width: 32px; height: 32px;">
                            <span class="small text-primary fw-bold">${p.nome_paciente.charAt(
                              0
                            )}</span>
                        </div>
                        ${p.nome_paciente}
                    </div>
                </td>
                <td>${p.cpf}</td>
                <td>${dataNasc}</td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-info me-1" onclick="verHistorico(${
                      p.id_paciente
                    })" title="Ver Histórico">
                        📋 Histórico
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deletarPaciente(${
                      p.id_paciente
                    })" title="Excluir">
                        🗑️
                    </button>
                </td>
            `;
      tbody.appendChild(tr);
    });
  } catch (error) {
    console.error("Erro ao carregar pacientes:", error);
    document.querySelector(
      "#tabela-pacientes tbody"
    ).innerHTML = `<tr><td colspan="5" class="text-center text-danger">Erro ao carregar dados. Verifique a conexão.</td></tr>`;
  }
}

async function deletarPaciente(id) {
  if (
    confirm(
      "Tem certeza que deseja remover este paciente? Isso pode afetar históricos de consultas."
    )
  ) {
    try {
      await API.delete(`/pacientes/${id}`); // A rota no Flask deve suportar DELETE /pacientes/<id>
      alert("Paciente removido com sucesso!");
      carregarPacientes(); // Recarrega a tabela
    } catch (error) {
      alert("Erro ao deletar paciente: " + error.message);
    }
  }
}

function verHistorico(id) {
  // Redireciona para uma página de histórico (que você criará depois)
  // ou abre um modal. Por enquanto, vamos alertar.
  window.location.href = `/ui/pacientes/${id}/historico`;
}

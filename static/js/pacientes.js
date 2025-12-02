let listaPacientesGlobal = [];

document.addEventListener("DOMContentLoaded", () => {
  carregarPacientes();
});

async function carregarPacientes() {
  const tbody = document.querySelector("#tabela-pacientes tbody");

  try {
    // A API agora retorna 'foto_base64' (se o backend estiver correto)
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

    // Calcula iniciais para o caso de não ter foto
    const iniciais = p.nome_paciente
      .split(" ")
      .map((n) => n[0])
      .slice(0, 2)
      .join("")
      .toUpperCase();

    // 1. Lógica do Avatar (Foto ou Iniciais) - CORRIGIDA E UNIFICADA
    let avatarHtml;
    if (p.foto_base64) {
      // Se tiver foto, usa a tag IMG com a Base64
      avatarHtml = `
            <div class="rounded-circle d-flex align-items-center justify-content-center me-3 position-relative overflow-hidden"
                 style="width: 40px; height: 40px; background-color: #e9ecef;">
                <img src="data:image/jpeg;base64,${p.foto_base64}" alt="Foto" style="width: 100%; height: 100%; object-fit: cover;">
            </div>`;
    } else {
      // Se não tiver, usa as iniciais
      avatarHtml = `
            <div class="rounded-circle bg-primary bg-opacity-10 text-primary d-flex align-items-center justify-content-center me-3 fw-bold"
                 style="width: 40px; height: 40px;">
                ${iniciais}
            </div>`;
    }

    // 2. Monta a linha completa
    tr.innerHTML = `
                <td class="ps-4">
                    <div class="d-flex align-items-center">
                        ${avatarHtml}
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
                    <button class="btn btn-sm btn-outline-secondary border-0 me-1" onclick="iniciarUploadFoto(${
                      p.id_paciente
                    })" title="Alterar Foto">
                        <i class="bi bi-camera"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-info border-0 me-1" onclick="verHistorico(${
                      p.id_paciente
                    })" title="Prontuário">
                        <i class="bi bi-clipboard2-pulse"></i>
                    </button>
                    ${USER_ROLE !== 'enfermeiro' ? `
                    <button class="btn btn-sm btn-outline-danger border-0" onclick="deletarPaciente(${
                      p.id_paciente
                    })" title="Excluir">
                        <i class="bi bi-trash"></i>
                    </button>` : ''}
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
  const elTotal = document.getElementById("kpi-total");
  const elIdosos = document.getElementById("kpi-idosos");
  const elMenores = document.getElementById("kpi-menores");

  if (elTotal) elTotal.textContent = total;
  if (elIdosos) elIdosos.textContent = idosos;
  if (elMenores) elMenores.textContent = menores;
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
const inputBusca = document.getElementById("input-busca");
if (inputBusca) {
  inputBusca.addEventListener("keyup", (e) => {
    const termo = e.target.value.toLowerCase();
    const filtrados = listaPacientesGlobal.filter(
      (p) =>
        p.nome_paciente.toLowerCase().includes(termo) || p.cpf.includes(termo)
    );
    renderizarTabela(filtrados);
  });
}

// Ações
async function deletarPaciente(id) {
  // Passo 1: Confirmação inicial
  const result1 = await Swal.fire({
    title: 'Tem certeza?',
    text: "Deseja iniciar o processo de exclusão deste paciente?",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'Sim, continuar',
    cancelButtonText: 'Cancelar'
  });

  if (result1.isConfirmed) {
    // Passo 2: Confirmação crítica (Dupla confirmação)
    const result2 = await Swal.fire({
      title: 'Atenção Crítica!',
      html: "Ao apagar este paciente, <b>TODOS</b> os registros vinculados a ele serão perdidos permanentemente:<br><br>" +
            "<ul style='text-align: left;'>" +
            "<li>Histórico de Consultas</li>" +
            "<li>Registros de Internações</li>" +
            "<li>Prescrições e Exames</li>" +
            "</ul>" +
            "Essa ação <b>NÃO</b> pode ser desfeita.",
      icon: 'error',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#6c757d',
      confirmButtonText: 'Sim, apagar tudo!',
      cancelButtonText: 'Cancelar',
      focusCancel: true // Foca no cancelar por segurança
    });

    if (result2.isConfirmed) {
      try {
        await API.delete(`/pacientes/${id}`);
        
        // Remove da lista global e re-renderiza
        listaPacientesGlobal = listaPacientesGlobal.filter(
          (p) => p.id_paciente !== id
        );
        renderizarTabela(listaPacientesGlobal);
        atualizarKPIs(listaPacientesGlobal);
        
        Swal.fire(
          'Excluído!',
          'O paciente e todos os seus registros foram removidos.',
          'success'
        );
      } catch (error) {
        Swal.fire(
          'Erro!',
          'Erro ao deletar paciente: ' + error.message,
          'error'
        );
      }
    }
  }
}

function verHistorico(id) {
  window.location.href = `/ui/pacientes/${id}/historico`;
}

// 1. Função chamada ao clicar no botão "Alterar Foto"
function iniciarUploadFoto(idPaciente) {
  const input = document.getElementById("input-foto-paciente");
  const hiddenId = document.getElementById("id-paciente-foto");

  if (input && hiddenId) {
    hiddenId.value = idPaciente;
    input.click(); // Simula clique no input invisível
  } else {
    console.error("Elementos de upload não encontrados no HTML");
  }
}

// 2. Processa o arquivo selecionado
async function processarUploadFoto() {
  const input = document.getElementById("input-foto-paciente");
  const idPaciente = document.getElementById("id-paciente-foto").value;

  if (input.files && input.files[0]) {
    const file = input.files[0];

    // Converte para Base64
    const reader = new FileReader();
    reader.onload = async function (e) {
      // O resultado vem como "data:image/jpeg;base64,....."
      const base64String = e.target.result.split(",")[1];

      try {
        const response = await API.post(`/pacientes/${idPaciente}/foto`, {
          foto_base64: base64String,
        });

        // Verifica se houve erro no JSON retornado pelo backend (se o 500 não ocorreu)
        if (response.error) {
          throw new Error(response.error);
        }

        alert("Foto atualizada com sucesso!");
        carregarPacientes(); // Recarrega a lista para mostrar a nova foto
      } catch (error) {
        console.error(error);
        alert("Erro ao enviar foto: " + error.message);
      }
    };
    reader.readAsDataURL(file);
  }
  // Limpa o input
  input.value = "";
}

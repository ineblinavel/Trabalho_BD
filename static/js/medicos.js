let todosMedicos = [];

document.addEventListener("DOMContentLoaded", () => {
  if (typeof Validation !== 'undefined') {
      Validation.applyMasks();
  }
  carregarMedicos();

  // Listeners de busca
  document.getElementById('search-ativos').addEventListener('keyup', (e) => {
      filtrarMedicos(e.target.value, true);
  });
  document.getElementById('search-inativos').addEventListener('keyup', (e) => {
      filtrarMedicos(e.target.value, false);
  });
});

async function carregarMedicos() {
  try {
    // Busca TODOS os médicos (ativos e inativos)
    const medicos = await API.get("/medicos/medicos?include_inactive=true");
    todosMedicos = medicos;
    
    renderizarTabelas(medicos);

  } catch (error) {
    console.error("Erro ao carregar médicos:", error);
  }
}

function renderizarTabelas(listaMedicos) {
    const tbodyAtivos = document.querySelector("#tabela-medicos-ativos tbody");
    const tbodyInativos = document.querySelector("#tabela-medicos-inativos tbody");
    
    tbodyAtivos.innerHTML = "";
    tbodyInativos.innerHTML = "";

    const ativos = listaMedicos.filter(m => m.ativo);
    const inativos = listaMedicos.filter(m => !m.ativo);

    renderizarRows(ativos, tbodyAtivos, true);
    renderizarRows(inativos, tbodyInativos, false);
}

function renderizarRows(lista, tbody, isAtivo) {
    if (lista.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center text-muted py-4">Nenhum registro encontrado.</td></tr>`;
        return;
    }

    lista.forEach((medico) => {
      const salarioFmt = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(medico.salario);
      const tr = document.createElement("tr");
      
      let botoes = '';
      if (isAtivo) {
          botoes = `
            <button class="btn btn-sm btn-outline-primary border-0 me-1" onclick="abrirModalEditar('${medico.crm}')" title="Editar">
                <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-sm btn-outline-danger border-0" onclick="deletarMedico('${medico.crm}')" title="Desativar">
                <i class="bi bi-trash"></i>
            </button>
          `;
      } else {
          botoes = `
            <button class="btn btn-sm btn-outline-success border-0" onclick="reativarMedico('${medico.crm}')" title="Reativar">
                <i class="bi bi-arrow-counterclockwise me-1"></i> Reativar
            </button>
          `;
      }

      tr.innerHTML = `
                <td><span class="fw-bold text-dark">${medico.crm}</span></td>
                <td>${medico.nome_medico}</td>
                <td>${medico.cpf}</td>
                <td>${salarioFmt}</td>
                <td class="text-end">${botoes}</td>
            `;
      tbody.appendChild(tr);
    });
}

function filtrarMedicos(termo, apenasAtivos) {
    const termoLower = termo.toLowerCase();
    
    // Filtra da lista global
    const filtrados = todosMedicos.filter(m => {
        // Primeiro verifica se o status bate com a aba
        const statusMatch = apenasAtivos ? m.ativo : !m.ativo;
        if (!statusMatch) return false;

        // Depois verifica o termo de busca
        return m.nome_medico.toLowerCase().includes(termoLower) ||
               m.crm.toLowerCase().includes(termoLower) ||
               m.cpf.includes(termoLower);
    });

    // Renderiza apenas a tabela específica
    const tbody = document.querySelector(apenasAtivos ? "#tabela-medicos-ativos tbody" : "#tabela-medicos-inativos tbody");
    tbody.innerHTML = "";
    renderizarRows(filtrados, tbody, apenasAtivos);
}

async function salvarMedico() {
    const crm = document.getElementById('crm').value.trim();
    const nome = document.getElementById('nome_medico').value.trim();
    const cpf = document.getElementById('cpf').value.trim();
    const salarioVal = document.getElementById('salario').value;
    const salario = parseFloat(salarioVal);
    const isEdit = document.getElementById('is_edit_medico').value === 'true';

    if (!crm || !nome || !cpf || !salarioVal) return alert("Preencha todos os campos!");
    
    if (typeof Validation !== 'undefined' && !Validation.isValidCPF(cpf)) {
        return alert("CPF inválido!");
    }
    if (isNaN(salario) || salario <= 0) {
        return alert("O salário deve ser maior que zero.");
    }

    try {
        if (isEdit) {
            await API.put(`/medicos/${crm}`, {
                nome_medico: nome,
                cpf: cpf,
                salario: parseFloat(salario)
            });
            alert("Médico atualizado!");
        } else {
            const res = await API.post('/medicos/medicos', {
                crm: crm,
                nome_medico: nome,
                cpf: cpf,
                salario: parseFloat(salario)
            });
            alert(res.message || "Médico cadastrado!");
        }
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('modalNovoMedico'));
        modal.hide();
        document.getElementById('formMedico').reset();
        document.getElementById('is_edit_medico').value = 'false';
        document.getElementById('crm').readOnly = false;
        carregarMedicos();
    } catch (e) {
        alert("Erro: " + (e.message || e.error));
    }
}

async function abrirModalEditar(crm) {
    try {
        const medico = await API.get(`/medicos/${crm}`);
        
        document.getElementById('crm').value = medico.crm;
        document.getElementById('nome_medico').value = medico.nome_medico;
        document.getElementById('cpf').value = medico.cpf;
        document.getElementById('salario').value = medico.salario;
        document.getElementById('password').value = medico.password || '********'; 
        
        document.getElementById('is_edit_medico').value = 'true';
        document.getElementById('crm').readOnly = true;
        
        new bootstrap.Modal(document.getElementById('modalNovoMedico')).show();
    } catch (e) {
        alert("Erro ao carregar dados do médico: " + e.message);
    }
}

async function deletarMedico(crm) {
  if (confirm("Tem certeza que deseja desativar este médico? Ele ficará disponível na aba 'Inativos'.")) {
    try {
        await API.delete(`/medicos/${crm}`);
        carregarMedicos();
    } catch (e) {
        alert("Erro: " + (e.message || e.error));
    }
  }
}

async function reativarMedico(crm) {
    if (confirm("Deseja reativar este médico?")) {
      try {
          await API.post(`/medicos/${crm}/reactivate`, {});
          carregarMedicos();
      } catch (e) {
          alert("Erro: " + (e.message || e.error));
      }
    }
  }

document.addEventListener("DOMContentLoaded", () => {
  if (typeof Validation !== 'undefined') {
      Validation.applyMasks();
  }
  carregarEnfermeiros();
});

async function carregarEnfermeiros() {
  try {
    const enfermeiros = await API.get("/enfermeiros/");
    const tbody = document.querySelector("#tabela-enfermeiros tbody");
    tbody.innerHTML = "";

    if (enfermeiros.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">Nenhum enfermeiro cadastrado.</td></tr>';
        return;
    }

    enfermeiros.forEach((enf) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
                <td>${enf.corem}</td>
                <td>${enf.nome_enfermeiro}</td>
                <td>${enf.cpf}</td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary border-0 me-1" 
                        onclick="abrirModalEditar('${enf.corem}', '${enf.nome_enfermeiro}', '${enf.cpf}')">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger border-0" onclick="deletarEnfermeiro('${enf.corem}')">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            `;
      tbody.appendChild(tr);
    });
  } catch (error) {
    console.error("Erro ao carregar enfermeiros:", error);
    document.querySelector("#tabela-enfermeiros tbody").innerHTML = 
        '<tr><td colspan="4" class="text-center text-danger">Erro ao carregar dados.</td></tr>';
  }
}

async function salvarEnfermeiro() {
    const corem = document.getElementById('corem').value.trim();
    const nome = document.getElementById('nome_enfermeiro').value.trim();
    const cpf = document.getElementById('cpf').value.trim();
    const isEdit = document.getElementById('is_edit_enfermeiro').value === 'true';

    if (!corem || !nome || !cpf) return alert("Preencha todos os campos!");

    if (!Validation.isValidCPF(cpf)) {
        return alert("CPF inválido!");
    }

    try {
        if (isEdit) {
            await API.put(`/enfermeiros/${corem}`, {
                nome_enfermeiro: nome,
                cpf: cpf
            });
            alert("Enfermeiro atualizado!");
        } else {
            const res = await API.post('/enfermeiros/', {
                corem: corem,
                nome_enfermeiro: nome,
                cpf: cpf
            });
            alert(res.message || "Enfermeiro cadastrado!");
        }
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('modalNovoEnfermeiro'));
        modal.hide();
        document.getElementById('formEnfermeiro').reset();
        document.getElementById('is_edit_enfermeiro').value = 'false';
        document.getElementById('corem').readOnly = false;
        carregarEnfermeiros();
    } catch (e) {
        alert("Erro: " + e.message);
    }
}

function abrirModalEditar(corem, nome, cpf) {
    document.getElementById('corem').value = corem;
    document.getElementById('nome_enfermeiro').value = nome;
    document.getElementById('cpf').value = cpf;
    document.getElementById('is_edit_enfermeiro').value = 'true';
    document.getElementById('corem').readOnly = true;
    
    new bootstrap.Modal(document.getElementById('modalNovoEnfermeiro')).show();
}

async function deletarEnfermeiro(corem) {
  if (confirm("Tem certeza que deseja excluir este enfermeiro?")) {
    try {
        await API.delete(`/enfermeiros/${corem}`);
        carregarEnfermeiros();
    } catch (error) {
        alert("Erro ao deletar: " + error.message);
    }
  }
}

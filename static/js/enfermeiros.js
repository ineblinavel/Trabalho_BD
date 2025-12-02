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
                        onclick="abrirModalEditar('${enf.corem}')">
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

function abrirModalNovo() {
    document.getElementById('formEnfermeiro').reset();
    document.getElementById('is_edit_enfermeiro').value = 'false';
    document.getElementById('corem').readOnly = false;
    document.getElementById('containerSenhaEnfermeiro').style.display = 'none';
    new bootstrap.Modal(document.getElementById('modalNovoEnfermeiro')).show();
}

async function salvarEnfermeiro() {
    const corem = document.getElementById('corem').value.trim();
    const nome = document.getElementById('nome_enfermeiro').value.trim();
    const cpf = document.getElementById('cpf').value.trim();
    const isEdit = document.getElementById('is_edit_enfermeiro').value === 'true';

    if (!corem || !nome || !cpf) return Swal.fire('Atenção', "Preencha todos os campos!", 'warning');

    if (!Validation.isValidCPF(cpf)) {
        return Swal.fire('Erro', "CPF inválido!", 'error');
    }

    try {
        if (isEdit) {
            await API.put(`/enfermeiros/${corem}`, {
                nome_enfermeiro: nome,
                cpf: cpf
            });
            Swal.fire('Sucesso', "Enfermeiro atualizado!", 'success');
        } else {
            const res = await API.post('/enfermeiros/', {
                corem: corem,
                nome_enfermeiro: nome,
                cpf: cpf
            });
            Swal.fire('Sucesso', res.message || "Enfermeiro cadastrado!", 'success');
        }
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('modalNovoEnfermeiro'));
        modal.hide();
        document.getElementById('formEnfermeiro').reset();
        document.getElementById('is_edit_enfermeiro').value = 'false';
        document.getElementById('corem').readOnly = false;
        carregarEnfermeiros();
    } catch (e) {
        Swal.fire('Erro', "Erro: " + e.message, 'error');
    }
}

async function abrirModalEditar(corem) {
    try {
        const enf = await API.get(`/enfermeiros/${corem}`);
        
        document.getElementById('corem').value = enf.corem;
        document.getElementById('nome_enfermeiro').value = enf.nome_enfermeiro;
        document.getElementById('cpf').value = enf.cpf;
        document.getElementById('password').value = enf.password || '********'; 
        
        document.getElementById('is_edit_enfermeiro').value = 'true';
        document.getElementById('corem').readOnly = true;
        document.getElementById('containerSenhaEnfermeiro').style.display = 'block';
        
        new bootstrap.Modal(document.getElementById('modalNovoEnfermeiro')).show();
    } catch (e) {
        Swal.fire('Erro', "Erro ao carregar dados do enfermeiro: " + e.message, 'error');
    }
}

async function deletarEnfermeiro(corem) {
  const result = await Swal.fire({
      title: 'Tem certeza?',
      text: "Deseja excluir este enfermeiro?",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Sim, excluir!',
      cancelButtonText: 'Cancelar'
  });

  if (result.isConfirmed) {
    try {
        await API.delete(`/enfermeiros/${corem}`);
        carregarEnfermeiros();
        Swal.fire('Excluído!', 'O enfermeiro foi excluído.', 'success');
    } catch (error) {
        Swal.fire('Erro', "Erro ao deletar: " + error.message, 'error');
    }
  }
}

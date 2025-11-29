document.addEventListener("DOMContentLoaded", () => {
  if (typeof Validation !== 'undefined') {
      Validation.applyMasks();
  }
  carregarMedicos();
});

async function carregarMedicos() {
  try {
    const medicos = await API.get("/medicos/medicos"); // Rota da sua API
    const tbody = document.querySelector("#tabela-medicos tbody");
    tbody.innerHTML = "";

    medicos.forEach((medico) => {
      const salarioFmt = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(medico.salario);
      const tr = document.createElement("tr");
      tr.innerHTML = `
                <td>${medico.crm}</td>
                <td>${medico.nome_medico}</td>
                <td>${medico.cpf}</td>
                <td>${salarioFmt}</td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary border-0 me-1" 
                        onclick="abrirModalEditar('${medico.crm}', '${medico.nome_medico}', '${medico.cpf}', ${medico.salario})">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger border-0" onclick="deletarMedico('${medico.crm}')">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            `;
      tbody.appendChild(tr);
    });
  } catch (error) {
    console.error("Erro ao carregar médicos:", error);
  }
}

async function salvarMedico() {
    const crm = document.getElementById('crm').value.trim();
    const nome = document.getElementById('nome_medico').value.trim();
    const cpf = document.getElementById('cpf').value.trim();
    const salarioVal = document.getElementById('salario').value;
    const salario = parseFloat(salarioVal);
    const isEdit = document.getElementById('is_edit_medico').value === 'true';

    if (!crm || !nome || !cpf || !salarioVal) return alert("Preencha todos os campos!");
    
    if (!Validation.isValidCPF(cpf)) {
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
        alert("Erro: " + e.message);
    }
}

function abrirModalEditar(crm, nome, cpf, salario) {
    document.getElementById('crm').value = crm;
    document.getElementById('nome_medico').value = nome;
    document.getElementById('cpf').value = cpf;
    document.getElementById('salario').value = salario;
    document.getElementById('is_edit_medico').value = 'true';
    document.getElementById('crm').readOnly = true;
    
    new bootstrap.Modal(document.getElementById('modalNovoMedico')).show();
}

async function deletarMedico(crm) {
  if (confirm("Tem certeza que deseja excluir este médico?")) {
    try {
        await API.delete(`/medicos/${crm}`);
        carregarMedicos();
    } catch (e) {
        alert("Erro: " + e.message);
    }
  }
}

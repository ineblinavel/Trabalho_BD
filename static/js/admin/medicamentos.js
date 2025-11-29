document.addEventListener("DOMContentLoaded", carregarMedicamentos);

async function carregarMedicamentos() {
    try {
        const lista = await API.get('/medicamentos/');
        const tbody = document.querySelector('#tabela-medicamentos tbody');
        tbody.innerHTML = '';
        
        if(lista.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">Nenhum medicamento cadastrado.</td></tr>';
            return;
        }

        lista.forEach(m => {
            tbody.innerHTML += `
                <tr>
                    <td>${m.id_medicamento}</td>
                    <td class="fw-bold">${m.nome_comercial}</td>
                    <td>${m.fabricante || '-'}</td>
                    <td class="text-end">
                        <button class="btn btn-sm btn-outline-primary border-0 me-1" onclick="abrirModalEditar(${m.id_medicamento}, '${m.nome_comercial}', '${m.fabricante || ''}')">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger border-0" onclick="deletarMedicamento(${m.id_medicamento})">
                            <i class="bi bi-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
    } catch (e) {
        console.error(e);
    }
}

async function salvarMedicamento() {
    const id = document.getElementById('id_medicamento').value;
    const nome = document.getElementById('nome_comercial').value.trim();
    const fabricante = document.getElementById('fabricante').value.trim();
    
    if(!nome) return alert("Nome comercial é obrigatório");
    if(nome.length < 3) return alert("Nome comercial muito curto.");

    try {
        if (id) {
            await API.put(`/medicamentos/${id}`, { 
                nome_comercial: nome, 
                fabricante: fabricante 
            });
            alert("Medicamento atualizado!");
        } else {
            await API.post('/medicamentos/', { 
                nome_comercial: nome, 
                fabricante: fabricante 
            });
            alert("Medicamento cadastrado!");
        }
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('modalNovoMedicamento'));
        modal.hide();
        document.getElementById('formMedicamento').reset();
        document.getElementById('id_medicamento').value = '';
        carregarMedicamentos();
    } catch (e) {
        alert("Erro: " + e.message);
    }
}

function abrirModalEditar(id, nome, fabricante) {
    document.getElementById('id_medicamento').value = id;
    document.getElementById('nome_comercial').value = nome;
    document.getElementById('fabricante').value = fabricante;
    
    const modal = new bootstrap.Modal(document.getElementById('modalNovoMedicamento'));
    modal.show();
}

async function deletarMedicamento(id) {
    if(confirm("Remover este medicamento?")) {
        try {
            await API.delete(`/medicamentos/${id}`);
            carregarMedicamentos();
        } catch (e) {
            alert("Erro: " + e.message);
        }
    }
}

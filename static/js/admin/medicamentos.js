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
    
    if(!nome) return Swal.fire('Atenção', "Nome comercial é obrigatório", 'warning');
    if(nome.length < 3) return Swal.fire('Atenção', "Nome comercial muito curto.", 'warning');

    try {
        if (id) {
            await API.put(`/medicamentos/${id}`, { 
                nome_comercial: nome, 
                fabricante: fabricante 
            });
            Swal.fire('Sucesso', "Medicamento atualizado!", 'success');
        } else {
            await API.post('/medicamentos/', { 
                nome_comercial: nome, 
                fabricante: fabricante 
            });
            Swal.fire('Sucesso', "Medicamento cadastrado!", 'success');
        }
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('modalNovoMedicamento'));
        modal.hide();
        document.getElementById('formMedicamento').reset();
        document.getElementById('id_medicamento').value = '';
        carregarMedicamentos();
    } catch (e) {
        Swal.fire('Erro', "Erro: " + e.message, 'error');
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
    const result = await Swal.fire({
        title: 'Tem certeza?',
        text: "Deseja remover este medicamento?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Sim, remover!',
        cancelButtonText: 'Cancelar'
    });

    if(result.isConfirmed) {
        try {
            await API.delete(`/medicamentos/${id}`);
            carregarMedicamentos();
            Swal.fire('Removido!', 'Medicamento removido com sucesso.', 'success');
        } catch (e) {
            Swal.fire('Erro', "Erro: " + e.message, 'error');
        }
    }
}

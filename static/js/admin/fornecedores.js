document.addEventListener("DOMContentLoaded", () => {
    if (typeof Validation !== 'undefined') {
        Validation.applyMasks();
    }
    carregarFornecedores();
});

async function carregarFornecedores() {
    try {
        const lista = await API.get('/fornecedores/');
        const tbody = document.querySelector('#tabela-fornecedores tbody');
        tbody.innerHTML = '';
        
        if(lista.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">Nenhum fornecedor cadastrado.</td></tr>';
            return;
        }

        lista.forEach(f => {
            tbody.innerHTML += `
                <tr>
                    <td>${f.cnpj}</td>
                    <td>${f.nome_empresa || '-'}</td>
                    <td class="text-end">
                        <button class="btn btn-sm btn-outline-primary border-0 me-1" onclick="abrirModalEditar('${f.cnpj}', '${f.nome_empresa || ''}')">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger border-0" onclick="deletarFornecedor('${f.cnpj}')">
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

async function salvarFornecedor() {
    const cnpj = document.getElementById('cnpj').value.trim();
    const nome = document.getElementById('nome_empresa').value.trim();
    const isEdit = document.getElementById('is_edit').value === 'true';
    
    if(!cnpj) return Swal.fire('Atenção', "CNPJ é obrigatório", 'warning');
    if(!nome) return Swal.fire('Atenção', "Nome da empresa é obrigatório", 'warning');
    if(!Validation.isValidCNPJ(cnpj)) return Swal.fire('Erro', "CNPJ inválido (deve ter 14 dígitos)", 'error');

    try {
        if (isEdit) {
            await API.put(`/fornecedores/${cnpj}`, { nome_empresa: nome });
            Swal.fire('Sucesso', "Fornecedor atualizado!", 'success');
        } else {
            await API.post('/fornecedores/', { cnpj, nome_empresa: nome });
            Swal.fire('Sucesso', "Fornecedor cadastrado!", 'success');
        }
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('modalNovoFornecedor'));
        modal.hide();
        document.getElementById('formFornecedor').reset();
        document.getElementById('is_edit').value = 'false';
        document.getElementById('cnpj').readOnly = false;
        carregarFornecedores();
    } catch (e) {
        Swal.fire('Erro', "Erro: " + e.message, 'error');
    }
}

function abrirModalEditar(cnpj, nome) {
    document.getElementById('cnpj').value = cnpj;
    document.getElementById('nome_empresa').value = nome;
    document.getElementById('is_edit').value = 'true';
    document.getElementById('cnpj').readOnly = true;
    
    const modal = new bootstrap.Modal(document.getElementById('modalNovoFornecedor'));
    modal.show();
}

async function deletarFornecedor(cnpj) {
    const result = await Swal.fire({
        title: 'Tem certeza?',
        text: "Deseja remover este fornecedor?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Sim, remover!',
        cancelButtonText: 'Cancelar'
    });

    if(result.isConfirmed) {
        try {
            await API.delete(`/fornecedores/${cnpj}`);
            carregarFornecedores();
            Swal.fire('Removido!', 'Fornecedor removido com sucesso.', 'success');
        } catch (e) {
            Swal.fire('Erro', "Erro: " + e.message, 'error');
        }
    }
}
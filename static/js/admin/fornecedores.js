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
    
    if(!cnpj) return alert("CNPJ é obrigatório");
    if(!nome) return alert("Nome da empresa é obrigatório");
    if(!Validation.isValidCNPJ(cnpj)) return alert("CNPJ inválido (deve ter 14 dígitos)");

    try {
        if (isEdit) {
            await API.put(`/fornecedores/${cnpj}`, { nome_empresa: nome });
            alert("Fornecedor atualizado!");
        } else {
            await API.post('/fornecedores/', { cnpj, nome_empresa: nome });
            alert("Fornecedor cadastrado!");
        }
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('modalNovoFornecedor'));
        modal.hide();
        document.getElementById('formFornecedor').reset();
        document.getElementById('is_edit').value = 'false';
        document.getElementById('cnpj').readOnly = false;
        carregarFornecedores();
    } catch (e) {
        alert("Erro: " + e.message);
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
    if(confirm("Remover fornecedor?")) {
        try {
            await API.delete(`/fornecedores/${cnpj}`);
            carregarFornecedores();
        } catch (e) {
            alert("Erro: " + e.message);
        }
    }
}
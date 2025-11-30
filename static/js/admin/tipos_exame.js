document.addEventListener("DOMContentLoaded", carregarTipos);

async function carregarTipos() {
    try {
        const lista = await API.get('/tipos-exame/');
        const tbody = document.querySelector('#tabela-tipos tbody');
        tbody.innerHTML = '';
        
        if(lista.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">Nenhum tipo cadastrado.</td></tr>';
            return;
        }

        lista.forEach(t => {
            const preco = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(t.preco);
            tbody.innerHTML += `
                <tr>
                    <td>${t.id_tipo_exame}</td>
                    <td class="fw-bold">${t.nome_do_exame}</td>
                    <td>${preco}</td>
                    <td class="small text-muted">${t.descricao || '-'}</td>
                    <td class="text-end">
                        <button class="btn btn-sm btn-outline-primary border-0 me-1" onclick="abrirModalEditar(${t.id_tipo_exame}, '${t.nome_do_exame}', ${t.preco}, '${t.descricao || ''}')">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger border-0" onclick="deletarTipo(${t.id_tipo_exame})">
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

async function salvarTipo() {
    const id = document.getElementById('id_tipo_exame').value;
    const nome = document.getElementById('nome_exame').value.trim();
    const precoVal = document.getElementById('preco').value;
    const preco = parseFloat(precoVal);
    const descricao = document.getElementById('descricao').value.trim();
    
    if(!nome || !precoVal) return alert("Preencha os campos obrigatórios");
    if(preco <= 0) return alert("O preço deve ser maior que zero.");

    try {
        if (id) {
            await API.put(`/tipos-exame/${id}`, { 
                nome_do_exame: nome, 
                preco: parseFloat(preco),
                descricao: descricao 
            });
            alert("Tipo de exame atualizado!");
        } else {
            await API.post('/tipos-exame/', { 
                nome_do_exame: nome, 
                preco: parseFloat(preco),
                descricao: descricao 
            });
            alert("Tipo de exame cadastrado!");
        }
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('modalNovoTipo'));
        modal.hide();
        document.getElementById('formTipo').reset();
        document.getElementById('id_tipo_exame').value = '';
        carregarTipos();
    } catch (e) {
        alert("Erro: " + e.message);
    }
}

function abrirModalEditar(id, nome, preco, descricao) {
    document.getElementById('id_tipo_exame').value = id;
    document.getElementById('nome_exame').value = nome;
    document.getElementById('preco').value = preco;
    document.getElementById('descricao').value = descricao;
    
    const modal = new bootstrap.Modal(document.getElementById('modalNovoTipo'));
    modal.show();
}

async function deletarTipo(id) {
    if(confirm("Remover este tipo de exame?")) {
        try {
            await API.delete(`/tipos-exame/${id}`);
            carregarTipos();
        } catch (e) {
            alert("Erro: " + e.message);
        }
    }
}
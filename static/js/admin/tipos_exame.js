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
    
    if(!nome || !precoVal) return Swal.fire('Atenção', "Preencha os campos obrigatórios", 'warning');
    if(preco <= 0) return Swal.fire('Atenção', "O preço deve ser maior que zero.", 'warning');

    try {
        if (id) {
            await API.put(`/tipos-exame/${id}`, { 
                nome_do_exame: nome, 
                preco: parseFloat(preco),
                descricao: descricao 
            });
            Swal.fire('Sucesso', "Tipo de exame atualizado!", 'success');
        } else {
            await API.post('/tipos-exame/', { 
                nome_do_exame: nome, 
                preco: parseFloat(preco),
                descricao: descricao 
            });
            Swal.fire('Sucesso', "Tipo de exame cadastrado!", 'success');
        }
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('modalNovoTipo'));
        modal.hide();
        document.getElementById('formTipo').reset();
        document.getElementById('id_tipo_exame').value = '';
        carregarTipos();
    } catch (e) {
        Swal.fire('Erro', "Erro: " + e.message, 'error');
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
    const result = await Swal.fire({
        title: 'Tem certeza?',
        text: "Deseja remover este tipo de exame?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Sim, remover!',
        cancelButtonText: 'Cancelar'
    });

    if(result.isConfirmed) {
        try {
            await API.delete(`/tipos-exame/${id}`);
            carregarTipos();
            Swal.fire('Removido!', 'Tipo de exame removido com sucesso.', 'success');
        } catch (e) {
            Swal.fire('Erro', "Erro: " + e.message, 'error');
        }
    }
}
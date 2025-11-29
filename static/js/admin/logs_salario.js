document.addEventListener("DOMContentLoaded", () => {
    carregarLogs();
    
    const buscaInput = document.getElementById('busca-crm');
    let timeout = null;
    
    buscaInput.addEventListener('input', (e) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            carregarLogs(e.target.value);
        }, 500);
    });
});

async function carregarLogs(crm = '') {
    try {
        const url = crm ? `/logs-salario/?crm=${crm}` : '/logs-salario/';
        const logs = await API.get(url);
        const tbody = document.querySelector('#tabela-logs tbody');
        tbody.innerHTML = '';
        
        if(logs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">Nenhum registro encontrado.</td></tr>';
            return;
        }

        logs.forEach(log => {
            const data = new Date(log.data_alteracao).toLocaleString('pt-BR');
            const antigo = parseFloat(log.salario_antigo);
            const novo = parseFloat(log.salario_novo);
            const diff = novo - antigo;
            
            const fmt = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
            const diffClass = diff >= 0 ? 'text-success' : 'text-danger';
            const diffIcon = diff >= 0 ? 'bi-arrow-up' : 'bi-arrow-down';

            tbody.innerHTML += `
                <tr>
                    <td>${data}</td>
                    <td class="fw-bold">${log.nome_medico}</td>
                    <td><span class="badge bg-light text-dark border">${log.crm_medico}</span></td>
                    <td>${fmt.format(antigo)}</td>
                    <td>${fmt.format(novo)}</td>
                    <td class="${diffClass}">
                        <i class="bi ${diffIcon} me-1"></i>${fmt.format(diff)}
                    </td>
                </tr>
            `;
        });
    } catch (e) {
        console.error(e);
        document.querySelector('#tabela-logs tbody').innerHTML = 
            '<tr><td colspan="6" class="text-center text-danger">Erro ao carregar logs.</td></tr>';
    }
}

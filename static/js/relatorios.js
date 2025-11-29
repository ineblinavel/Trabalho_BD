document.addEventListener("DOMContentLoaded", () => {
    // Define ano atual como padrão
    document.getElementById("filtro-ano").value = new Date().getFullYear();
    carregarRelatorio();
});

async function carregarRelatorio() {
    const tbody = document.getElementById("tabela-relatorios");
    const ano = document.getElementById("filtro-ano").value;
    
    let url = "/relatorios/faturamento";
    if (ano) url += `?ano=${ano}`;

    try {
        const dados = await API.get(url);
        tbody.innerHTML = "";
        
        if (dados.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center py-4 text-muted">Nenhum registro encontrado.</td></tr>';
            document.getElementById("total-geral").textContent = "R$ 0,00";
            return;
        }

        let totalGeral = 0;

        dados.forEach(item => {
            const valor = parseFloat(item.total);
            totalGeral += valor;
            
            const valorFormatado = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);
            const mesNome = new Date(2000, item.mes - 1).toLocaleString('pt-BR', { month: 'long' });

            const tr = `
                <tr>
                    <td class="ps-4">${item.ano}</td>
                    <td class="text-capitalize">${mesNome}</td>
                    <td><span class="badge bg-light text-dark border">${item.tipo}</span></td>
                    <td class="text-end pe-4 fw-bold text-success">${valorFormatado}</td>
                </tr>
            `;
            tbody.innerHTML += tr;
        });

        document.getElementById("total-geral").textContent = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(totalGeral);

    } catch (error) {
        console.error(error);
        tbody.innerHTML = `<tr><td colspan="4" class="text-center text-danger">Erro ao carregar: ${error.message}</td></tr>`;
    }
}

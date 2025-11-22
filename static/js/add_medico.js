document.getElementById('add-medico-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const form = event.target;
    const crm = form.crm.value;
    const nome_medico = form.nome_medico.value;
    const cpf = form.cpf.value;
    const salario = form.salario.value;
    const messageDiv = document.getElementById('message');

    // Clear previous messages
    messageDiv.textContent = '';
    messageDiv.className = '';

    try {
        const response = await fetch('/medicos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ crm, nome_medico, cpf, salario })
        });

        const result = await response.json();

        if (response.ok) {
            messageDiv.className = 'success';
            messageDiv.textContent = result.message || 'Médico adicionado com sucesso!';
            form.reset();
        } else {
            messageDiv.className = 'error';
            messageDiv.textContent = 'Erro: ' + (result.error || 'Ocorreu um problema ao adicionar o médico.');
        }
    } catch (error) {
        messageDiv.className = 'error';
        messageDiv.textContent = 'Erro de conexão: ' + error.message;
    }
});

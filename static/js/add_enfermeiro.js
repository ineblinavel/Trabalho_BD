document.addEventListener('DOMContentLoaded', () => {
    if (typeof Validation !== 'undefined') {
        Validation.applyMasks();
    }
});

document.getElementById('add-enfermeiro-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const form = event.target;
    const corem = form.corem.value.trim();
    const nome_enfermeiro = form.nome_enfermeiro.value.trim();
    const cpf = form.cpf.value.trim();
    const messageDiv = document.getElementById('message');

    // Clear previous messages
    messageDiv.textContent = '';
    messageDiv.className = '';

    if (!corem || !nome_enfermeiro || !cpf) {
        messageDiv.className = 'alert alert-danger';
        messageDiv.textContent = 'Preencha todos os campos.';
        return;
    }

    if (!Validation.isValidCPF(cpf)) {
        messageDiv.className = 'alert alert-danger';
        messageDiv.textContent = 'CPF inválido.';
        return;
    }

    try {
        const response = await fetch('/enfermeiros', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ corem, nome_enfermeiro, cpf })
        });

        const result = await response.json();

        if (response.ok) {
            messageDiv.className = 'alert alert-success';
            let msg = result.message || 'Enfermeiro adicionado com sucesso!';
            if (result.senha_gerada) {
                msg += `<br><strong>Usuário criado!</strong><br>Login: ${corem}<br>Senha: <code>${result.senha_gerada}</code>`;
            }
            messageDiv.innerHTML = msg;
            form.reset();
        } else {
            messageDiv.className = 'alert alert-danger';
            messageDiv.textContent = 'Erro: ' + (result.error || 'Ocorreu um problema ao adicionar o enfermeiro.');
        }
    } catch (error) {
        messageDiv.className = 'alert alert-danger';
        messageDiv.textContent = 'Erro de conexão: ' + error.message;
    }
});

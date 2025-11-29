document.addEventListener("DOMContentLoaded", async () => {
    await carregarOpcoes();
});

async function carregarOpcoes() {
    try {
        const [pacientes, medicos] = await Promise.all([
            API.get("/pacientes/"),
            API.get("/medicos/medicos")
        ]);

        const selPac = document.getElementById("select-paciente");
        selPac.innerHTML = '<option value="" selected disabled>Selecione o paciente...</option>';
        pacientes.forEach(p => {
            selPac.innerHTML += `<option value="${p.id_paciente}">${p.nome_paciente} (CPF: ${p.cpf})</option>`;
        });

        const selMed = document.getElementById("select-medico");
        selMed.innerHTML = '<option value="" selected disabled>Selecione o médico...</option>';
        medicos.forEach(m => {
            selMed.innerHTML += `<option value="${m.crm}">${m.nome_medico} - ${m.crm}</option>`;
        });

    } catch (error) {
        console.error(error);
        alert("Erro ao carregar listas: " + error.message);
    }
}

document.getElementById("form-consulta").addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    // Formata a data para o formato esperado pelo backend se necessário
    // O input datetime-local envia 'YYYY-MM-DDTHH:MM', o backend espera 'YYYY-MM-DD HH:MM:SS'
    if (data.data_hora_agendamento) {
        data.data_hora_agendamento = data.data_hora_agendamento.replace('T', ' ') + ':00';
    }

    try {
        await API.post("/consultas/", data);
        alert("Consulta agendada com sucesso!");
        window.location.href = "/ui/portal/enfermeiro";
    } catch (error) {
        alert("Erro ao agendar consulta: " + error.message);
    }
});

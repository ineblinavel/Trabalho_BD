document.addEventListener("DOMContentLoaded", async () => {
    document.getElementById("data_resultado").valueAsDate = new Date();
    document.getElementById("data_solicitacao").valueAsDate = new Date();
    
    await carregarExames();
    await carregarOpcoesSolicitacao();
});

async function carregarExames() {
    const tbody = document.getElementById("tabela-exames");
    try {
        const exames = await API.get("/exames/");
        
        // Para pegar nomes, precisaríamos de um endpoint que retorne detalhes ou fazer join no front
        // O endpoint /exames/ retorna lista simples. Vamos assumir que retorna detalhes ou faremos fetch extra se precisar.
        // O ExameRepository.find_all retorna SELECT * FROM Exame. Não tem nomes.
        // O ideal seria alterar o backend para retornar nomes, mas vamos trabalhar com o que temos.
        // Vamos buscar detalhes de cada um? Não, muito pesado.
        // Vamos buscar lista de pacientes e tipos para mapear.
        
        const [pacientes, tipos] = await Promise.all([
            API.get("/pacientes/"),
            API.get("/tipos-exame/") // Assumindo que existe essa rota
        ]);
        
        const mapPacientes = {};
        pacientes.forEach(p => mapPacientes[p.id_paciente] = p.nome_paciente);
        
        const mapTipos = {};
        tipos.forEach(t => mapTipos[t.id_tipo_exame] = t.nome_do_exame);

        tbody.innerHTML = "";
        
        if (exames.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-muted">Nenhum exame encontrado.</td></tr>';
            return;
        }

        exames.forEach(exame => {
            const nomePaciente = mapPacientes[exame.id_paciente] || `ID: ${exame.id_paciente}`;
            const nomeExame = mapTipos[exame.id_tipo_exame] || `ID: ${exame.id_tipo_exame}`;
            
            let statusBadge = '';
            let actionBtn = '';
            
            if (exame.status === 'R') {
                statusBadge = '<span class="badge bg-success">Realizado</span>';
                actionBtn = '<button class="btn btn-sm btn-outline-secondary" disabled>Concluído</button>';
            } else {
                statusBadge = '<span class="badge bg-warning text-dark">Pendente</span>';
                actionBtn = `<button class="btn btn-sm btn-outline-primary" onclick="abrirModalResultado(${exame.id_exame})">
                                <i class="bi bi-pencil-square me-1"></i> Resultado
                             </button>`;
            }

            const tr = `
                <tr>
                    <td class="ps-4 fw-bold">#${exame.id_exame}</td>
                    <td>${nomePaciente}</td>
                    <td>${nomeExame}</td>
                    <td>${new Date(exame.data_solicitacao).toLocaleDateString('pt-BR', {timeZone: 'UTC'})}</td>
                    <td>${statusBadge}</td>
                    <td class="text-end pe-4">${actionBtn}</td>
                </tr>
            `;
            tbody.innerHTML += tr;
        });

    } catch (error) {
        console.error(error);
        tbody.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Erro ao carregar: ${error.message}</td></tr>`;
    }
}

async function carregarOpcoesSolicitacao() {
    try {
        const [pacientes, medicos, tipos] = await Promise.all([
            API.get("/pacientes/"),
            API.get("/medicos/medicos"),
            API.get("/tipos-exame/")
        ]);

        const selPac = document.getElementById("select-paciente");
        pacientes.forEach(p => selPac.innerHTML += `<option value="${p.id_paciente}">${p.nome_paciente}</option>`);

        const selMed = document.getElementById("select-medico");
        medicos.forEach(m => selMed.innerHTML += `<option value="${m.crm}">${m.nome_medico}</option>`);

        const selTipo = document.getElementById("select-tipo-exame");
        tipos.forEach(t => selTipo.innerHTML += `<option value="${t.id_tipo_exame}">${t.nome_do_exame}</option>`);

    } catch (error) {
        console.error("Erro ao carregar opções do modal", error);
    }
}

window.abrirModalResultado = function(idExame) {
    document.getElementById("id_exame_resultado").value = idExame;
    const modal = new bootstrap.Modal(document.getElementById("modalRegistrarResultado"));
    modal.show();
}

document.getElementById("form-resultado").addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    try {
        await API.post("/resultados-exame/", data);
        alert("Resultado registrado com sucesso!");
        location.reload();
    } catch (error) {
        alert("Erro ao registrar resultado: " + error.message);
    }
});

document.getElementById("form-solicitar").addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    try {
        await API.post("/exames/", data);
        alert("Exame solicitado com sucesso!");
        location.reload();
    } catch (error) {
        alert("Erro ao solicitar exame: " + error.message);
    }
});

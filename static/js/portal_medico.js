document.addEventListener("DOMContentLoaded", async () => {
    const crm = document.getElementById("medico-data").dataset.crm;
    if (!crm || crm === 'None') {
        document.getElementById("agenda-container").innerHTML = `
            <div class="text-center py-5">
                <i class="bi bi-exclamation-circle text-warning icon-lg mb-3"></i>
                <p class="text-muted">CRM não identificado na sessão. Por favor, faça login novamente.</p>
            </div>
        `;
        return;
    }

    await carregarAgenda(crm);
    await carregarConsultas(crm);
    carregarTiposExame();
});

async function carregarAgenda(crm) {
    const container = document.getElementById("agenda-container");
    
    try {
        // Busca as agendas do médico
        const agendas = await API.get(`/agenda/medico/${crm}`);
        
        if (agendas.length === 0) {
            container.innerHTML = `
                <div class="text-center py-5">
                    <i class="bi bi-calendar-x text-muted icon-lg mb-3"></i>
                    <p class="text-muted">Nenhuma agenda configurada para este CRM.</p>
                </div>
            `;
            return;
        }

        // Se tiver agendas, vamos mostrar a mais recente ou listar todas
        // Por simplicidade, vamos listar cards simples
        let html = '<div class="list-group list-group-flush text-start">';
        
        agendas.forEach(agenda => {
            const dataFmt = new Date(agenda.data).toLocaleDateString('pt-BR', {timeZone: 'UTC'});
            html += `
                <div class="list-group-item py-3">
                    <div class="d-flex w-100 justify-content-between">
                        <h5 class="mb-1"><i class="bi bi-calendar-date me-2"></i>${dataFmt}</h5>
                        <small class="text-muted">${agenda.inicio_platao} - ${agenda.fim_platao}</small>
                    </div>
                    <p class="mb-1">Plantão com slots de ${agenda.duracao_slot_minutos} minutos.</p>
                    <small class="text-primary cursor-pointer" onclick="verSlots(${agenda.id_agenda})">Ver horários disponíveis</small>
                    <div id="slots-${agenda.id_agenda}" class="mt-2 d-none"></div>
                </div>
            `;
        });
        html += '</div>';
        
        container.innerHTML = html;
        container.classList.remove('text-center', 'py-5', 'bg-light'); // Remove estilos de placeholder

    } catch (error) {
        console.error(error);
        container.innerHTML = `
            <div class="text-center py-5 text-danger">
                <p>Erro ao carregar agenda: ${error.message}</p>
            </div>
        `;
    }
}

async function verSlots(idAgenda) {
    const container = document.getElementById(`slots-${idAgenda}`);
    if (!container.classList.contains('d-none')) {
        container.classList.add('d-none');
        return;
    }
    
    container.innerHTML = '<div class="spinner-border spinner-border-sm text-primary"></div> Carregando...';
    container.classList.remove('d-none');

    try {
        const slots = await API.get(`/agenda/${idAgenda}/slots`);
        
        if (slots.length === 0) {
            container.innerHTML = '<small class="text-muted">Nenhum horário disponível.</small>';
            return;
        }

        let badges = '';
        slots.forEach(slot => {
            // Corta os segundos HH:MM:SS -> HH:MM
            const hora = slot.substring(0, 5);
            badges += `<span class="badge bg-success me-1 mb-1">${hora}</span>`;
        });
        
        container.innerHTML = `<div class="d-flex flex-wrap">${badges}</div>`;
        
    } catch (error) {
        container.innerHTML = '<small class="text-danger">Erro ao carregar slots.</small>';
    }
}

async function carregarConsultas(crm) {
    const container = document.getElementById("consultas-container");
    try {
        const consultas = await API.get(`/consultas/medico/${crm}`);
        
        if (consultas.length === 0) {
            container.innerHTML = '<p class="text-muted text-center py-3">Nenhuma consulta agendada.</p>';
            container.classList.remove('bg-light');
            return;
        }

        let html = '<div class="list-group list-group-flush">';
        consultas.forEach(c => {
            const data = new Date(c.data_hora_agendamento).toLocaleString('pt-BR');
            html += `
                <div class="list-group-item px-0 py-3">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-1">${c.nome_paciente}</h6>
                            <small class="text-muted"><i class="bi bi-clock me-1"></i>${data}</small>
                        </div>
                        <button class="btn btn-sm btn-outline-primary" onclick="abrirModalExame(${c.id_consulta})">
                            <i class="bi bi-file-medical me-1"></i> Solicitar Exame
                        </button>
                    </div>
                </div>
            `;
        });
        html += '</div>';
        
        container.innerHTML = html;
        container.classList.remove('text-center', 'py-5', 'bg-light');
    } catch (error) {
        console.error(error);
        container.innerHTML = `<p class="text-danger text-center">Erro ao carregar consultas: ${error.message}</p>`;
    }
}

async function carregarTiposExame() {
    try {
        const tipos = await API.get('/tipos-exame/');
        const select = document.getElementById('tipo_exame_select');
        select.innerHTML = '<option value="">Selecione um exame...</option>';
        tipos.forEach(t => {
            select.innerHTML += `<option value="${t.id_tipo_exame}">${t.nome_do_exame}</option>`;
        });
    } catch (e) {
        console.error("Erro ao carregar tipos de exame", e);
    }
}

function abrirModalExame(idConsulta) {
    document.getElementById('id_consulta_exame').value = idConsulta;
    new bootstrap.Modal(document.getElementById('modalSolicitarExame')).show();
}

async function confirmarSolicitacaoExame() {
    const idConsulta = document.getElementById('id_consulta_exame').value;
    const idTipo = document.getElementById('tipo_exame_select').value;
    
    if (!idTipo) return alert("Selecione um tipo de exame.");

    try {
        await API.post('/exames/', {
            id_consulta: parseInt(idConsulta),
            id_tipo_exame: parseInt(idTipo)
        });
        alert("Exame solicitado com sucesso!");
        bootstrap.Modal.getInstance(document.getElementById('modalSolicitarExame')).hide();
    } catch (error) {
        alert("Erro ao solicitar exame: " + error.message);
    }
}

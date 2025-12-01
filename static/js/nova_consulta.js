document.addEventListener("DOMContentLoaded", async () => {
  await carregarOpcoes();
  
  // Listeners para carregar horários
  document.getElementById('select-medico').addEventListener('change', carregarHorarios);
  document.getElementById('data_consulta').addEventListener('change', carregarHorarios);
});

async function carregarOpcoes() {
  try {
    const [pacientes, medicos] = await Promise.all([
      API.get("/pacientes/"),
      API.get("/medicos/medicos"),
    ]);

    const selPac = document.getElementById("select-paciente");
    selPac.innerHTML =
      '<option value="" selected disabled>Selecione o paciente...</option>';
    pacientes.forEach((p) => {
      selPac.innerHTML += `<option value="${p.id_paciente}">${p.nome_paciente} (CPF: ${p.cpf})</option>`;
    });

    const selMed = document.getElementById("select-medico");
    selMed.innerHTML =
      '<option value="" selected disabled>Selecione o médico...</option>';
    medicos.forEach((m) => {
      selMed.innerHTML += `<option value="${m.crm}">${m.nome_medico} - ${m.crm}</option>`;
    });
  } catch (error) {
    console.error(error);
    alert("Erro ao carregar listas: " + error.message);
  }
}

async function carregarHorarios() {
    const crm = document.getElementById('select-medico').value;
    const data = document.getElementById('data_consulta').value;
    const selectHora = document.getElementById('hora_consulta');

    if (!crm || !data) {
        selectHora.innerHTML = '<option value="" selected disabled>Selecione médico e data...</option>';
        selectHora.disabled = true;
        return;
    }

    selectHora.innerHTML = '<option value="" selected disabled>Carregando...</option>';
    selectHora.disabled = true;

    try {
        // 1. Busca a agenda do médico para a data
        const agenda = await API.get(`/agenda/medico/${crm}/data/${data}`);
        
        if (agenda.error) {
            selectHora.innerHTML = '<option value="" selected disabled>Sem agenda para esta data</option>';
            return;
        }

        // 2. Busca os slots disponíveis dessa agenda
        const slots = await API.get(`/agenda/${agenda.id_agenda}/slots`);

        if (slots.length === 0) {
            selectHora.innerHTML = '<option value="" selected disabled>Nenhum horário livre</option>';
            return;
        }

        selectHora.innerHTML = '<option value="" selected disabled>Selecione um horário...</option>';
        slots.forEach(hora => {
            // hora vem como "HH:MM:SS"
            const horaCurta = hora.substring(0, 5);
            selectHora.innerHTML += `<option value="${hora}">${horaCurta}</option>`;
        });
        selectHora.disabled = false;

    } catch (error) {
        console.error(error);
        selectHora.innerHTML = '<option value="" selected disabled>Indisponível nesta data</option>';
    }
}

document
  .getElementById("form-consulta")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const idPaciente = document.getElementById('select-paciente').value;
    const crm = document.getElementById('select-medico').value;
    const data = document.getElementById('data_consulta').value;
    const hora = document.getElementById('hora_consulta').value;

    if (!idPaciente || !crm || !data || !hora) {
        return alert("Preencha todos os campos.");
    }

    const dataHoraAgendamento = `${data} ${hora}`;

    const payload = {
        id_paciente: idPaciente,
        crm_medico: crm,
        data_hora_agendamento: dataHoraAgendamento
    };

    try {
      // 1. Faz a requisição
      const response = await API.post("/consultas/", payload);

      // 2. VERIFICAÇÃO CRÍTICA
      if (response.error) {
        alert("Não foi possível agendar: " + response.error);
        return; 
      }

      // 3. Sucesso
      alert("Consulta agendada com sucesso!");
      window.location.href = "/ui/portal/enfermeiro"; // Redireciona para o painel
    } catch (error) {
      console.error(error);
      alert("Erro técnico ao agendar consulta: " + (error.message || error.error));
    }
  });

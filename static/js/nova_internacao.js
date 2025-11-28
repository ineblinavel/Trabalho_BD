document.addEventListener("DOMContentLoaded", async () => {
  // Define a data de hoje como padrão
  document.getElementById("data_admissao").valueAsDate = new Date();
  await carregarDados();
});

async function carregarDados() {
  try {
    // Carrega tudo em paralelo para ser rápido
    const [pacientes, medicos, enfermeiros, quartos] = await Promise.all([
      API.get("/pacientes/"),
      API.get("/medicos/medicos"),
      API.get("/enfermeiros/"),
      API.get("/quartos/mapa"), // Traz status ocupado/livre
    ]);

    // 1. Preencher Pacientes
    const selPac = document.getElementById("select-paciente");
    selPac.innerHTML =
      '<option value="" selected disabled>Selecione o paciente...</option>';
    pacientes.forEach((p) => {
      selPac.innerHTML += `<option value="${p.id_paciente}">${p.nome_paciente} (CPF: ${p.cpf})</option>`;
    });

    // 2. Preencher Médicos
    const selMed = document.getElementById("select-medico");
    selMed.innerHTML =
      '<option value="" selected disabled>Selecione o médico...</option>';
    medicos.forEach((m) => {
      selMed.innerHTML += `<option value="${m.crm}">${m.nome_medico} - ${m.crm}</option>`;
    });

    // 3. Preencher Enfermeiros
    const selEnf = document.getElementById("select-enfermeiro");
    selEnf.innerHTML =
      '<option value="" selected disabled>Selecione o enfermeiro...</option>';
    enfermeiros.forEach((e) => {
      selEnf.innerHTML += `<option value="${e.corem}">${e.nome_enfermeiro}</option>`;
    });

    // 4. Preencher Quartos (Apenas LIVRES)
    const selQuarto = document.getElementById("select-quarto");
    const quartosLivres = quartos.filter((q) => q.status_atual === "Livre");

    selQuarto.innerHTML =
      '<option value="" selected disabled>Selecione um leito...</option>';
    if (quartosLivres.length === 0) {
      selQuarto.innerHTML =
        "<option disabled>Nenhum leito disponível!</option>";
    } else {
      quartosLivres.forEach((q) => {
        const preco = new Intl.NumberFormat("pt-BR", {
          style: "currency",
          currency: "BRL",
        }).format(q.valor_diaria);
        selQuarto.innerHTML += `<option value="${q.id_quarto}">Quarto ${q.num_quarto} (${q.tipo_de_quarto}) - ${preco}</option>`;
      });
    }
  } catch (error) {
    console.error(error);
    alert("Erro ao carregar listas. Verifique o servidor.");
  }
}

document
  .getElementById("form-internacao")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    try {
      await API.post("/internacoes/", data);
      alert("Internação realizada com sucesso!");
      window.location.href = "/ui/quartos"; // Vai para o mapa ver o resultado
    } catch (error) {
      alert("Erro ao internar: " + error.message);
    }
  });

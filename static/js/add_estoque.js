document.addEventListener("DOMContentLoaded", async () => {
  await carregarOpcoes();
});

async function carregarOpcoes() {
  const selectMed = document.getElementById("select-medicamento");
  const selectForn = document.getElementById("select-fornecedor");

  try {
    // 1. Buscar Medicamentos e Fornecedores em paralelo
    const [medicamentos, fornecedores] = await Promise.all([
      API.get("/medicamentos/"),
      API.get("/fornecedores/"),
    ]);

    // 2. Preencher Select de Medicamentos
    selectMed.innerHTML =
      '<option value="" selected disabled>Selecione um medicamento...</option>';
    medicamentos.forEach((med) => {
      const option = document.createElement("option");
      option.value = med.id_medicamento;
      option.textContent = `${med.nome_comercial} (${
        med.fabricante || "Genérico"
      })`;
      selectMed.appendChild(option);
    });

    // 3. Preencher Select de Fornecedores
    selectForn.innerHTML =
      '<option value="" selected disabled>Selecione um fornecedor...</option>';
    fornecedores.forEach((forn) => {
      const option = document.createElement("option");
      option.value = forn.cnpj;
      option.textContent = `${forn.nome_empresa} - CNPJ: ${forn.cnpj}`;
      selectForn.appendChild(option);
    });
  } catch (error) {
    console.error("Erro ao carregar opções:", error);
    alert(
      "Erro ao carregar listas de medicamentos ou fornecedores. Verifique se eles estão cadastrados."
    );
  }
}

// Handler do Formulário
document
  .getElementById("form-estoque")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    // Transforma os dados do form em objeto
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    // Conversões necessárias para a API (strings para números)
    data.quantidade = parseInt(data.quantidade);
    data.preco_unitario = parseFloat(data.preco_unitario);
    data.id_medicamento = parseInt(data.id_medicamento);

    try {
      await API.post("/estoque/", data);
      alert("Item adicionado ao estoque com sucesso!");
      window.location.href = "/ui/estoque";
    } catch (error) {
      alert("Erro ao salvar: " + (error.message || "Verifique os dados."));
    }
  });

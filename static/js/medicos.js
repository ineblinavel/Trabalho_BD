document.addEventListener("DOMContentLoaded", () => {
  carregarMedicos();
});

async function carregarMedicos() {
  try {
    const medicos = await API.get("/medicos/medicos"); // Rota da sua API
    const tbody = document.querySelector("#tabela-medicos tbody");
    tbody.innerHTML = "";

    medicos.forEach((medico) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
                <td>${medico.crm}</td>
                <td>${medico.nome_medico}</td>
                <td>-</td>
                <td>
                    <button class="btn btn-sm btn-danger" onclick="deletarMedico('${medico.crm}')">Excluir</button>
                    </td>
            `;
      tbody.appendChild(tr);
    });
  } catch (error) {
    console.error("Erro ao carregar médicos:", error);
  }
}

async function deletarMedico(crm) {
  if (confirm("Tem certeza que deseja excluir este médico?")) {
    // Nota: Sua rota de delete precisa estar configurada corretamente no backend
    // Assumindo que você criará/ajustará a rota DELETE /medicos/<crm>
    // Atualmente seu backend usa ID ou CRM dependendo da rota. Verifique medicos_routes.py
    alert(
      "Funcionalidade de deletar precisa ser implementada na rota correta!"
    );
    // Exemplo: await API.delete(`/medicos/${crm}`);
    // carregarMedicos();
  }
}

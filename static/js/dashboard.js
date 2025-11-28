document.addEventListener("DOMContentLoaded", () => {
  carregarEstatisticas();
  verificarAlertas();
});

async function carregarEstatisticas() {
  try {
    // 1. Buscar Médicos
    // Nota: A rota no seu backend é /medicos/medicos para o GET ALL
    const medicos = await API.get("/medicos/medicos");
    animarNumero("total-medicos", medicos.length);

    // 2. Buscar Pacientes
    const pacientes = await API.get("/pacientes/");
    animarNumero("total-pacientes", pacientes.length);

    // 3. Buscar Internações Ativas
    // Nota: Certifique-se de ter aplicado a correção na rota /internacoes/ativas
    const internacoes = await API.get("/internacoes/ativas");
    animarNumero("total-internacoes", internacoes.length);
  } catch (error) {
    console.error("Erro ao carregar dashboard:", error);
  }
}

async function verificarAlertas() {
  try {
    // Verifica medicamentos vencidos
    const vencidos = await API.get("/estoque/vencidos");

    if (vencidos && vencidos.length > 0) {
      const alerta = document.getElementById("alerta-estoque");
      alerta.classList.remove("d-none");
      alerta.innerHTML = `<strong>Atenção:</strong> Existem ${vencidos.length} lotes de medicamentos vencidos no estoque! <a href="/ui/estoque" class="alert-link">Verificar</a>`;
    }
  } catch (error) {
    console.error("Erro ao verificar alertas:", error);
  }
}

// Função utilitária apenas para dar um efeito visual de contagem
function animarNumero(elementId, total) {
  const element = document.getElementById(elementId);
  element.textContent = total;
  // Se quiser animação complexa, pode adicionar lógica aqui
}

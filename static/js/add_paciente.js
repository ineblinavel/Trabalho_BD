document.addEventListener("DOMContentLoaded", () => {
  // Máscara simples para CPF (opcional, melhora UX)
  const cpfInput = document.getElementById("cpf");
  if (cpfInput) {
    cpfInput.addEventListener("input", function (e) {
      let value = e.target.value.replace(/\D/g, "");
      if (value.length > 11) value = value.slice(0, 11);

      if (value.length > 9) {
        value = value.replace(/^(\d{3})(\d{3})(\d{3})(\d{2}).*/, "$1.$2.$3-$4");
      } else if (value.length > 6) {
        value = value.replace(/^(\d{3})(\d{3})(\d{3}).*/, "$1.$2.$3");
      } else if (value.length > 3) {
        value = value.replace(/^(\d{3})(\d{3}).*/, "$1.$2");
      }
      e.target.value = value;
    });
  }
});

document
  .getElementById("form-paciente")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    // Captura os dados do formulário
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    // Desabilita o botão para evitar duplo clique
    const btnSubmit = e.target.querySelector('button[type="submit"]');
    const textoOriginal = btnSubmit.innerHTML;
    btnSubmit.disabled = true;
    btnSubmit.innerHTML =
      '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Salvando...';

    try {
      // Envia para a API (Endpoint definido em paciente_routes.py)
      await API.post("/pacientes/", data);

      // Sucesso
      alert("Paciente cadastrado com sucesso!");
      window.location.href = "/ui/pacientes"; // Redireciona para a lista
    } catch (error) {
      // Erro
      console.error("Erro ao cadastrar:", error);
      alert(
        "Erro ao salvar paciente: " +
          (error.message || "Verifique os dados e tente novamente.")
      );

      // Reabilita o botão em caso de erro
      btnSubmit.disabled = false;
      btnSubmit.innerHTML = textoOriginal;
    }
  });

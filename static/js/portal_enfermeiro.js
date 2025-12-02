document.addEventListener("DOMContentLoaded", () => {
  const personal = document.getElementById("personal-info-enf");
  if (personal) {
    const corem = personal.dataset.corem;
    carregarTelefonesEnfermeiro(corem);

    document
      .getElementById("btn-add-telefone-enfermeiro")
      .addEventListener("click", async (e) => {
        e.preventDefault();
        const input = document.getElementById("novo-telefone-enfermeiro");
        const numero = input.value.trim();
        if (!numero) return alert("Digite um número válido");
        try {
          await API.post("/telefones/enfermeiros/", {
            corem_enfermeiro: corem,
            numero_telefone: numero,
          });
          input.value = "";
          carregarTelefonesEnfermeiro(corem);
        } catch (err) {
          alert(
            "Erro ao adicionar telefone: " +
              (err.message || JSON.stringify(err))
          );
        }
      });
  }
});

async function carregarTelefonesEnfermeiro(corem) {
  const ul = document.getElementById("lista-telefones-enfermeiro");
  if (!ul) return;
  ul.innerHTML = '<li class="list-group-item text-muted">Carregando...</li>';
  try {
    const lista = await API.get(`/telefones/enfermeiros/${corem}`);
    renderListaTelefonesEnfermeiro(lista || []);
  } catch (err) {
    ul.innerHTML = `<li class="list-group-item text-danger">Erro ao carregar: ${
      err.message || err
    }</li>`;
  }
}

function renderListaTelefonesEnfermeiro(lista) {
  const ul = document.getElementById("lista-telefones-enfermeiro");
  ul.innerHTML = "";
  if (!lista || lista.length === 0) {
    ul.innerHTML =
      '<li class="list-group-item text-muted">Nenhum telefone cadastrado.</li>';
    return;
  }

  lista.forEach((t) => {
    const li = document.createElement("li");
    li.className =
      "list-group-item d-flex justify-content-between align-items-center";
    li.innerHTML = `
            <span class="me-3">${t.numero_telefone}</span>
            <div class="btn-group btn-group-sm" role="group">
                <button class="btn btn-outline-secondary" onclick="editarTelefoneEnfermeiro(${
                  t.id_telefone_enfermeiro
                }, '${t.numero_telefone.replace(/'/g, "\\'")}')">Editar</button>
                <button class="btn btn-danger" onclick="removerTelefoneEnfermeiro(${
                  t.id_telefone_enfermeiro
                })">Remover</button>
            </div>
        `;
    ul.appendChild(li);
  });
}

async function removerTelefoneEnfermeiro(id) {
  if (!confirm("Remover telefone?")) return;
  try {
    await API.delete(`/telefones/enfermeiros/${id}`);
    const corem = document.getElementById("personal-info-enf").dataset.corem;
    carregarTelefonesEnfermeiro(corem);
  } catch (err) {
    alert("Erro ao remover: " + (err.message || JSON.stringify(err)));
  }
}

async function editarTelefoneEnfermeiro(id, atual) {
  const novo = prompt("Editar telefone:", atual);
  if (novo === null) return;
  try {
    await API.put(`/telefones/enfermeiros/${id}`, { numero_telefone: novo });
    const corem = document.getElementById("personal-info-enf").dataset.corem;
    carregarTelefonesEnfermeiro(corem);
  } catch (err) {
    alert("Erro ao editar: " + (err.message || JSON.stringify(err)));
  }
}

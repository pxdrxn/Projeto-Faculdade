const API = "http://localhost:8000";
const token = localStorage.getItem("token");

if (!token) {
  window.location.href = "index.html";
}

// Função para mostrar um carregando enquanto a requisição é feita
function showLoading(message) {
  const div = document.getElementById("problemas");
  div.innerHTML = `<p>${message}</p>`;
}

// Função para renderizar os problemas de forma mais bonita
function renderProblemas(problemas) {
  const div = document.getElementById("problemas");
  div.innerHTML = ''; // Limpa qualquer conteúdo anterior
  if (problemas.length > 0) {
    problemas.forEach(p => {
      const item = document.createElement("div");
      item.classList.add("problema-card");
      item.innerHTML = `
        <h3>${p.tipo_de_aparelho} (${p.marca})</h3>
        <p><strong>Descrição:</strong> ${p.descricao}</p>
        <p><strong>Telefone do Cliente:</strong> ${p.cliente_telefone ? p.cliente_telefone : 'N/A'}</p>
        <hr/>
      `;
      div.appendChild(item);
    });
  } else {
    div.innerHTML = "<p>Nenhum problema encontrado.</p>";
  }
}

// Função para buscar problemas da API
function fetchProblemas() {
  showLoading('Carregando problemas...');
  fetch(`${API}/problemas`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  .then(res => res.json())
  .then(data => {
    if (Array.isArray(data)) {
      renderProblemas(data);
    } else {
      document.getElementById("problemas").innerHTML = "Erro ao carregar problemas.";
    }
  })
  .catch(err => {
    console.error('Erro ao carregar problemas:', err);
    document.getElementById("problemas").innerHTML = "Erro ao conectar com o servidor.";
  });
}

// Chama a função para carregar os problemas assim que a página carrega
if (document.getElementById("problemas")) {
  fetchProblemas();
}

// Formulário de criação de problema
document.getElementById("problema-form")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const problema = {
    tipo_de_aparelho: document.getElementById("tipo_de_aparelho").value,
    marca: document.getElementById("marca").value,
    descricao: document.getElementById("descricao").value,
  };

  try {
    const res = await fetch(`${API}/problemas`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(problema),
    });

    if (res.ok) {
      alert("Problema criado com sucesso!");
      window.location.href = "problemas.html";
    } else {
      const data = await res.json();
      alert(data.detail || "Erro ao criar problema");
    }
  } catch (err) {
    console.error('Erro ao criar problema:', err);
    alert('Erro ao se conectar com o servidor.');
  }
});

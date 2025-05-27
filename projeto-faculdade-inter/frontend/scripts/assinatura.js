const API = "http://localhost:8000";
const token = localStorage.getItem("token");

if (!token) window.location.href = "index.html";

async function criarAssinatura() {
  const res = await fetch(`${API}/assinaturas`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await res.json();

  if (res.ok) {
    alert("Assinatura criada com sucesso!");
    window.location.href = "problemas.html";
  } else {
    alert(data.detail || "Erro ao criar assinatura");
  }
}
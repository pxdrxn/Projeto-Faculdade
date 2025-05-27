const API = "http://localhost:8000";

document.getElementById("login-form")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch(`${API}/login`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ email, password }),
  });

  const data = await res.json();
  if (res.ok) {
    localStorage.setItem("token", data.access_token);
    window.location.href = "problemas.html";
  } else {
    alert(data.detail || "Erro ao fazer login");
  }
});

document.getElementById("register-form")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const user = {
    username: document.getElementById("username").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
    telefone: document.getElementById("telefone").value,
    tipo_usuario: document.getElementById("tipo_usuario").value,
  };

  const res = await fetch(`${API}/register`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(user),
  });

  if (res.ok) {
    alert("Conta criada com sucesso!");
    window.location.href = "index.html";
  } else {
    const data = await res.json();
    alert(data.detail || "Erro ao registrar");
  }
});

function logout() {
  localStorage.removeItem("token");
}
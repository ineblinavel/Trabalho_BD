// static/js/api.js
const API = {
  get: async (url) => {
    const response = await fetch(url);
    if (!response.ok) throw new Error("Erro ao carregar dados");
    return await response.json();
  },
  post: async (url, data) => {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    return await response.json();
  },
  put: async (url, data) => {
    const response = await fetch(url, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    return await response.json();
  },
  delete: async (url) => {
    const response = await fetch(url, { method: "DELETE" });
    return await response.json();
  },
};

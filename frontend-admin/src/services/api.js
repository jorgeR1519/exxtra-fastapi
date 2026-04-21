import axios from "axios";
import { getSession } from "./session";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const session = getSession();
  if (session?.access_token) {
    config.headers.Authorization = `Bearer ${session.access_token}`;
  }
  return config;
});

export async function login(payload) {
  const response = await api.post("/auth/login", payload);
  return response.data;
}

export async function register(payload) {
  const response = await api.post("/auth/register", payload);
  return response.data;
}

export async function fetchUsers(search = "") {
  const response = await api.get("/usuarios", {
    params: search ? { search } : {},
  });
  return response.data;
}

export async function createUser(payload) {
  const response = await api.post("/usuario", payload);
  return response.data;
}

export async function updateUser(userId, payload) {
  const response = await api.put(`/usuario/${userId}`, payload);
  return response.data;
}

export async function deleteUser(userId) {
  const response = await api.delete(`/usuario/${userId}`);
  return response.data;
}

export async function fetchIntermediaries(search = "") {
  const response = await api.get("/intermediarios", {
    params: search ? { search } : {},
  });
  return response.data;
}

export async function fetchIntermediaryRelations(intermediaryId) {
  const response = await api.get(`/intermediario/${intermediaryId}/relaciones`);
  return response.data;
}

export async function createIntermediary(payload) {
  const response = await api.post("/nuevo-intermediario", payload);
  return response.data;
}

export async function updateIntermediary(intermediaryId, payload) {
  const response = await api.put(`/actualiza-intermediario/${intermediaryId}`, payload);
  return response.data;
}

export async function deleteIntermediary(intermediaryId) {
  const response = await api.delete(`/intermediario/${intermediaryId}`);
  return response.data;
}

export async function fetchClients(search = "") {
  const response = await api.get("/clientes", {
    params: search ? { search } : {},
  });
  return response.data;
}

export async function createClient(payload) {
  const response = await api.post("/nuevo-cliente", payload);
  return response.data;
}

export async function updateClient(clientId, payload) {
  const response = await api.put(`/actualiza-cliente/${clientId}`, payload);
  return response.data;
}

export async function deleteClient(clientId) {
  const response = await api.delete(`/cliente/${clientId}`);
  return response.data;
}

export default api;

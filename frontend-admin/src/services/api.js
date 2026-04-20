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

export default api;

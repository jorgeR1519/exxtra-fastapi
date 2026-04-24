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

export async function getAdvisorDashboard() {
  const response = await api.get("/asesores/dashboard");
  return response.data;
}

export default api;

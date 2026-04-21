import { createRouter, createWebHistory } from "vue-router";
import { clearSession, getSession, isClientSession } from "../services/session";
import AuthView from "../views/AuthView.vue";
import DashboardView from "../views/DashboardView.vue";

const routes = [
  {
    path: "/",
    redirect: "/auth/login",
  },
  {
    path: "/auth/login",
    name: "auth",
    component: AuthView,
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: DashboardView,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const session = getSession();

  if (to.meta.requiresAuth && !session) {
    return { name: "auth", params: { mode: "login" } };
  }

  if (session && !isClientSession(session)) {
    clearSession();
    return { name: "auth", params: { mode: "login" }, query: { denied: "role" } };
  }

  if (to.name === "auth" && session) {
    return { name: "dashboard" };
  }

  return true;
});

export default router;

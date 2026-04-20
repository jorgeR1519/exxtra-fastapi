import { createRouter, createWebHistory } from "vue-router";
import { clearSession, getSession, isAdminSession } from "../services/session";
import AuthView from "../views/AuthView.vue";
import DashboardView from "../views/DashboardView.vue";

const routes = [
  {
    path: "/",
    redirect: "/auth/login",
  },
  {
    path: "/auth/:mode(login|register)",
    name: "auth",
    component: AuthView,
    props: true,
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

   if (session && !isAdminSession(session)) {
    clearSession();
    return { name: "auth", params: { mode: "login" } };
  }

  if (to.name === "auth" && session) {
    return { name: "dashboard" };
  }

  return true;
});

export default router;

<script setup>
import { computed, reactive, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { login } from "../services/api";
import { setSession } from "../services/session";

const route = useRoute();
const router = useRouter();
const brandLogo = "https://exxtra.com.co/wp-content/uploads/2019/12/logo-1.png";

const loginForm = reactive({
  usuario: "",
  contrasena: "",
});

const quickAccessCards = [
  {
    id: "solicitudes",
    value: "Solicitudes",
    label: "Consulta y seguimiento del expediente comercial.",
  },
  {
    id: "clientes",
    value: "Clientes",
    label: "Acceso rapido a cartera, contacto y trazabilidad.",
  },
  {
    id: "pipeline",
    value: "Pipeline",
    label: "Base para tareas, alertas y conversion comercial.",
  },
];

const isSubmitting = ref(false);
const apiError = ref("");
const helperMessage = computed(() => {
  if (route.query.denied === "role") {
    return "Este portal esta reservado para asesores y usuarios comerciales autorizados.";
  }
  return "Usa tu documento o usuario comercial para continuar.";
});

watch(
  () => route.fullPath,
  () => {
    apiError.value = "";
  }
);

async function submitLogin() {
  isSubmitting.value = true;
  apiError.value = "";

  try {
    const session = await login({ ...loginForm });
    const role = session?.user?.tipo?.toLowerCase();

    if (role !== "asesor" && role !== "intermediario") {
      apiError.value = "Tu cuenta no corresponde al portal de asesores.";
      return;
    }

    setSession(session);
    await router.push({ name: "dashboard" });
  } catch (error) {
    apiError.value = error.response?.data?.detail || "No fue posible iniciar sesion.";
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <main class="advisor-login-shell">
    <section class="advisor-stage">
      <div class="advisor-copy">
        <div class="brand-stack">
          <img :src="brandLogo" alt="Exxtra" class="brand-logo advisor-brand-logo" />
          <div class="brand-chip advisor-chip">Portal comercial Exxtra</div>
        </div>

        <h1>Login para asesores y fuerza comercial.</h1>
        <p>
          Entra a tu espacio para cotizar, registrar solicitudes y dar seguimiento comercial sin depender
          del panel administrativo.
        </p>
      </div>

      <div class="advisor-quick-grid">
        <article v-for="item in quickAccessCards" :key="item.id" class="advisor-quick-card">
          <strong>{{ item.value }}</strong>
          <span>{{ item.label }}</span>
        </article>
      </div>

      <div class="advisor-note">
        <span>Acceso esperado</span>
        <p>Este portal esta orientado a usuarios con rol <strong>asesor</strong>.</p>
      </div>
    </section>

    <section class="advisor-login-panel">
      <div class="advisor-panel-header">
        <div>
          <span class="eyebrow">Inicio de sesion</span>
          <h2>Bienvenido de vuelta</h2>
        </div>
        <p>{{ helperMessage }}</p>
      </div>

      <p v-if="apiError" class="feedback error">{{ apiError }}</p>

      <form class="auth-form" @submit.prevent="submitLogin">
        <label>
          <span>Usuario o correo del asesor</span>
          <input
            v-model.trim="loginForm.usuario"
            type="text"
            placeholder="Ej. ASE001 o asesor@correo.com"
            required
          />
        </label>

        <label>
          <span>Contrasena</span>
          <input
            v-model="loginForm.contrasena"
            type="password"
            placeholder="Minimo 6 caracteres"
            required
          />
        </label>

        <button class="primary-btn" :disabled="isSubmitting">
          {{ isSubmitting ? "Validando acceso..." : "Entrar al portal" }}
        </button>
      </form>

      <div class="advisor-login-footer">
        <span>Necesitas una cuenta nueva o apoyo con el acceso?</span>
        <p>Solicita creacion o recuperacion de credenciales al equipo administrativo.</p>
      </div>
    </section>
  </main>
</template>

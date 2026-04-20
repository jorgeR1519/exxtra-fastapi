<script setup>
import { computed, reactive, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { login, register } from "../services/api";
import { setSession } from "../services/session";

const route = useRoute();
const router = useRouter();

const isLogin = computed(() => route.params.mode !== "register");
const title = computed(() =>
  isLogin.value ? "Accede al portal de asesores Exxtra" : "Crea tu acceso como asesor"
);
const subtitle = computed(() =>
  isLogin.value
    ? "Ingresa para gestionar solicitudes, clientes y acompanamiento comercial."
    : "Registra una cuenta orientada al trabajo comercial y seguimiento del proceso."
);

const loginForm = reactive({
  usuario: "",
  contrasena: "",
});

const registerForm = reactive({
  idUsuario: "",
  email: "",
  contrasena: "",
  tipo: "asesor",
  primeravez: "si",
});

const roleCards = [
  {
    id: "asesor",
    eyebrow: "Operacion comercial",
    title: "Asesor",
    description: "Seguimiento de solicitudes, onboarding de clientes y gestion del flujo comercial.",
  },
  {
    id: "pipeline",
    eyebrow: "Vista futura",
    title: "Pipeline",
    description: "Base lista para crecer hacia tablero de negocios, tareas y alertas de seguimiento.",
  },
];

const isSubmitting = ref(false);
const apiError = ref("");

watch(
  () => route.params.mode,
  () => {
    apiError.value = "";
  }
);

async function submitLogin() {
  isSubmitting.value = true;
  apiError.value = "";

  try {
    const session = await login({ ...loginForm });
    setSession(session);
    await router.push({ name: "dashboard" });
  } catch (error) {
    apiError.value = error.response?.data?.detail || "No fue posible iniciar sesion.";
  } finally {
    isSubmitting.value = false;
  }
}

async function submitRegister() {
  isSubmitting.value = true;
  apiError.value = "";

  try {
    const normalizedRole = registerForm.tipo === "asesor" ? "intermediario" : "administrador";
    const session = await register({
      ...registerForm,
      tipo: normalizedRole,
    });
    setSession(session);
    await router.push({ name: "dashboard" });
  } catch (error) {
    apiError.value = error.response?.data?.detail || "No fue posible crear la cuenta.";
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <main class="auth-shell">
    <section class="auth-hero">
      <div class="brand-chip">Exxtra credit operating hub</div>
      <h1>{{ title }}</h1>
      <p>{{ subtitle }}</p>

      <div class="role-grid">
        <article v-for="card in roleCards" :key="card.id" class="role-card">
          <span>{{ card.eyebrow }}</span>
          <h3>{{ card.title }}</h3>
          <p>{{ card.description }}</p>
        </article>
      </div>
    </section>

    <section class="auth-panel">
      <div class="panel-header">
        <div>
          <span class="eyebrow">{{ isLogin ? "Inicio de sesion" : "Registro" }}</span>
          <h2>{{ isLogin ? "Bienvenido de vuelta" : "Crea tu perfil" }}</h2>
        </div>

        <div class="toggle-group">
          <RouterLink
            class="toggle-link"
            :class="{ active: isLogin }"
            :to="{ name: 'auth', params: { mode: 'login' } }"
          >
            Login
          </RouterLink>
          <RouterLink
            class="toggle-link"
            :class="{ active: !isLogin }"
            :to="{ name: 'auth', params: { mode: 'register' } }"
          >
            Register
          </RouterLink>
        </div>
      </div>

      <p v-if="apiError" class="feedback error">{{ apiError }}</p>

      <form v-if="isLogin" class="auth-form" @submit.prevent="submitLogin">
        <label>
          <span>Usuario</span>
          <input v-model.trim="loginForm.usuario" type="text" placeholder="Ej. 123456789" required />
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
          {{ isSubmitting ? "Ingresando..." : "Entrar al sistema" }}
        </button>
      </form>

      <form v-else class="auth-form" @submit.prevent="submitRegister">
        <label>
          <span>Documento o usuario</span>
          <input v-model.trim="registerForm.idUsuario" type="text" placeholder="Ej. 900809703" required />
        </label>

        <label>
          <span>Correo</span>
          <input v-model.trim="registerForm.email" type="email" placeholder="correo@exxtra.com" required />
        </label>

        <label>
          <span>Contrasena</span>
          <input
            v-model="registerForm.contrasena"
            type="password"
            placeholder="Minimo 6 caracteres"
            required
          />
        </label>

        <label>
          <span>Perfil inicial</span>
          <input value="Asesor" type="text" disabled />
        </label>

        <button class="primary-btn" :disabled="isSubmitting">
          {{ isSubmitting ? "Creando cuenta..." : "Crear acceso" }}
        </button>
      </form>
    </section>
  </main>
</template>

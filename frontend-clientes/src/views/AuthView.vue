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
    id: "estado",
    value: "Tu credito",
    label: "Consulta saldos, estado actual y seguimiento de tu obligacion.",
  },
  {
    id: "pagos",
    value: "Pagos",
    label: "Base para enlaces de pago y recordatorios asociados a tu cuenta.",
  },
  {
    id: "soporte",
    value: "Soporte",
    label: "Canal inicial para resolver dudas de acceso y seguimiento.",
  },
];

const isSubmitting = ref(false);
const apiError = ref("");
const helperMessage = computed(() => {
  if (route.query.denied === "role") {
    return "Este portal esta reservado para usuarios con rol cliente.";
  }
  return "Ingresa con los datos enviados por correo para consultar tu informacion.";
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

    if (role !== "cliente") {
      apiError.value = "Tu cuenta no corresponde al portal de clientes.";
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
  <main class="client-login-shell">
    <section class="client-stage">
      <div class="client-copy">
        <div class="brand-stack">
          <img :src="brandLogo" alt="Exxtra" class="brand-logo client-brand-logo" />
          <div class="brand-chip client-chip">Portal clientes Exxtra</div>
        </div>

        <h1>Accede a tu portal de cliente Exxtra.</h1>
        <p>
          Desde aqui podras consultar el estado de tu credito, revisar informacion asociada a tu
          cuenta y continuar el flujo que la empresa te habilite para pagos y seguimiento.
        </p>
      </div>

      <div class="client-quick-grid">
        <article v-for="item in quickAccessCards" :key="item.id" class="client-quick-card">
          <strong>{{ item.value }}</strong>
          <span>{{ item.label }}</span>
        </article>
      </div>

      <div class="client-note">
        <span>Acceso por invitacion</span>
        <p>
          Tus credenciales suelen enviarse por correo cuando tu cuenta queda habilitada dentro del
          proceso.
        </p>
      </div>
    </section>

    <section class="client-login-panel">
      <div class="client-panel-header">
        <div>
          <span class="eyebrow">Inicio de sesion</span>
          <h2>Bienvenido a tu espacio</h2>
        </div>
        <p>{{ helperMessage }}</p>
      </div>

      <p v-if="apiError" class="feedback error">{{ apiError }}</p>

      <form class="auth-form" @submit.prevent="submitLogin">
        <label>
          <span>Usuario o correo del cliente</span>
          <input
            v-model.trim="loginForm.usuario"
            type="text"
            placeholder="Ej. 66979476 o cliente@correo.com"
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
          {{ isSubmitting ? "Validando acceso..." : "Entrar como cliente" }}
        </button>
      </form>

      <div class="client-login-footer">
        <span>No encuentras el correo o tus datos de acceso?</span>
        <p>Solicita al equipo de Exxtra el reenvio de tus credenciales o la recuperacion de acceso.</p>
      </div>
    </section>
  </main>
</template>

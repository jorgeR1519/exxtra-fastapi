<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { clearSession, getSession } from "../services/session";

const router = useRouter();
const session = getSession();
const brandLogo = "https://exxtra.com.co/wp-content/uploads/2019/12/logo-1.png";

const roleLabel = computed(() => {
  if (!session?.user?.tipo) return "Sin rol";
  if (session.user.tipo.toLowerCase() === "administrador") return "Administrador";
  if (session.user.tipo.toLowerCase() === "intermediario") return "Intermediario";
  if (session.user.tipo.toLowerCase() === "cliente") return "Cliente";
  return session.user.tipo;
});

function logout() {
  clearSession();
  router.push({ name: "auth", params: { mode: "login" } });
}
</script>

<template>
  <main class="dashboard-shell">
    <section class="dashboard-card">
      <img :src="brandLogo" alt="Exxtra" class="brand-logo dashboard-logo client-brand-logo" />
      <span class="eyebrow">Sesion activa</span>
      <h1>Hola, {{ session?.user?.idUsuario }}</h1>
      <p>
        Esta es la base visual inicial del portal de clientes. Desde aqui puedes crecer hacia modulos
        de saldo, plan de pagos, enlaces de pago y seguimiento de tu credito.
      </p>

      <div class="dashboard-grid">
        <article>
          <span>Rol</span>
          <strong>{{ roleLabel }}</strong>
        </article>
        <article>
          <span>Correo</span>
          <strong>{{ session?.user?.email }}</strong>
        </article>
        <article>
          <span>Token</span>
          <strong>{{ session?.token_type }}</strong>
        </article>
      </div>

      <button class="primary-btn secondary" @click="logout">Cerrar sesion</button>
    </section>
  </main>
</template>

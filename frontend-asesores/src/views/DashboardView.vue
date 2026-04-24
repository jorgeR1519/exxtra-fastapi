<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { getAdvisorDashboard } from "../services/api";
import { clearSession, getSession } from "../services/session";

const router = useRouter();
const session = getSession();
const brandLogo = "https://exxtra.com.co/wp-content/uploads/2019/12/logo-1.png";
const activeSection = ref("inicio");
const sidebarOpen = ref(false);
const requestsOpen = ref(true);

const navSections = [
  { id: "inicio", label: "Inicio" },
  { id: "cotizador", label: "Cotizador" },
];

const requestSections = [
  { id: "solicitudes-pendientes", label: "Pendientes" },
  { id: "solicitudes-legalizar", label: "Para legalizar" },
  { id: "solicitudes-legalizadas", label: "Legalizadas" },
];

const finalSections = [
  { id: "creditos", label: "Creditos" },
  { id: "desembolsos", label: "Desembolsos" },
];

const dashboardLoading = ref(false);
const dashboardError = ref("");
const dashboardData = ref({
  summary: {
    pending_requests: 0,
    to_legalize_requests: 0,
    legalized_requests: 0,
    active_credits: 0,
  },
  risk_credits: [],
});

const roleLabel = computed(() => {
  if (!session?.user?.tipo) return "Sin rol";
  if (session.user.tipo.toLowerCase() === "administrador") return "Administrador";
  if (session.user.tipo.toLowerCase() === "intermediario") return "Intermediario";
  if (session.user.tipo.toLowerCase() === "asesor") return "Asesor";
  return session.user.tipo;
});

const advisorInitials = computed(() => {
  const base = session?.user?.idUsuario || session?.user?.email || "AS";
  return base.slice(0, 2).toUpperCase();
});

const sectionMeta = computed(() => {
  const current = activeSection.value;

  if (current === "inicio") {
    return {
      eyebrow: "Vista general",
      title: "Inicio comercial",
      description:
        "Consulta el estado general de tu operacion comercial y accede rapidamente a las tareas del dia.",
    };
  }

  if (current === "cotizador") {
    return {
      eyebrow: "Herramienta",
      title: "Cotizador",
      description:
        "Prepara escenarios iniciales de credito y revisa condiciones comerciales antes de crear la solicitud.",
    };
  }

  if (current === "solicitudes-pendientes") {
    return {
      eyebrow: "Solicitudes",
      title: "Pendientes",
      description:
        "Expedientes en construccion o a la espera de completar informacion documental y comercial.",
    };
  }

  if (current === "solicitudes-legalizar") {
    return {
      eyebrow: "Solicitudes",
      title: "Para legalizar",
      description:
        "Solicitudes que requieren validacion final, firma o soportes para avanzar a su formalizacion.",
    };
  }

  if (current === "solicitudes-legalizadas") {
    return {
      eyebrow: "Solicitudes",
      title: "Legalizadas",
      description:
        "Casos completados comercialmente y listos para consulta historica o seguimiento posterior.",
    };
  }

  if (current === "creditos") {
    return {
      eyebrow: "Operacion",
      title: "Creditos",
      description:
        "Consulta negocios formalizados y da seguimiento a su evolucion desde el frente comercial.",
    };
  }

  return {
    eyebrow: "Operacion",
    title: "Desembolsos",
    description:
      "Visualiza desembolsos relacionados con tu gestion comercial y mantiene trazabilidad sobre cada caso.",
  };
});

const overviewCards = computed(() => [
  {
    id: "rol",
    label: "Rol",
    value: roleLabel.value,
  },
  {
    id: "correo",
    label: "Correo",
    value: session?.user?.email || "No disponible",
  },
  {
    id: "usuario",
    label: "Usuario",
    value: session?.user?.idUsuario || "Sin identificacion",
  },
]);

const homeStats = computed(() => [
  {
    id: "pending",
    label: "Solicitudes pendientes",
    value: dashboardLoading.value ? "..." : dashboardData.value.summary.pending_requests,
    icon: "S",
    tone: "info",
  },
  {
    id: "active",
    label: "Creditos activos",
    value: dashboardLoading.value ? "..." : dashboardData.value.summary.active_credits,
    icon: "C",
    tone: "success",
  },
]);

const riskCredits = computed(() => dashboardData.value.risk_credits);

function selectSection(sectionId) {
  activeSection.value = sectionId;
  sidebarOpen.value = false;
}

function toggleRequests() {
  requestsOpen.value = !requestsOpen.value;
}

function logout() {
  clearSession();
  router.push({ name: "auth", params: { mode: "login" } });
}

async function loadAdvisorDashboard() {
  dashboardLoading.value = true;
  dashboardError.value = "";

  try {
    dashboardData.value = await getAdvisorDashboard();
  } catch (error) {
    dashboardError.value = error.response?.data?.detail || "No fue posible cargar el inicio del asesor.";
  } finally {
    dashboardLoading.value = false;
  }
}

onMounted(() => {
  loadAdvisorDashboard();
});
</script>

<template>
  <main class="advisor-dashboard-shell">
    <button class="advisor-mobile-toggle" type="button" @click="sidebarOpen = !sidebarOpen">
      {{ sidebarOpen ? "Cerrar menu" : "Abrir menu" }}
    </button>

    <aside class="advisor-sidebar" :class="{ open: sidebarOpen }">
      <div class="advisor-sidebar-top">
        <img :src="brandLogo" alt="Exxtra" class="brand-logo advisor-brand-logo" />

        <div class="advisor-avatar">{{ advisorInitials }}</div>

        <div class="advisor-session-card">
          <span>Sesion actual</span>
          <strong>{{ session?.user?.idUsuario || "Asesor" }}</strong>
          <p>{{ roleLabel }}</p>
        </div>
      </div>

      <nav class="advisor-nav">
        <button
          v-for="section in navSections"
          :key="section.id"
          type="button"
          class="advisor-nav-item"
          :class="{ active: activeSection === section.id }"
          @click="selectSection(section.id)"
        >
          {{ section.label }}
        </button>

        <div class="advisor-nav-group" :class="{ open: requestsOpen }">
          <button
            type="button"
            class="advisor-nav-item advisor-nav-parent"
            :class="{ active: activeSection.startsWith('solicitudes') }"
            @click="toggleRequests"
          >
            Solicitudes
          </button>

          <div v-if="requestsOpen" class="advisor-subnav">
            <button
              v-for="section in requestSections"
              :key="section.id"
              type="button"
              class="advisor-subnav-item"
              :class="{ active: activeSection === section.id }"
              @click="selectSection(section.id)"
            >
              {{ section.label }}
            </button>
          </div>
        </div>

        <button
          v-for="section in finalSections"
          :key="section.id"
          type="button"
          class="advisor-nav-item"
          :class="{ active: activeSection === section.id }"
          @click="selectSection(section.id)"
        >
          {{ section.label }}
        </button>
      </nav>

      <button class="primary-btn secondary advisor-logout" @click="logout">Cerrar sesion</button>
    </aside>

    <section class="advisor-main-panel">
      <article class="dashboard-card advisor-dashboard-card">
        <span class="eyebrow">{{ sectionMeta.eyebrow }}</span>
        <h1>{{ sectionMeta.title }}</h1>
        <p>{{ sectionMeta.description }}</p>

        <p v-if="activeSection === 'inicio' && dashboardError" class="feedback error">
          {{ dashboardError }}
        </p>

        <div v-if="activeSection === 'inicio'" class="advisor-home-kpis">
          <article
            v-for="item in homeStats"
            :key="item.id"
            class="advisor-kpi-card"
            :class="[`tone-${item.tone}`]"
          >
            <div>
              <span>{{ item.label }}</span>
              <strong>{{ item.value }}</strong>
            </div>
            <div class="advisor-kpi-icon">{{ item.icon }}</div>
          </article>
        </div>

        <section v-if="activeSection === 'inicio'" class="advisor-table-panel">
          <div class="advisor-table-header">
            <div>
              <span class="eyebrow">Monitoreo</span>
              <h2>Creditos en seguimiento</h2>
            </div>
            <p>Clientes con mayor alerta para seguimiento comercial inmediato.</p>
          </div>

          <div class="advisor-table-wrap">
            <table class="advisor-table">
              <thead>
                <tr>
                  <th>Credito</th>
                  <th>Cliente</th>
                  <th>Identificacion</th>
                  <th>Poliza</th>
                  <th>Placa</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in riskCredits" :key="`${item.credito}-${item.placa}`">
                  <td>{{ item.credito }}</td>
                  <td>{{ item.cliente }}</td>
                  <td>{{ item.identificacion }}</td>
                  <td>{{ item.poliza }}</td>
                  <td>{{ item.placa }}</td>
                  <td>
                    <span class="risk-badge">
                      {{ item.estado }}
                      <strong>{{ item.mora }}</strong>
                    </span>
                  </td>
                </tr>
                <tr v-if="!riskCredits.length">
                  <td colspan="6">
                    <div class="advisor-table-empty">
                      <strong>Sin datos cargados</strong>
                      <p>Esta vista queda lista para mostrar los creditos reales cuando conectemos el backend.</p>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <div v-else class="dashboard-grid advisor-summary-grid">
          <article v-for="item in overviewCards" :key="item.id">
            <span>{{ item.label }}</span>
            <strong>{{ item.value }}</strong>
          </article>
        </div>

        <section v-if="activeSection !== 'inicio'" class="advisor-workspace">
          <div class="advisor-workspace-card">
            <span>Estado del modulo</span>
            <h2>{{ sectionMeta.title }}</h2>
            <p>
              Este espacio queda listo para conectar los datos reales del flujo comercial sin cambiar la
              estructura del panel.
            </p>
          </div>

          <div class="advisor-workspace-card">
            <span>Proximo paso</span>
            <h2>Integracion funcional</h2>
            <p>
              Podemos conectar esta vista con cotizador, solicitudes o bandejas operativas cuando avances con
              el backend correspondiente.
            </p>
          </div>
        </section>
      </article>
    </section>
  </main>
</template>

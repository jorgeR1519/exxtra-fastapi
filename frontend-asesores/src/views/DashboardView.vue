<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { getAdvisorDashboard, getCitiesCatalog } from "../services/api";
import { clearSession, getSession } from "../services/session";

const router = useRouter();
const session = getSession();
const brandLogo = "https://exxtra.com.co/wp-content/uploads/2019/12/logo-1.png";
const activeSection = ref("inicio");
const sidebarOpen = ref(false);
const requestsOpen = ref(true);
const fiscalDropdownOpen = ref(false);

const navSections = [
  {
    id: "inicio",
    label: "Inicio",
    icon: "M4 10.5 12 4l8 6.5V19a1 1 0 0 1-1 1h-4.5v-5h-5v5H5a1 1 0 0 1-1-1z",
  },
  {
    id: "cotizador",
    label: "Cotizador",
    icon: "M8 3.5h8a2.5 2.5 0 0 1 2.5 2.5v12A2.5 2.5 0 0 1 16 20.5H8A2.5 2.5 0 0 1 5.5 18V6A2.5 2.5 0 0 1 8 3.5zm2 4h4m-4 4h4m-4 4h2",
  },
];

const requestSections = [
  {
    id: "solicitudes-pendientes",
    label: "Pendientes",
    icon: "M8 3.5h7l4.5 4.5V18A2.5 2.5 0 0 1 17 20.5H8A2.5 2.5 0 0 1 5.5 18V6A2.5 2.5 0 0 1 8 3.5zm2 5h4m-4 4h4m-4 4h3",
  },
  {
    id: "solicitudes-legalizar",
    label: "Para legalizar",
    icon: "M8 3.5h8A2.5 2.5 0 0 1 18.5 6v12a2.5 2.5 0 0 1-2.5 2.5H8A2.5 2.5 0 0 1 5.5 18V6A2.5 2.5 0 0 1 8 3.5zm2.2 9.2 1.8 1.8 4-4",
  },
  {
    id: "solicitudes-legalizadas",
    label: "Legalizadas",
    icon: "M8 3.5h8A2.5 2.5 0 0 1 18.5 6v12a2.5 2.5 0 0 1-2.5 2.5H8A2.5 2.5 0 0 1 5.5 18V6A2.5 2.5 0 0 1 8 3.5zm2.1 9 2 2 4.8-5.2",
  },
];

const finalSections = [
  {
    id: "creditos",
    label: "Creditos",
    icon: "M4.5 8A2.5 2.5 0 0 1 7 5.5h10A2.5 2.5 0 0 1 19.5 8v8A2.5 2.5 0 0 1 17 18.5H7A2.5 2.5 0 0 1 4.5 16zm3.5 3h8m-8-2h1",
  },
  {
    id: "desembolsos",
    label: "Desembolsos",
    icon: "M12 3.5v17M8.5 7.5c0-1.7 1.6-3 3.5-3s3.5 1.3 3.5 3-1.6 3-3.5 3-3.5 1.3-3.5 3 1.6 3 3.5 3 3.5 1.3 3.5 3",
  },
];

const summaryFlags = [
  {
    id: "documentos",
    label: "Documentos Adjuntos",
    icon: "M8 3.5h7l4.5 4.5V18A2.5 2.5 0 0 1 17 20.5H8A2.5 2.5 0 0 1 5.5 18V6A2.5 2.5 0 0 1 8 3.5zm2 7h4m-4 4h4",
  },
  {
    id: "firmada",
    label: "Solicitud Firmada",
    icon: "M8 12.5 10.3 14.8 15.5 9.6M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z",
  },
  {
    id: "pagada",
    label: "C.I Pagada",
    icon: "M12 3.5v17M8.5 7.5c0-1.7 1.6-3 3.5-3s3.5 1.3 3.5 3-1.6 3-3.5 3-3.5 1.3-3.5 3 1.6 3 3.5 3 3.5 1.3 3.5 3",
  },
  {
    id: "legalizada",
    label: "Solicitud Legalizada",
    icon: "M8 3.5h8A2.5 2.5 0 0 1 18.5 6v12a2.5 2.5 0 0 1-2.5 2.5H8A2.5 2.5 0 0 1 5.5 18V6A2.5 2.5 0 0 1 8 3.5zm2.1 9 2 2 4.8-5.2",
  },
];

const dashboardLoading = ref(false);
const dashboardError = ref("");
const cityOptions = ref([]);
const dashboardData = ref({
  summary: {
    pending_requests: 0,
    to_legalize_requests: 0,
    legalized_requests: 0,
    active_credits: 0,
  },
  risk_credits: [],
});

const quoteForm = reactive({
  tipoPersona: "Persona Natural",
  primerNombre: "",
  segundoNombre: "",
  primerApellido: "",
  segundoApellido: "",
  tipoDocumento: "Cedula de Ciudadania",
  numeroIdentificacion: "",
  correo: "",
  ciudad: "",
  direccion: "",
  celular: "",
  celularAlternativo: "",
  actividadEconomica: "",
  regimenVentas: "",
  responsabilidadesFiscales: [],
  origenRecursos: "",
  reutilizaCorreoFacturacion: false,
  correoFacturacion: "",
  correoAlternoFirma: false,
  correoAlternoPagare: "",
  nombreAsesor: session?.user?.idUsuario || "",
  cedulaAsesor: "",
  ramo: "AUTOMOVILES",
  fechaInicioVigencia: "",
  vigenciaHasta: "",
  tiempoCorrido: "",
  placa: "",
  valorConIva: "",
  aseguradora: "",
  numeroPoliza: "",
  numeroCertificado: "",
  beneficiarioOneroso: false,
  nombreBeneficiarioOneroso: "",
  numeroCuotas: "",
  cuotasMaximas: "",
  pagoSuperiorPrimeraCuota: false,
  valorMinimoPrimeraCuota: "",
  otroValorPrimeraCuota: "",
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
        "Prepara la información del cliente, simula la póliza y deja lista la solicitud para continuar el flujo.",
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

const summaryItems = computed(() => [
  { id: "credito", label: "Credito", value: quoteForm.numeroPoliza || "-" },
  { id: "documento", label: "Cedula / NIT", value: quoteForm.numeroIdentificacion || "-" },
  { id: "correo", label: "Correo Electrónico", value: quoteForm.correo || "-" },
  { id: "celular", label: "Celular", value: quoteForm.celular || "-" },
]);

const riskCredits = computed(() => dashboardData.value.risk_credits);

const economicActivityOptions = [
  "Empleado",
  "Pensionado",
  "Profesional Indep",
  "Comerciante",
  "Otro",
];

const salesRegimeOptions = [
  "No responsable de IVA",
  "Si responsable de IVA",
  "Impuesto al consumo",
  "Si responsable de IVA e Impuesto al consumo",
];

const fiscalResponsibilityOptions = [
  "Gran contribuyente",
  "Autorretenedor",
  "Agente de retencion en el impuesto sobre las ventas",
  "Regimen Simple de Tributacion - SIMPLE",
  "Otro tipo de responsable",
];

function normalizeAlertStatus(status) {
  const normalized = String(status || "").trim().toUpperCase();
  if (normalized.includes("MORA")) return "MORA AV";
  if (normalized.includes("RIESGO")) return "RIESGO";
  return "RIESGO";
}

function alertBadgeClass(status) {
  return normalizeAlertStatus(status) === "MORA AV" ? "mora-av" : "riesgo";
}

function selectSection(sectionId) {
  activeSection.value = sectionId;
  sidebarOpen.value = false;
}

function toggleRequests() {
  requestsOpen.value = !requestsOpen.value;
}

function toggleFiscalDropdown() {
  fiscalDropdownOpen.value = !fiscalDropdownOpen.value;
}

function logout() {
  clearSession();
  router.push({ name: "auth", params: { mode: "login" } });
}

function moneyPlaceholder(value) {
  if (!value) return "$0";
  return new Intl.NumberFormat("es-CO", { style: "currency", currency: "COP", maximumFractionDigits: 0 }).format(
    Number(value) || 0
  );
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

async function loadCitiesCatalog() {
  try {
    cityOptions.value = await getCitiesCatalog();
  } catch {
    cityOptions.value = [];
  }
}

onMounted(() => {
  loadAdvisorDashboard();
  loadCitiesCatalog();
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
          <span class="advisor-nav-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path :d="section.icon" />
            </svg>
          </span>
          <span class="advisor-nav-label">{{ section.label }}</span>
        </button>

        <div class="advisor-nav-group" :class="{ open: requestsOpen }">
          <button
            type="button"
            class="advisor-nav-item advisor-nav-parent"
            :class="{ active: activeSection.startsWith('solicitudes') }"
            @click="toggleRequests"
          >
            <span class="advisor-nav-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M8 3.5h7l4.5 4.5V18A2.5 2.5 0 0 1 17 20.5H8A2.5 2.5 0 0 1 5.5 18V6A2.5 2.5 0 0 1 8 3.5zm2 7h4m-4 4h4" />
              </svg>
            </span>
            <span class="advisor-nav-label">Solicitudes</span>
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
              <span class="advisor-subnav-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none">
                  <path :d="section.icon" />
                </svg>
              </span>
              <span class="advisor-nav-label">{{ section.label }}</span>
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
          <span class="advisor-nav-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path :d="section.icon" />
            </svg>
          </span>
          <span class="advisor-nav-label">{{ section.label }}</span>
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
            <div class="advisor-table-meta">
              <p>Clientes con mayor alerta para seguimiento comercial inmediato.</p>
              <div class="advisor-status-legends">
                <span class="legend-chip riesgo">Riesgo</span>
                <span class="legend-chip mora-av">Mora AV</span>
              </div>
            </div>
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
                    <span class="risk-badge" :class="alertBadgeClass(item.estado)">
                      {{ normalizeAlertStatus(item.estado) }}
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

        <section v-else-if="activeSection === 'cotizador'" class="quote-flow">
          <article class="quote-section">
            <div class="quote-section-header">
              <div class="quote-section-title">
                <span class="quote-title-icon">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path d="M16 19a4 4 0 0 0-8 0m8 0H8m8 0h3m-11 0H5m7-8a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z" />
                  </svg>
                </span>
                <h2>Resumen</h2>
              </div>
            </div>

            <div class="quote-summary-grid">
              <div v-for="item in summaryItems" :key="item.id" class="quote-summary-card">
                <span>{{ item.label }}</span>
                <strong>{{ item.value }}</strong>
              </div>
            </div>

            <div class="quote-flag-grid">
              <div v-for="item in summaryFlags" :key="item.id" class="quote-flag-card">
                <span class="quote-flag-icon">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path :d="item.icon" />
                  </svg>
                </span>
                <small>{{ item.label }}</small>
              </div>
            </div>
          </article>

          <article class="quote-section">
            <div class="quote-section-header">
              <div class="quote-section-title">
                <span class="quote-title-icon">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path d="M16 19a4 4 0 0 0-8 0m8 0H8m8 0h3m-11 0H5m7-8a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z" />
                  </svg>
                </span>
                <h2>Información Basica</h2>
              </div>
              <div class="quote-section-aside">
                <p>Para agilizar la cotización, monta la carátula de la póliza sin clausulado aquí.</p>
                <button type="button" class="quote-outline-btn">OCR</button>
              </div>
            </div>

            <div class="quote-form-grid quote-basic-grid">
              <label class="field">
                <span>Tipo de Persona*</span>
                <select v-model="quoteForm.tipoPersona">
                  <option>Persona Natural</option>
                  <option>Persona Juridica</option>
                </select>
              </label>
              <div class="quote-grid-spacer"></div>
              <div class="quote-grid-spacer"></div>
              <div class="quote-grid-spacer"></div>

              <label class="field"><span>Primer Nombre*</span><input v-model="quoteForm.primerNombre" type="text" /></label>
              <label class="field"><span>Segundo Nombre</span><input v-model="quoteForm.segundoNombre" type="text" /></label>
              <label class="field"><span>Primer Apellido*</span><input v-model="quoteForm.primerApellido" type="text" /></label>
              <label class="field"><span>Segundo Apellido*</span><input v-model="quoteForm.segundoApellido" type="text" /></label>

              <label class="field">
                <span>Tipo de Documento*</span>
                <select v-model="quoteForm.tipoDocumento">
                  <option>Cedula de Ciudadania</option>
                  <option>NIT</option>
                  <option>Cedula de Extranjeria</option>
                  <option>Pasaporte</option>
                </select>
              </label>
              <label class="field"><span>Número de Identificación*</span><input v-model="quoteForm.numeroIdentificacion" type="text" /></label>
              <label class="field field-span-2"><span>Correo Electrónico*</span><input v-model="quoteForm.correo" type="email" /></label>

              <label class="field">
                <span>Ciudad*</span>
                <select v-model="quoteForm.ciudad">
                  <option value="">Ciudad*</option>
                  <option v-for="city in cityOptions" :key="city.value" :value="city.label">{{ city.label }}</option>
                </select>
              </label>
              <label class="field field-span-2"><span>Dirección*</span><input v-model="quoteForm.direccion" type="text" /></label>
              <label class="field"><span>Celular*</span><input v-model="quoteForm.celular" type="text" /></label>
              <label class="field"><span>Celular Alternativo</span><input v-model="quoteForm.celularAlternativo" type="text" /></label>

              <label class="field">
                <span>Actividad Economica*</span>
                <select v-model="quoteForm.actividadEconomica">
                  <option value="">Actividad Economica*</option>
                  <option v-for="option in economicActivityOptions" :key="option" :value="option">{{ option }}</option>
                </select>
              </label>
              <label class="field">
                <span>Regimen de Ventas*</span>
                <select v-model="quoteForm.regimenVentas">
                  <option value="">Regimen de Ventas*</option>
                  <option v-for="option in salesRegimeOptions" :key="option" :value="option">{{ option }}</option>
                </select>
              </label>
              <div class="field quote-checklist-field field-span-2">
                <span>Responsabilidades Fiscales*</span>
                <div class="quote-multiselect" :class="{ open: fiscalDropdownOpen }">
                  <button type="button" class="quote-multiselect-trigger" @click="toggleFiscalDropdown">
                    <span>
                      {{
                        quoteForm.responsabilidadesFiscales.length
                          ? `${quoteForm.responsabilidadesFiscales.length} seleccionada(s)`
                          : "Responsabilidades Fiscales*"
                      }}
                    </span>
                    <strong>{{ fiscalDropdownOpen ? "▴" : "▾" }}</strong>
                  </button>
                  <div v-if="fiscalDropdownOpen" class="quote-checklist">
                    <label v-for="option in fiscalResponsibilityOptions" :key="option" class="quote-checkbox-option">
                      <input v-model="quoteForm.responsabilidadesFiscales" :value="option" type="checkbox" />
                      <span>{{ option }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <label class="field field-span-full"><span>Origen de los Recursos*</span><input v-model="quoteForm.origenRecursos" type="text" /></label>
            </div>

            <div class="quote-radio-grid">
              <div class="quote-radio-card">
                <strong>¿Desea reutilizar el correo para facturación electrónica?</strong>
                <div class="radio-group">
                  <label><input v-model="quoteForm.reutilizaCorreoFacturacion" :value="false" type="radio" />No</label>
                  <label><input v-model="quoteForm.reutilizaCorreoFacturacion" :value="true" type="radio" />SI</label>
                </div>
              </div>
              <label class="field">
                <span>Correo de Facturación Electrónica*</span>
                <input v-model="quoteForm.correoFacturacion" type="email" />
              </label>
            </div>

            <div class="quote-radio-grid">
              <div class="quote-radio-card">
                <strong>¿Desea un Correo alterno para firmar pagaré?</strong>
                <div class="radio-group">
                  <label><input v-model="quoteForm.correoAlternoFirma" :value="false" type="radio" />No</label>
                  <label><input v-model="quoteForm.correoAlternoFirma" :value="true" type="radio" />SI</label>
                </div>
              </div>
              <label class="field">
                <span>Correo Alterno Para Firmar Pagaré</span>
                <input v-model="quoteForm.correoAlternoPagare" type="email" />
              </label>
            </div>
          </article>

          <article class="quote-section">
            <div class="quote-section-header">
              <div class="quote-section-title">
                <span class="quote-title-icon">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path d="M8 3.5h8a2.5 2.5 0 0 1 2.5 2.5v12A2.5 2.5 0 0 1 16 20.5H8A2.5 2.5 0 0 1 5.5 18V6A2.5 2.5 0 0 1 8 3.5zm2 4h4m-4 4h4m-4 4h4" />
                  </svg>
                </span>
                <h2>Simulación de tu Poliza</h2>
              </div>
              <div class="quote-date-note">
                <span>*Fecha Creación*</span>
                <strong>--/--/----</strong>
              </div>
            </div>

            <div class="quote-form-grid">
              <label class="field field-span-2"><span>Nombre del Asesor*</span><input v-model="quoteForm.nombreAsesor" type="text" /></label>
              <label class="field field-span-2"><span>Cedula del Asesor*</span><input v-model="quoteForm.cedulaAsesor" type="text" /></label>

              <label class="field field-span-full">
                <span>Ramo*</span>
                <select v-model="quoteForm.ramo">
                  <option>AUTOMOVILES</option>
                  <option>VIDA</option>
                  <option>HOGAR</option>
                </select>
              </label>

              <label class="field"><span>Fecha de Inicio de Vigencia*</span><input v-model="quoteForm.fechaInicioVigencia" type="date" /></label>
              <label class="field"><span>Vigencia Hasta</span><input v-model="quoteForm.vigenciaHasta" type="date" /></label>
              <label class="field"><span>Tiempo Corrido (días)</span><input v-model="quoteForm.tiempoCorrido" type="number" /></label>
              <div class="quote-grid-spacer"></div>

              <label class="field"><span>Placa*</span><input v-model="quoteForm.placa" type="text" /></label>
              <label class="field"><span>Valor (con IVA)*</span><input v-model="quoteForm.valorConIva" type="number" /></label>
              <label class="field">
                <span>Aseguradora</span>
                <select v-model="quoteForm.aseguradora">
                  <option value="">Aseguradora</option>
                  <option>Sura</option>
                  <option>Allianz</option>
                  <option>Bolivar</option>
                </select>
              </label>
              <label class="field"><span># de Póliza*</span><input v-model="quoteForm.numeroPoliza" type="text" /></label>
              <label class="field"><span># de Certificado</span><input v-model="quoteForm.numeroCertificado" type="text" /></label>

              <div class="quote-radio-stack">
                <strong>¿Beneficiario Oneroso?</strong>
                <div class="radio-group">
                  <label><input v-model="quoteForm.beneficiarioOneroso" :value="false" type="radio" />NO</label>
                  <label><input v-model="quoteForm.beneficiarioOneroso" :value="true" type="radio" />SI</label>
                </div>
              </div>
              <label class="field field-span-2">
                <span>Beneficiario Oneroso</span>
                <select v-model="quoteForm.nombreBeneficiarioOneroso">
                  <option value="">Beneficiario Oneroso</option>
                  <option>Bancolombia</option>
                  <option>Davivienda</option>
                </select>
              </label>
              <label class="field"><span># de Cuotas*</span><input v-model="quoteForm.numeroCuotas" type="number" /></label>
              <label class="field"><span>Cuotas Máximas</span><input v-model="quoteForm.cuotasMaximas" type="number" /></label>

              <label class="field"><span>Valor Mínimo Primera Cuota</span><input v-model="quoteForm.valorMinimoPrimeraCuota" type="number" /></label>
              <div class="quote-radio-stack field-span-2">
                <strong>¿Desea realizar un pago superior de primera cuota?</strong>
                <div class="radio-group">
                  <label><input v-model="quoteForm.pagoSuperiorPrimeraCuota" :value="false" type="radio" />NO</label>
                  <label><input v-model="quoteForm.pagoSuperiorPrimeraCuota" :value="true" type="radio" />SI</label>
                </div>
              </div>
              <label class="field">
                <span>Otro Valor Primera Cuota</span>
                <input v-model="quoteForm.otroValorPrimeraCuota" type="number" />
                <small class="field-help">{{ moneyPlaceholder(quoteForm.otroValorPrimeraCuota) }}</small>
              </label>
            </div>

            <div class="quote-policy-notes">
              <p><strong>Tasa % Efectiva Anual:</strong> 26.675 %</p>
              <p>Nota: Cuotas vencen el día ___ de cada mes.</p>
            </div>

            <div class="quote-duedates">
              <div class="quote-duedate-item">
                <span class="quote-mini-icon">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path d="M7 3.5v3m10-3v3M4.5 9.5h15M6.5 5.5h11A2 2 0 0 1 19.5 7.5v10a2 2 0 0 1-2 2h-11a2 2 0 0 1-2-2v-10a2 2 0 0 1 2-2Z" />
                  </svg>
                </span>
                <div>
                  <span>Cotización Válida hasta</span>
                  <strong>--/--/----</strong>
                </div>
              </div>
              <div class="quote-duedate-item">
                <span class="quote-mini-icon">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path d="M12 6v6l4 2m4-2a8 8 0 1 1-16 0 8 8 0 0 1 16 0Z" />
                  </svg>
                </span>
                <div>
                  <span>Fecha Máxima Pago Primera Cuota</span>
                  <strong>--/--/----</strong>
                </div>
              </div>
            </div>
          </article>

          <article class="quote-section">
            <div class="quote-section-title">
              <span class="quote-title-icon">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M7 3.5v3m10-3v3M4.5 9.5h15M6.5 5.5h11A2 2 0 0 1 19.5 7.5v10a2 2 0 0 1-2 2h-11a2 2 0 0 1-2-2v-10a2 2 0 0 1 2-2Z" />
                </svg>
              </span>
              <h2>Plan de Pagos</h2>
            </div>
            <p class="quote-empty-copy">No se ha generado un plan de pagos.</p>
          </article>

          <article class="quote-section">
            <div class="quote-section-title">
              <span class="quote-title-icon">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M7 3.5v3m10-3v3M4.5 9.5h15M6.5 5.5h11A2 2 0 0 1 19.5 7.5v10a2 2 0 0 1-2 2h-11a2 2 0 0 1-2-2v-10a2 2 0 0 1 2-2Z" />
                </svg>
              </span>
              <h2>Documentos</h2>
            </div>
            <p class="quote-empty-copy">No se ha creado la solicitud. No puedes adjuntar documentos.</p>
          </article>

          <article class="quote-section">
            <div class="quote-section-title">
              <span class="quote-title-icon">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M7 3.5v3m10-3v3M4.5 9.5h15M6.5 5.5h11A2 2 0 0 1 19.5 7.5v10a2 2 0 0 1-2 2h-11a2 2 0 0 1-2-2v-10a2 2 0 0 1 2-2Z" />
                </svg>
              </span>
              <h2>Enviar Solicitud</h2>
            </div>
            <p class="quote-empty-copy">A continuación, se debe crear la solicitud.</p>
            <button type="button" class="primary-btn quote-submit-btn">Crear Solicitud</button>
          </article>
        </section>

        <div v-else class="dashboard-grid advisor-summary-grid">
          <article v-for="item in overviewCards" :key="item.id">
            <span>{{ item.label }}</span>
            <strong>{{ item.value }}</strong>
          </article>
        </div>

        <section v-if="activeSection !== 'inicio' && activeSection !== 'cotizador'" class="advisor-workspace">
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

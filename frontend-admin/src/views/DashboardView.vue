<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import {
  createClient,
  createIntermediary,
  createUser,
  deleteClient,
  deleteIntermediary,
  deleteUser,
  fetchClients,
  fetchIntermediaries,
  fetchIntermediaryRelations,
  fetchUsers,
  updateClient,
  updateIntermediary,
  updateUser,
} from "../services/api";
import { clearSession, getSession } from "../services/session";

const router = useRouter();
const session = getSession();
const brandLogo = "https://exxtra.com.co/wp-content/uploads/2019/12/logo-1.png";

const activeSection = ref("usuarios");

const users = ref([]);
const userSearch = ref("");
const isUsersLoading = ref(false);
const isUserSaving = ref(false);
const userFeedback = ref("");
const userErrorMessage = ref("");
const editingUserId = ref(null);
const isUserFormOpen = ref(false);

const clients = ref([]);
const clientSearch = ref("");
const isClientsLoading = ref(false);
const isClientSaving = ref(false);
const clientFeedback = ref("");
const clientErrorMessage = ref("");
const editingClientId = ref(null);
const isClientFormOpen = ref(false);

const intermediaries = ref([]);
const intermediarySearch = ref("");
const isIntermediariesLoading = ref(false);
const isIntermediarySaving = ref(false);
const intermediaryFeedback = ref("");
const intermediaryErrorMessage = ref("");
const editingIntermediaryId = ref(null);
const isIntermediaryFormOpen = ref(false);
const intermediaryRelations = ref(null);
const isRelationsLoading = ref(false);

const adminModules = [
  { id: "usuarios", badge: "U", title: "Usuarios", description: "Accesos, roles y credenciales del sistema." },
  { id: "clientes", badge: "C", title: "Clientes", description: "Consulta y administracion del cliente final." },
  { id: "intermediarios", badge: "I", title: "Intermediarios", description: "Red comercial y actores del negocio." },
  { id: "solicitudes", badge: "S", title: "Solicitudes", description: "Expedientes de credito y seguimiento." },
  { id: "negocios", badge: "N", title: "Negocios", description: "Creditos formalizados y control operativo." },
  { id: "reportes", badge: "R", title: "Reportes", description: "Descargas, tableros y supervision gerencial." },
];

const defaultUserForm = () => ({
  idUsuario: "",
  email: "",
  contrasena: "",
  tipo: "intermediario",
  nombre: "",
  primeravez: "si",
  activo: true,
  verificado: true,
});

const defaultIntermediaryForm = () => ({
  int_nit: "",
  int_nombre: "",
  int_email: "",
  int_ciudad: "",
  int_cel: "",
  int_tel: "",
  fecha: "",
});

const defaultClientForm = () => ({
  cli_cedula: "",
  cli_nombre: "",
  cli_email: "",
  cli_telefono: "",
  cli_cel: "",
  cli_activo: true,
  fecha: "",
});

const userForm = reactive(defaultUserForm());
const clientForm = reactive(defaultClientForm());
const intermediaryForm = reactive(defaultIntermediaryForm());

const roleLabel = computed(() => {
  if (!session?.user?.tipo) return "Sin rol";
  if (session.user.tipo.toLowerCase() === "administrador") return "Administrador";
  if (session.user.tipo.toLowerCase() === "intermediario") return "Intermediario";
  if (session.user.tipo.toLowerCase() === "cliente") return "Cliente";
  return session.user.tipo;
});

const activeModule = computed(
  () => adminModules.find((module) => module.id === activeSection.value) ?? adminModules[0]
);

const formTitle = computed(() => (editingUserId.value ? "Editar usuario" : "Crear usuario"));
const actionLabel = computed(() => (editingUserId.value ? "Guardar cambios" : "Crear usuario"));
const intermediaryFormTitle = computed(() =>
  editingIntermediaryId.value ? "Editar intermediario" : "Crear intermediario"
);
const intermediaryActionLabel = computed(() =>
  editingIntermediaryId.value ? "Guardar cambios" : "Crear intermediario"
);
const usersCount = computed(() => users.value.length);
const clientsCount = computed(() => clients.value.length);
const intermediariesCount = computed(() => intermediaries.value.length);
const activeMetricLabel = computed(() => {
  if (activeSection.value === "clientes") return "Clientes visibles";
  if (activeSection.value === "intermediarios") return "Intermediarios visibles";
  if (activeSection.value === "usuarios") return "Usuarios visibles";
  return "Modulo activo";
});
const activeMetricValue = computed(() => {
  if (activeSection.value === "clientes") return String(clientsCount.value);
  if (activeSection.value === "intermediarios") return String(intermediariesCount.value);
  if (activeSection.value === "usuarios") return String(usersCount.value);
  return activeModule.value.title;
});

function resetUserForm() {
  Object.assign(userForm, defaultUserForm());
  editingUserId.value = null;
  isUserFormOpen.value = false;
}

function resetIntermediaryForm() {
  Object.assign(intermediaryForm, defaultIntermediaryForm());
  editingIntermediaryId.value = null;
  intermediaryRelations.value = null;
  isIntermediaryFormOpen.value = false;
}

function resetClientForm() {
  Object.assign(clientForm, defaultClientForm());
  editingClientId.value = null;
  isClientFormOpen.value = false;
}

async function openSection(sectionId) {
  activeSection.value = sectionId;

  if (sectionId === "usuarios" && !users.value.length) {
    await loadUsers();
  }

  if (sectionId === "clientes" && !clients.value.length) {
    await loadClients();
  }

  if (sectionId === "intermediarios" && !intermediaries.value.length) {
    await loadIntermediaries();
  }
}

async function loadUsers() {
  isUsersLoading.value = true;
  userErrorMessage.value = "";

  try {
    const response = await fetchUsers(userSearch.value.trim());
    users.value = response.data;
  } catch (error) {
    userErrorMessage.value = error.response?.data?.detail || "No fue posible cargar los usuarios.";
  } finally {
    isUsersLoading.value = false;
  }
}

function editUser(user) {
  activeSection.value = "usuarios";
  isUserFormOpen.value = true;
  editingUserId.value = user.id;
  Object.assign(userForm, {
    idUsuario: user.idUsuario,
    email: user.email,
    contrasena: "",
    tipo: user.tipo,
    nombre: user.nombre || "",
    primeravez: user.primeravez || "si",
    activo: user.activo ?? true,
    verificado: user.verificado ?? true,
  });
  userFeedback.value = "";
  userErrorMessage.value = "";
}

function openCreateUser() {
  activeSection.value = "usuarios";
  userFeedback.value = "";
  userErrorMessage.value = "";
  Object.assign(userForm, defaultUserForm());
  editingUserId.value = null;
  isUserFormOpen.value = true;
}

async function submitUser() {
  isUserSaving.value = true;
  userFeedback.value = "";
  userErrorMessage.value = "";

  try {
    const payload = {
      idUsuario: userForm.idUsuario,
      email: userForm.email,
      tipo: userForm.tipo,
      nombre: userForm.nombre || null,
      primeravez: userForm.primeravez,
      activo: userForm.activo,
      verificado: userForm.verificado,
    };

    if (userForm.contrasena) {
      payload.contrasena = userForm.contrasena;
    }

    if (editingUserId.value) {
      delete payload.idUsuario;
      await updateUser(editingUserId.value, payload);
      userFeedback.value = "Usuario actualizado correctamente.";
    } else {
      await createUser(payload);
      userFeedback.value = "Usuario creado correctamente.";
    }

    resetUserForm();
    await loadUsers();
  } catch (error) {
    userErrorMessage.value = error.response?.data?.detail || "No fue posible guardar el usuario.";
  } finally {
    isUserSaving.value = false;
  }
}

async function removeUser(userId) {
  if (!window.confirm("Se eliminara el usuario seleccionado. Deseas continuar?")) {
    return;
  }

  userFeedback.value = "";
  userErrorMessage.value = "";

  try {
    await deleteUser(userId);
    userFeedback.value = "Usuario eliminado correctamente.";
    if (editingUserId.value === userId) {
      resetUserForm();
    }
    await loadUsers();
  } catch (error) {
    userErrorMessage.value = error.response?.data?.detail || "No fue posible eliminar el usuario.";
  }
}

async function loadClients() {
  isClientsLoading.value = true;
  clientErrorMessage.value = "";

  try {
    const response = await fetchClients(clientSearch.value.trim());
    clients.value = response.data;
  } catch (error) {
    clientErrorMessage.value = error.response?.data?.detail || "No fue posible cargar los clientes.";
  } finally {
    isClientsLoading.value = false;
  }
}

function openCreateClient() {
  activeSection.value = "clientes";
  clientFeedback.value = "";
  clientErrorMessage.value = "";
  Object.assign(clientForm, defaultClientForm());
  editingClientId.value = null;
  isClientFormOpen.value = true;
}

function editClient(client) {
  activeSection.value = "clientes";
  clientFeedback.value = "";
  clientErrorMessage.value = "";
  editingClientId.value = client.id;
  Object.assign(clientForm, {
    cli_cedula: client.cli_cedula,
    cli_nombre: client.cli_nombre,
    cli_email: client.cli_email || "",
    cli_telefono: client.cli_telefono || "",
    cli_cel: client.cli_cel || "",
    cli_activo: client.cli_activo ?? true,
    fecha: client.fecha || "",
  });
  isClientFormOpen.value = true;
}

async function submitClient() {
  isClientSaving.value = true;
  clientFeedback.value = "";
  clientErrorMessage.value = "";

  try {
    const payload = {
      cli_cedula: clientForm.cli_cedula,
      cli_nombre: clientForm.cli_nombre,
      cli_email: clientForm.cli_email || null,
      cli_telefono: clientForm.cli_telefono || null,
      cli_cel: clientForm.cli_cel || null,
      cli_activo: clientForm.cli_activo,
      fecha: clientForm.fecha || null,
    };

    if (editingClientId.value) {
      delete payload.cli_cedula;
      await updateClient(editingClientId.value, payload);
      clientFeedback.value = "Cliente actualizado correctamente.";
    } else {
      await createClient(payload);
      clientFeedback.value = "Cliente creado correctamente.";
    }

    resetClientForm();
    await loadClients();
  } catch (error) {
    clientErrorMessage.value = error.response?.data?.detail || "No fue posible guardar el cliente.";
  } finally {
    isClientSaving.value = false;
  }
}

async function removeClient(clientId) {
  if (!window.confirm("Se eliminara el cliente seleccionado. Deseas continuar?")) {
    return;
  }

  clientFeedback.value = "";
  clientErrorMessage.value = "";

  try {
    await deleteClient(clientId);
    clientFeedback.value = "Cliente eliminado correctamente.";
    if (editingClientId.value === clientId) {
      resetClientForm();
    }
    await loadClients();
  } catch (error) {
    clientErrorMessage.value = error.response?.data?.detail || "No fue posible eliminar el cliente.";
  }
}

async function loadIntermediaries() {
  isIntermediariesLoading.value = true;
  intermediaryErrorMessage.value = "";

  try {
    const response = await fetchIntermediaries(intermediarySearch.value.trim());
    intermediaries.value = response.data;
  } catch (error) {
    intermediaryErrorMessage.value =
      error.response?.data?.detail || "No fue posible cargar los intermediarios.";
  } finally {
    isIntermediariesLoading.value = false;
  }
}

async function loadIntermediaryRelations(intermediaryId) {
  isRelationsLoading.value = true;

  try {
    intermediaryRelations.value = await fetchIntermediaryRelations(intermediaryId);
  } catch (error) {
    intermediaryRelations.value = null;
    intermediaryErrorMessage.value =
      error.response?.data?.detail || "No fue posible cargar las relaciones del intermediario.";
  } finally {
    isRelationsLoading.value = false;
  }
}

function openCreateIntermediary() {
  activeSection.value = "intermediarios";
  intermediaryFeedback.value = "";
  intermediaryErrorMessage.value = "";
  Object.assign(intermediaryForm, defaultIntermediaryForm());
  editingIntermediaryId.value = null;
  intermediaryRelations.value = null;
  isIntermediaryFormOpen.value = true;
}

async function editIntermediary(intermediary) {
  activeSection.value = "intermediarios";
  intermediaryFeedback.value = "";
  intermediaryErrorMessage.value = "";
  editingIntermediaryId.value = intermediary.id;
  Object.assign(intermediaryForm, {
    int_nit: intermediary.int_nit,
    int_nombre: intermediary.int_nombre,
    int_email: intermediary.int_email || "",
    int_ciudad: intermediary.int_ciudad || "",
    int_cel: intermediary.int_cel || "",
    int_tel: intermediary.int_tel || "",
    fecha: intermediary.fecha || "",
  });
  isIntermediaryFormOpen.value = true;
  await loadIntermediaryRelations(intermediary.id);
}

async function submitIntermediary() {
  isIntermediarySaving.value = true;
  intermediaryFeedback.value = "";
  intermediaryErrorMessage.value = "";

  try {
    const payload = {
      int_nit: intermediaryForm.int_nit,
      int_nombre: intermediaryForm.int_nombre,
      int_email: intermediaryForm.int_email || null,
      int_ciudad: intermediaryForm.int_ciudad || null,
      int_cel: intermediaryForm.int_cel || null,
      int_tel: intermediaryForm.int_tel || null,
      fecha: intermediaryForm.fecha || null,
    };

    if (editingIntermediaryId.value) {
      delete payload.int_nit;
      await updateIntermediary(editingIntermediaryId.value, payload);
      intermediaryFeedback.value = "Intermediario actualizado correctamente.";
    } else {
      await createIntermediary(payload);
      intermediaryFeedback.value = "Intermediario creado correctamente.";
    }

    resetIntermediaryForm();
    await loadIntermediaries();
  } catch (error) {
    intermediaryErrorMessage.value =
      error.response?.data?.detail || "No fue posible guardar el intermediario.";
  } finally {
    isIntermediarySaving.value = false;
  }
}

async function removeIntermediary(intermediaryId) {
  if (!window.confirm("Se eliminara el intermediario seleccionado. Deseas continuar?")) {
    return;
  }

  intermediaryFeedback.value = "";
  intermediaryErrorMessage.value = "";

  try {
    await deleteIntermediary(intermediaryId);
    intermediaryFeedback.value = "Intermediario eliminado correctamente.";
    if (editingIntermediaryId.value === intermediaryId) {
      resetIntermediaryForm();
    }
    await loadIntermediaries();
  } catch (error) {
    intermediaryErrorMessage.value =
      error.response?.data?.detail || "No fue posible eliminar el intermediario.";
  }
}

function logout() {
  clearSession();
  router.push({ name: "auth", params: { mode: "login" } });
}

onMounted(loadUsers);
</script>

<template>
  <main class="dashboard-shell admin-app-shell">
    <aside class="admin-sidebar">
      <div class="sidebar-brand">
        <img :src="brandLogo" alt="Exxtra" class="brand-logo sidebar-logo" />
        <div>
          <span class="eyebrow">Panel Exxtra</span>
          <h2>Administrador</h2>
        </div>
      </div>

      <div class="sidebar-session">
        <span>Sesion actual</span>
        <strong>{{ session?.user?.idUsuario }}</strong>
        <small>{{ roleLabel }}</small>
      </div>

      <nav class="sidebar-nav">
        <button
          v-for="module in adminModules"
          :key="module.id"
          class="sidebar-link"
          :class="{ active: activeSection === module.id }"
          @click="openSection(module.id)"
        >
          <span class="sidebar-icon">{{ module.badge }}</span>
          <span class="sidebar-copy">
            <strong>{{ module.title }}</strong>
            <small>{{ module.description }}</small>
          </span>
        </button>
      </nav>

      <button class="primary-btn secondary sidebar-logout" @click="logout">Cerrar sesion</button>
    </aside>

    <section class="admin-main">
      <header class="admin-hero">
        <div>
          <span class="eyebrow">{{ activeModule.title }}</span>
          <h1>{{ activeModule.title }}</h1>
          <p>{{ activeModule.description }}</p>
        </div>

        <div class="hero-metrics">
          <article class="hero-card">
            <span>{{ activeMetricLabel }}</span>
            <strong>{{ activeMetricValue }}</strong>
          </article>
          <article class="hero-card">
            <span>Rol actual</span>
            <strong>{{ roleLabel }}</strong>
          </article>
        </div>
      </header>

      <template v-if="activeSection === 'usuarios'">
        <section class="admin-panel users-workspace">
          <div class="users-header">
            <div>
              <span class="eyebrow">Modulo activo</span>
              <h2>Usuarios del sistema</h2>
              <p>
                Administra accesos, roles y estados del personal operativo sin mezclar el listado
                con el formulario principal.
              </p>
            </div>

            <div class="users-header-actions">
              <button class="ghost-btn" @click="loadUsers">Actualizar</button>
              <button class="primary-btn users-create-btn" @click="openCreateUser">Nuevo usuario</button>
            </div>
          </div>

          <div class="admin-toolbar users-toolbar">
            <input
              v-model.trim="userSearch"
              class="toolbar-search"
              placeholder="Buscar por usuario, correo, tipo o nombre"
            />
            <button class="ghost-btn" @click="loadUsers">Buscar</button>
          </div>

          <p v-if="userFeedback" class="feedback success">{{ userFeedback }}</p>
          <p v-if="userErrorMessage" class="feedback error">{{ userErrorMessage }}</p>

          <p v-if="isUsersLoading" class="empty-state">Cargando usuarios...</p>

          <div v-else-if="users.length" class="user-list">
            <article v-for="user in users" :key="user.id" class="user-card">
              <div class="user-card-main">
                <div>
                  <strong>{{ user.idUsuario }}</strong>
                  <p>{{ user.email }}</p>
                </div>
                <span class="status-badge">{{ user.tipo }}</span>
              </div>

              <div class="user-meta">
                <span>{{ user.nombre || "Sin nombre" }}</span>
                <span>{{ user.activo ? "Activo" : "Inactivo" }}</span>
                <span>{{ user.verificado ? "Verificado" : "Pendiente" }}</span>
              </div>

              <div class="user-actions">
                <button class="ghost-btn" @click="editUser(user)">Editar</button>
                <button class="ghost-btn danger" @click="removeUser(user.id)">Eliminar</button>
              </div>
            </article>
          </div>

          <p v-else class="empty-state">No hay usuarios para mostrar con ese filtro.</p>
        </section>

        <transition name="drawer-fade">
          <div v-if="isUserFormOpen" class="drawer-backdrop" @click.self="resetUserForm">
            <section class="user-form-drawer">
              <div class="admin-section-header">
                <div>
                  <span class="eyebrow">Gestion de acceso</span>
                  <h2>{{ formTitle }}</h2>
                  <p class="drawer-copy">
                    {{
                      editingUserId
                        ? "Actualiza datos y permisos del usuario seleccionado."
                        : "Crea una nueva cuenta administrativa, de intermediario o cliente."
                    }}
                  </p>
                </div>
                <button class="ghost-btn" @click="resetUserForm">Cerrar</button>
              </div>

              <form class="admin-form" @submit.prevent="submitUser">
                <label>
                  <span>Id usuario</span>
                  <input v-model.trim="userForm.idUsuario" :disabled="Boolean(editingUserId)" required />
                </label>

                <label>
                  <span>Correo</span>
                  <input v-model.trim="userForm.email" type="email" required />
                </label>

                <label>
                  <span>Contrasena</span>
                  <input
                    v-model="userForm.contrasena"
                    type="password"
                    :placeholder="editingUserId ? 'Solo diligencia si deseas cambiarla' : 'Minimo 6 caracteres'"
                    :required="!editingUserId"
                  />
                </label>

                <label>
                  <span>Tipo</span>
                  <select v-model="userForm.tipo">
                    <option value="administrador">Administrador</option>
                    <option value="intermediario">Intermediario</option>
                    <option value="cliente">Cliente</option>
                  </select>
                </label>

                <label>
                  <span>Nombre</span>
                  <input v-model.trim="userForm.nombre" placeholder="Nombre visible del usuario" />
                </label>

                <label>
                  <span>Primeravez</span>
                  <select v-model="userForm.primeravez">
                    <option value="si">si</option>
                    <option value="no">no</option>
                  </select>
                </label>

                <label class="switch-row">
                  <input v-model="userForm.activo" type="checkbox" />
                  <span>Usuario activo</span>
                </label>

                <label class="switch-row">
                  <input v-model="userForm.verificado" type="checkbox" />
                  <span>Usuario verificado</span>
                </label>

                <button class="primary-btn" :disabled="isUserSaving">
                  {{ isUserSaving ? "Guardando..." : actionLabel }}
                </button>
              </form>
            </section>
          </div>
        </transition>
      </template>

      <template v-else-if="activeSection === 'clientes'">
        <section class="admin-panel users-workspace">
          <div class="users-header">
            <div>
              <span class="eyebrow">Modulo activo</span>
              <h2>Clientes</h2>
              <p>
                Gestiona los clientes finales, su estado y sus datos de contacto dentro del flujo
                operativo de Exxtra.
              </p>
            </div>

            <div class="users-header-actions">
              <button class="ghost-btn" @click="loadClients">Actualizar</button>
              <button class="primary-btn users-create-btn" @click="openCreateClient">
                Nuevo cliente
              </button>
            </div>
          </div>

          <div class="admin-toolbar users-toolbar">
            <input
              v-model.trim="clientSearch"
              class="toolbar-search"
              placeholder="Buscar por cedula, nombre, correo o telefono"
            />
            <button class="ghost-btn" @click="loadClients">Buscar</button>
          </div>

          <p v-if="clientFeedback" class="feedback success">{{ clientFeedback }}</p>
          <p v-if="clientErrorMessage" class="feedback error">{{ clientErrorMessage }}</p>

          <p v-if="isClientsLoading" class="empty-state">Cargando clientes...</p>

          <div v-else-if="clients.length" class="user-list">
            <article v-for="client in clients" :key="client.id" class="user-card">
              <div class="user-card-main">
                <div>
                  <strong>{{ client.cli_nombre }}</strong>
                  <p>Cedula {{ client.cli_cedula }}</p>
                </div>
                <span class="status-badge">{{ client.cli_activo ? "Activo" : "Inactivo" }}</span>
              </div>

              <div class="user-meta">
                <span>{{ client.cli_email || "Sin correo" }}</span>
                <span>{{ client.cli_cel || "Sin celular" }}</span>
                <span>{{ client.cli_telefono || "Sin telefono" }}</span>
              </div>

              <div class="user-actions">
                <button class="ghost-btn" @click="editClient(client)">Editar</button>
                <button class="ghost-btn danger" @click="removeClient(client.id)">Eliminar</button>
              </div>
            </article>
          </div>

          <p v-else class="empty-state">No hay clientes para mostrar con ese filtro.</p>
        </section>

        <transition name="drawer-fade">
          <div v-if="isClientFormOpen" class="drawer-backdrop" @click.self="resetClientForm">
            <section class="user-form-drawer">
              <div class="admin-section-header">
                <div>
                  <span class="eyebrow">Cliente final</span>
                  <h2>{{ editingClientId ? "Editar cliente" : "Crear cliente" }}</h2>
                  <p class="drawer-copy">
                    {{
                      editingClientId
                        ? "Actualiza la informacion del cliente seleccionado."
                        : "Crea un nuevo cliente para vincularlo al flujo comercial y crediticio."
                    }}
                  </p>
                </div>
                <button class="ghost-btn" @click="resetClientForm">Cerrar</button>
              </div>

              <form class="admin-form" @submit.prevent="submitClient">
                <label>
                  <span>Cedula</span>
                  <input
                    v-model.trim="clientForm.cli_cedula"
                    :disabled="Boolean(editingClientId)"
                    required
                  />
                </label>

                <label>
                  <span>Nombre</span>
                  <input v-model.trim="clientForm.cli_nombre" required />
                </label>

                <label>
                  <span>Correo</span>
                  <input v-model.trim="clientForm.cli_email" type="email" />
                </label>

                <label>
                  <span>Telefono</span>
                  <input v-model.trim="clientForm.cli_telefono" />
                </label>

                <label>
                  <span>Celular</span>
                  <input v-model.trim="clientForm.cli_cel" />
                </label>

                <label>
                  <span>Fecha</span>
                  <input v-model.trim="clientForm.fecha" type="date" />
                </label>

                <label class="switch-row">
                  <input v-model="clientForm.cli_activo" type="checkbox" />
                  <span>Cliente activo</span>
                </label>

                <button class="primary-btn" :disabled="isClientSaving">
                  {{ isClientSaving ? "Guardando..." : editingClientId ? "Guardar cambios" : "Crear cliente" }}
                </button>
              </form>
            </section>
          </div>
        </transition>
      </template>

      <template v-else-if="activeSection === 'intermediarios'">
        <section class="admin-panel users-workspace">
          <div class="users-header">
            <div>
              <span class="eyebrow">Modulo activo</span>
              <h2>Intermediarios</h2>
              <p>
                Gestiona la red comercial, sus datos de contacto y las relaciones operativas ya
                creadas dentro del sistema.
              </p>
            </div>

            <div class="users-header-actions">
              <button class="ghost-btn" @click="loadIntermediaries">Actualizar</button>
              <button class="primary-btn users-create-btn" @click="openCreateIntermediary">
                Nuevo intermediario
              </button>
            </div>
          </div>

          <div class="admin-toolbar users-toolbar">
            <input
              v-model.trim="intermediarySearch"
              class="toolbar-search"
              placeholder="Buscar por nit, nombre, correo o ciudad"
            />
            <button class="ghost-btn" @click="loadIntermediaries">Buscar</button>
          </div>

          <p v-if="intermediaryFeedback" class="feedback success">{{ intermediaryFeedback }}</p>
          <p v-if="intermediaryErrorMessage" class="feedback error">{{ intermediaryErrorMessage }}</p>

          <p v-if="isIntermediariesLoading" class="empty-state">Cargando intermediarios...</p>

          <div v-else-if="intermediaries.length" class="user-list">
            <article v-for="intermediary in intermediaries" :key="intermediary.id" class="user-card">
              <div class="user-card-main">
                <div>
                  <strong>{{ intermediary.int_nombre }}</strong>
                  <p>NIT {{ intermediary.int_nit }}</p>
                </div>
                <span class="status-badge">{{ intermediary.int_ciudad || "Sin ciudad" }}</span>
              </div>

              <div class="user-meta">
                <span>{{ intermediary.int_email || "Sin correo" }}</span>
                <span>{{ intermediary.int_cel || "Sin celular" }}</span>
                <span>{{ intermediary.int_tel || "Sin telefono" }}</span>
              </div>

              <div class="user-actions">
                <button class="ghost-btn" @click="editIntermediary(intermediary)">Editar</button>
                <button class="ghost-btn danger" @click="removeIntermediary(intermediary.id)">
                  Eliminar
                </button>
              </div>
            </article>
          </div>

          <p v-else class="empty-state">No hay intermediarios para mostrar con ese filtro.</p>
        </section>

        <transition name="drawer-fade">
          <div v-if="isIntermediaryFormOpen" class="drawer-backdrop" @click.self="resetIntermediaryForm">
            <section class="user-form-drawer">
              <div class="admin-section-header">
                <div>
                  <span class="eyebrow">Red comercial</span>
                  <h2>{{ intermediaryFormTitle }}</h2>
                  <p class="drawer-copy">
                    {{
                      editingIntermediaryId
                        ? "Actualiza datos de contacto y revisa la relacion del intermediario con otros modulos."
                        : "Crea un nuevo intermediario para integrarlo al flujo comercial y operativo."
                    }}
                  </p>
                </div>
                <button class="ghost-btn" @click="resetIntermediaryForm">Cerrar</button>
              </div>

              <form class="admin-form" @submit.prevent="submitIntermediary">
                <label>
                  <span>NIT</span>
                  <input
                    v-model.trim="intermediaryForm.int_nit"
                    :disabled="Boolean(editingIntermediaryId)"
                    required
                  />
                </label>

                <label>
                  <span>Nombre</span>
                  <input v-model.trim="intermediaryForm.int_nombre" required />
                </label>

                <label>
                  <span>Correo</span>
                  <input v-model.trim="intermediaryForm.int_email" type="email" />
                </label>

                <label>
                  <span>Ciudad</span>
                  <input v-model.trim="intermediaryForm.int_ciudad" placeholder="Codigo de ciudad" />
                </label>

                <label>
                  <span>Celular</span>
                  <input v-model.trim="intermediaryForm.int_cel" />
                </label>

                <label>
                  <span>Telefono</span>
                  <input v-model.trim="intermediaryForm.int_tel" />
                </label>

                <label>
                  <span>Fecha</span>
                  <input v-model.trim="intermediaryForm.fecha" type="date" />
                </label>

                <button class="primary-btn" :disabled="isIntermediarySaving">
                  {{ isIntermediarySaving ? "Guardando..." : intermediaryActionLabel }}
                </button>
              </form>

              <section v-if="editingIntermediaryId" class="relations-panel">
                <div class="relations-header">
                  <span class="eyebrow">Relaciones</span>
                  <strong>{{ isRelationsLoading ? "Cargando..." : "Contexto operativo" }}</strong>
                </div>

                <div v-if="intermediaryRelations" class="relations-grid">
                  <article class="relation-card">
                    <span>Usuarios asociados</span>
                    <strong>{{ intermediaryRelations.linked_users.length }}</strong>
                  </article>
                  <article class="relation-card">
                    <span>Negocios vinculados</span>
                    <strong>{{ intermediaryRelations.related_new_business_count }}</strong>
                  </article>
                </div>

                <div v-if="intermediaryRelations?.linked_users?.length" class="relation-users">
                  <article
                    v-for="linkedUser in intermediaryRelations.linked_users"
                    :key="linkedUser.id"
                    class="relation-user-card"
                  >
                    <strong>{{ linkedUser.idUsuario }}</strong>
                    <span>{{ linkedUser.email }}</span>
                  </article>
                </div>

                <p
                  v-else-if="!isRelationsLoading"
                  class="empty-state relation-empty"
                >
                  Este intermediario aun no tiene usuarios asociados.
                </p>
              </section>
            </section>
          </div>
        </transition>
      </template>

      <section v-else class="admin-panel module-placeholder">
        <div class="module-placeholder-copy">
          <span class="eyebrow">Modulo en preparacion</span>
          <h2>{{ activeModule.title }}</h2>
          <p>
            Este espacio ya esta reservado dentro del panel administrativo para que el flujo del
            administrador crezca de forma ordenada y consistente con la identidad de Exxtra.
          </p>
        </div>

        <div class="placeholder-grid">
          <article class="placeholder-card">
            <strong>Objetivo</strong>
            <p>{{ activeModule.description }}</p>
          </article>
          <article class="placeholder-card">
            <strong>Siguiente paso</strong>
            <p>Conectar este modulo a sus endpoints y reportes sin rehacer la navegacion principal.</p>
          </article>
          <article class="placeholder-card">
            <strong>Estado</strong>
            <p>Listo para evolucionar dentro del mismo layout administrativo.</p>
          </article>
        </div>
      </section>
    </section>
  </main>
</template>

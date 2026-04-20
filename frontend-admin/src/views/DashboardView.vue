<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { createUser, deleteUser, fetchUsers, updateUser } from "../services/api";
import { clearSession, getSession } from "../services/session";

const router = useRouter();
const session = getSession();
const brandLogo = "https://exxtra.com.co/wp-content/uploads/2019/12/logo-1.png";

const users = ref([]);
const search = ref("");
const isLoading = ref(false);
const isSaving = ref(false);
const feedback = ref("");
const errorMessage = ref("");
const editingUserId = ref(null);
const activeSection = ref("usuarios");
const isFormOpen = ref(false);

const adminModules = [
  { id: "usuarios", badge: "U", title: "Usuarios", description: "Accesos, roles y credenciales del sistema." },
  { id: "clientes", badge: "C", title: "Clientes", description: "Consulta y administracion del cliente final." },
  { id: "intermediarios", badge: "I", title: "Intermediarios", description: "Red comercial y actores del negocio." },
  { id: "solicitudes", badge: "S", title: "Solicitudes", description: "Expedientes de credito y seguimiento." },
  { id: "negocios", badge: "N", title: "Negocios", description: "Creditos formalizados y control operativo." },
  { id: "reportes", badge: "R", title: "Reportes", description: "Descargas, tableros y supervision gerencial." },
];

const defaultForm = () => ({
  idUsuario: "",
  email: "",
  contrasena: "",
  tipo: "intermediario",
  nombre: "",
  primeravez: "si",
  activo: true,
  verificado: true,
});

const userForm = reactive(defaultForm());

const roleLabel = computed(() => {
  if (!session?.user?.tipo) return "Sin rol";
  if (session.user.tipo.toLowerCase() === "administrador") return "Administrador";
  if (session.user.tipo.toLowerCase() === "intermediario") return "Intermediario";
  return session.user.tipo;
});

const activeModule = computed(
  () => adminModules.find((module) => module.id === activeSection.value) ?? adminModules[0]
);

const formTitle = computed(() => (editingUserId.value ? "Editar usuario" : "Crear usuario"));
const actionLabel = computed(() => (editingUserId.value ? "Guardar cambios" : "Crear usuario"));
const usersCount = computed(() => users.value.length);

function resetForm() {
  Object.assign(userForm, defaultForm());
  editingUserId.value = null;
  isFormOpen.value = false;
}

function openSection(sectionId) {
  activeSection.value = sectionId;
  feedback.value = "";
  errorMessage.value = "";
}

async function loadUsers() {
  isLoading.value = true;
  errorMessage.value = "";

  try {
    const response = await fetchUsers(search.value.trim());
    users.value = response.data;
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "No fue posible cargar los usuarios.";
  } finally {
    isLoading.value = false;
  }
}

function editUser(user) {
  activeSection.value = "usuarios";
  isFormOpen.value = true;
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
  feedback.value = "";
  errorMessage.value = "";
}

function openCreateUser() {
  activeSection.value = "usuarios";
  feedback.value = "";
  errorMessage.value = "";
  Object.assign(userForm, defaultForm());
  editingUserId.value = null;
  isFormOpen.value = true;
}

async function submitUser() {
  isSaving.value = true;
  feedback.value = "";
  errorMessage.value = "";

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
      feedback.value = "Usuario actualizado correctamente.";
    } else {
      await createUser(payload);
      feedback.value = "Usuario creado correctamente.";
    }

    resetForm();
    await loadUsers();
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "No fue posible guardar el usuario.";
  } finally {
    isSaving.value = false;
  }
}

async function removeUser(userId) {
  if (!window.confirm("Se eliminara el usuario seleccionado. Deseas continuar?")) {
    return;
  }

  feedback.value = "";
  errorMessage.value = "";

  try {
    await deleteUser(userId);
    feedback.value = "Usuario eliminado correctamente.";
    if (editingUserId.value === userId) {
      resetForm();
    }
    await loadUsers();
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "No fue posible eliminar el usuario.";
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
            <span>Usuarios visibles</span>
            <strong>{{ usersCount }}</strong>
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
              v-model.trim="search"
              class="toolbar-search"
              placeholder="Buscar por usuario, correo, tipo o nombre"
            />
            <button class="ghost-btn" @click="loadUsers">Buscar</button>
          </div>

          <p v-if="feedback" class="feedback success">{{ feedback }}</p>
          <p v-if="errorMessage" class="feedback error">{{ errorMessage }}</p>

          <p v-if="isLoading" class="empty-state">Cargando usuarios...</p>

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
          <div v-if="isFormOpen" class="drawer-backdrop" @click.self="resetForm">
            <section class="user-form-drawer">
              <div class="admin-section-header">
              <div>
                  <span class="eyebrow">Gestion de acceso</span>
                <h2>{{ formTitle }}</h2>
                  <p class="drawer-copy">
                    {{ editingUserId ? "Actualiza datos y permisos del usuario seleccionado." : "Crea una nueva cuenta administrativa, de intermediario o cliente." }}
                  </p>
              </div>
                <button class="ghost-btn" @click="resetForm">Cerrar</button>
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

                <button class="primary-btn" :disabled="isSaving">
                  {{ isSaving ? "Guardando..." : actionLabel }}
                </button>
              </form>
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

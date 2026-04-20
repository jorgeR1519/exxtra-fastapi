# Exxtra Platform

Repositorio del sistema **Exxtra**, orientado a la administracion de creditos asociados a polizas/seguros, su formalizacion, seguimiento de cartera y canales de pago.

## Descripcion General

Exxtra no es solo un sistema de usuarios. Es una plataforma operativa para gestionar el ciclo completo del credito:

- autenticacion de cuentas
- administracion de clientes e intermediarios
- registro de solicitudes de credito
- formalizacion en negocios nuevos
- seguimiento de saldos y planes de pago
- integracion con pagos Payzen
- consultas desde canales externos
- generacion de reportes
- manejo de catalogos maestros

En terminos de negocio, el flujo principal es:

1. se autentica un actor del sistema
2. se registran o consultan clientes e intermediarios
3. se crea una solicitud de credito
4. la solicitud puede convertirse en un negocio nuevo
5. el negocio se administra con saldos, cuotas y pagos
6. la operacion se apoya en reportes e integraciones externas

## Estructura Del Repositorio

El proyecto esta organizado en tres aplicaciones principales:

### `backend/`

Backend en **FastAPI** encargado de la API, autenticacion, logica de negocio y acceso a MongoDB.

Incluye:

- rutas REST
- servicios
- repositorios
- esquemas Pydantic
- integraciones externas
- pruebas

### `frontend-admin/`

Frontend en **Vue 3 + Vite** para el panel administrativo.

Pensado para crecer hacia modulos como:

- usuarios
- clientes
- intermediarios
- solicitudes
- negocios nuevos
- reportes

### `frontend-intermediarios/`

Frontend en **Vue 3 + Vite** para el portal de intermediarios.

Pensado para crecer hacia modulos como:

- login del intermediario
- seguimiento de solicitudes
- gestion comercial
- consulta de clientes
- seguimiento de pipeline

## Stack Tecnologico

### Backend

- FastAPI
- PyMongo
- MongoDB
- PyJWT
- bcrypt
- Pydantic Settings
- pytest

### Frontend

- Vue 3
- Vue Router
- Vite
- Axios

## Modulos De Negocio

Los modulos principales del sistema son:

- `usuarios`: autenticacion, permisos y tipos de cuenta
- `clientes`: informacion base del cliente
- `intermediarios`: informacion base del intermediario
- `solicitud_de_credito`: expediente inicial del credito
- `negocios_nuevos`: credito formalizado
- `saldos`: estado actual de deuda y mora
- `planes_de_pagos`: cuotas y vencimientos
- `pagos_payzen`: integracion de pagos
- catalogos: ciudades, ramos, aseguradoras, variables, lineas, onerosos, CIUU

## Estado Actual

Actualmente el repositorio ya cuenta con:

- backend organizado en arquitectura por capas
- autenticacion con JWT
- modulo funcional de clientes
- modulo funcional de intermediarios
- base visual inicial para login y registro en admin e intermediarios
- soporte de CORS para ambos frontends

## Endpoints Base De Autenticacion

Los endpoints actuales de autenticacion son:

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/register`
- `GET /api/v1/auth/me`

## Como Levantar El Proyecto

### 1. Backend

Desde la raiz del repositorio:

```powershell
cd backend
..\venv\Scripts\python -m uvicorn app.main:app --reload
```

El backend quedara disponible en:

```text
http://127.0.0.1:8000
```

### 2. Frontend Administrador

```powershell
cd frontend-admin
npm install
npm run dev
```

Disponible en:

```text
http://127.0.0.1:5173
```

### 3. Frontend Intermediarios

```powershell
cd frontend-intermediarios
npm install
npm run dev
```

Disponible en:

```text
http://127.0.0.1:5174
```

## Variables De Entorno

Las variables del backend estan dentro de:

- `backend/.env`
- `backend/.env.example`

Las mas importantes son:

- `MONGODB_URI`
- `MONGODB_DB_NAME`
- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`

## Pruebas

Para ejecutar las pruebas principales del backend:

```powershell
cd backend
..\venv\Scripts\python -m pytest app\tests\test_auth.py app\tests\test_intermediaries.py -q
```

## Objetivo Del Proyecto

El objetivo de esta migracion es reemplazar el backend legado en Node.js por una plataforma mas mantenible en FastAPI, conservando la logica del negocio y separando la experiencia de usuario por perfil operativo:

- un frontend para administradores
- un frontend para intermediarios
- un backend comun y centralizado

## Siguientes Pasos Recomendados

- construir dashboards reales por rol
- migrar solicitudes de credito
- migrar negocios nuevos
- migrar saldos y planes de pago
- integrar pagos Payzen desde la nueva arquitectura
- completar reportes y consultas externas

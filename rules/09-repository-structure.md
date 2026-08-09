---
id: repository-structure
title: Estructura de Repositorio
status: Definida
tags: [structure, monorepo, backend, frontend, shared, multi-language, scaffolding]
---

# Regla 09: Estructura de Repositorio

## Premisa

Todo proyecto consumidor debe seguir una estructura de repositorio predecible y multi-lenguaje, organizada por **rol** (`backend`, `frontend`, `shared`) y **lenguaje** (`java`, `nodejs`, `python`, `rust`). Un mismo proyecto puede combinar múltiples roles y lenguajes (ej: backend Java + frontend NodeJS + libs compartidas). Los helpers constituyen la capa única de ejecución compartida en la raíz del repositorio, nunca duplicada por lenguaje.

## Estructura

### Tree completo

```
proyecto/
├── Makefile                         # orquestación de build (incluye helpers/mk/*.mk)
├── Justfile                         # operativas de aplicación
├── mkdocs.yml                       # configuración de documentación (→ .config/mkdocs/)
│
├── docs/                            # documentación en Markdown + MermaidJS
│   └── .gitkeep
│
├── site/                            # (generado) no se versiona
│
├── helpers/                         # capa única de ejecución compartida
│   ├── mk/                          # módulos Makefile: build.mk, container.mk, docs.mk, ...
│   ├── shell/                       # scripts shell: build.sh, java.sh, container.sh, lint.sh, ...
│   ├── python/                      # helpers python opcionales
│   └── just/                        # operativas de aplicación: app.just, auth.just, ...
│
├── containers/                      # definiciones de imágenes
│   └── Containerfile                # imagen CI base
│
├── mcp/                             # SUGERENCIA — MCP opcional (ver regla 07)
│   └── mcp-config.json
│
└── source/                          # código fuente por rol + lenguaje
    ├── backend/                     # APIs, servicios
    │   ├── java/                    # Maven / Gradle
    │   │   └── <proyecto>/          # kebab-case: patos, orders, users
    │   │       ├── pom.xml          # o build.gradle
    │   │       └── src/
    │   │           ├── main/java/com/example/
    │   │           │   ├── domain/
    │   │           │   ├── application/
    │   │           │   ├── infrastructure/
    │   │           │   └── ports/
    │   │           └── test/java/com/example/
    │   ├── python/                  # uv / poetry
    │   │   └── <proyecto>/
    │   │       ├── pyproject.toml
    │   │       └── src/
    │   └── rust/                    # Cargo
    │       └── <proyecto>/
    │           ├── Cargo.toml
    │           └── src/
    │
    ├── frontend/                    # interfaces de usuario
    │   └── nodejs/                  # npm / pnpm
    │       └── <proyecto>/          # kebab-case: web, dashboard, admin
    │           ├── package.json
    │           └── src/
    │
    └── shared/                      # código compartido entre roles
        └── libs/                    # domain, types, contracts
            └── <proyecto>/
                └── src/
```

### Roles definidos

| Rol | Propósito | Contiene |
|-----|-----------|----------|
| `backend/` | APIs, servicios, workers, tareas asíncronas | `java/`, `python/`, `rust/` |
| `frontend/` | Interfaces de usuario, clientes web | `nodejs/`, `javascript/` |
| `shared/` | Código usado por ambos roles | `libs/`, `domain/`, `contracts/`, `types/` |

> Nota: bajo `backend/` y `frontend/` puede haber más de un lenguaje, pero cada proyecto (`<proyecto>/`) pertenece a un solo lenguaje.

## Nombres Sugeridos

- **Roles:** `backend`, `frontend`, `shared` — en minúsculas, sin plurales.
- **Lenguajes:** `java`, `python`, `rust`, `nodejs`, `javascript`. El nombre del lenguaje refleja el ecosistema de build (`java` usa Maven/Gradle; `nodejs` usa npm/pnpm).
- **Proyectos:** `kebab-case`: `patos`, `web`, `dashboard`, `users`, `domain`, `contracts`.
- **Subdirectorios de helpers:** `mk`, `shell`, `python`, `just` — idénticos bajo `helpers/` y `templates/`.
- `site/` nunca versionado (`.gitignore`).

## Comandos

### Scaffolding del repositorio

```bash
# Crear la estructura base de source/
mkdir -p source/{backend/{java,python,rust},frontend/nodejs,shared/libs}

# Backend Java (Maven)
mkdir -p source/backend/java/patos/src/{main/java/com/patos/{domain,application,infrastructure,ports},main/resources,test/java/com/patos}
mvn archetype:generate -DgroupId=com.patos -DartifactId=patos

# Backend Java (Gradle)
mkdir -p source/backend/java/patos/src/{main/java/com/patos/{domain,application,infrastructure,ports},main/resources,test/java/com/patos}
gradle init --type java-application

# Frontend NodeJS
mkdir -p source/frontend/nodejs/web/src
cd source/frontend/nodejs/web && npm init

# Shared libs
mkdir -p source/shared/libs/domain/src
```

### Crear helpers (copiando de templates)

```bash
# Los templates/helpers/*.tmpl se copian a helpers/ en el proyecto consumidor.
# Un agente puede iterar sobre templates/helpers/ y copiar cada .tmpl → helpers/<destino>.
cp templates/helpers/mk/*.tmpl helpers/mk/
cp templates/helpers/shell/*.tmpl helpers/shell/
```

## Ejemplos

### Proyecto "patos" — backend Java + frontend NodeJS + libs compartidas

```
source/
├── backend/
│   └── java/
│       └── patos/
│           ├── pom.xml
│           └── src/
│               ├── main/java/com/patos/
│               │   ├── domain/
│               │   │   ├── models/Pato.java
│               │   │   └── services/PatoService.java
│               │   ├── application/
│               │   │   └── CreatePatoUseCase.java
│               │   ├── infrastructure/
│               │   │   ├── web/PatoController.java
│               │   │   └── persistence/JpaPatoRepository.java
│               │   └── ports/
│               │       └── PatoRepository.java
│               └── test/java/com/patos/
│
├── frontend/
│   └── nodejs/
│       └── web/
│           ├── package.json
│           └── src/
│               ├── components/PatoCard.jsx
│               └── pages/Dashboard.jsx
│
└── shared/
    └── libs/
        └── domain/
            └── src/
                └── PatoDto.java
```

### Invocación desde la raíz (orquestación multi-lenguaje)

```bash
make build  LANG=java       BUILD_TOOL=maven  MODULE=source/backend/java/patos
make build  LANG=javascript BUILD_TOOL=pnpm   MODULE=source/frontend/nodejs/web
make test   LANG=java       BUILD_TOOL=maven  MODULE=source/backend/java/patos
make test   LANG=javascript BUILD_TOOL=pnpm   MODULE=source/frontend/nodejs/web
```

## Restricciones

- **`source/` no mezcla roles dentro de la misma carpeta:** cada rol (`backend/`, `frontend/`, `shared/`) es una carpeta independiente.
- **Helpers en raíz, nunca duplicados:** `helpers/` está en la raíz del repositorio y es compartido por todos los roles. No se replica dentro de `source/backend/java/` ni `source/frontend/nodejs/`.
- **Un proyecto pertenece a un solo rol y un solo lenguaje:** `source/backend/java/patos/` es backend Java. Si hay un frontend, va en `source/frontend/nodejs/web/`.
- **`site/` y artefactos de build no se versionan** (`site/`, `target/`, `dist/`, `build/`, `node_modules/`).
- **No mezclar gestores de paquetes** en el mismo proyecto: un `pom.xml` o `build.gradle`, no ambos. Igual para frontend: `package.json` con un solo gestor (`npm`, `pnpm` o `yarn`).
- **El rol `shared/` no debe contener lógica de infraestructura** (HTTP, persistencia). Solo DTOs, tipos, contratos, validaciones.
- **Cada proyecto (`<proyecto>/`) tiene su propia herramienta de build** — no hay un pom.xml global ni un package.json raíz. La orquestación es responsabilidad del Makefile en la raíz.

## Referencias

- [Regla 01: Build Tooling](01-build-tooling.md) — Makefile, Justfile, capa de helpers.
- [Regla 02: Arquitectura Hexagonal](02-architecture.md) — domain/application/infrastructure/ports.
- [Regla 08: Stack Tecnológico](08-stack.md) — versiones, Podman, Containerfile, Alpine.
- [Regla 12: Gitignore](12-gitignore.md) — exclusión de archivos por contexto y plantillas.
- [Regla 14: Archivos de Configuración](14-config-files.md) — `.config/` centraliza configuraciones de herramientas.
- [templates/repository-structure/README.md](../templates/repository-structure/README.md) — documentación de la estructura junto al template.
- [templates/helpers/mk/](../templates/repository-structure/helpers/mk/) y [templates/helpers/shell/](../templates/repository-structure/helpers/shell/) — origen de los helpers copiados a `helpers/`.
- [templates/gitignore/](../templates/gitignore/) — biblioteca de `.gitignore` por contexto.

## Plantilla

- [templates/repository-structure/](../templates/repository-structure/) — estructura completa con placeholders para copiar.
- [templates/helpers/mk/](../templates/repository-structure/helpers/mk/) — módulos Makefile.
- [templates/helpers/shell/](../templates/repository-structure/helpers/shell/) — scripts shell por lenguaje.
- [templates/helpers/just/](../templates/repository-structure/helpers/just/) — operativas de aplicación.
- [templates/Containerfile.tmpl](../templates/repository-structure/containers/Containerfile.tmpl) — definición de imagen CI.
- [templates/gitignore/](../templates/gitignore/) — biblioteca de `.gitignore` por ubicación (raíz, java, python, rust, nodejs, container, secretos, temporales, mcp).

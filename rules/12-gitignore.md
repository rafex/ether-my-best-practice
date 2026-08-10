---
id: gitignore
title: Gitignore y Exclusión de Archivos
status: Definida
tags: [git, gitignore, secrets, artifacts, templates, security]
---

# Regla 12: Gitignore y Exclusión de Archivos



### Premisa: Premisa

Todo repositorio debe tener un archivo `.gitignore` en la raíz del proyecto, y uno por cada ubicación de código fuente (`source/<rol>/<lenguaje>/<proyecto>/`) con las exclusiones específicas de ese lenguaje. Se disponibiliza una biblioteca de templates en `templates/gitignore/` para que el agente de IA elija los adecuados según el tipo de proyecto, combinando templates de raíz, lenguaje y complementos (secretos, temporales, MCP).

tags: [obligatorio]

### Estructura: Estructura

### Biblioteca de templates

| Template | Destino en el proyecto | Qué excluye |
|---|---|---|
| `.gitignore.raiz.tmpl` | `proyecto/.gitignore` | `site/`, `.githooks/.tools/.commitizen-venv/`, IDE (`.vscode/`, `.idea/`, `*.swp`), `.DS_Store`, `*~` |
| `.gitignore.java.tmpl` | `source/backend/java/<proyecto>/` | `target/`, `*.class`, `*.jar`, `*.war`, `.gradle/`, `bin/`, `*.log` |
| `.gitignore.python.tmpl` | `source/backend/python/<proyecto>/` | `__pycache__/`, `*.py[cod]`, `.venv/`, `venv/`, caches pytest/ruff/mypy, `dist/`, `build/`, `*.egg-info/` |
| `.gitignore.rust.tmpl` | `source/backend/rust/<proyecto>/` | `target/`, `*.rs.bk`, `Cargo.lock` (comentado) |
| `.gitignore.nodejs.tmpl` | `source/frontend/nodejs/<proyecto>/` | `node_modules/`, `dist/`, `build/`, `.next/`, `.nuxt/`, `coverage/`, `*.log`, `.env` |
| `.gitignore.container.tmpl` | `containers/` | `.env`, `*.tar`, caches de build/imágenes locales |
| `.gitignore.secretos.tmpl` | complemento combinable | `.env*`, `*.pem`, `*.key`, `*.p12`, `*.jks`, `.aws/`, `.ssh/`, credenciales |
| `.gitignore.temporales.tmpl` | complemento combinable | `*.tmp`, `*.bak`, `*.swp`, `*.log`, `*~`, `.DS_Store` |
| `.gitignore.mcp.tmpl` | complemento combinable | `.claude/`, `.codex/`, `.opencode/`, `.cursor/`, caches de agentes |

### Árbol de la biblioteca

```
templates/
└── gitignore/
    ├── .gitignore.raiz.tmpl
    ├── .gitignore.java.tmpl
    ├── .gitignore.python.tmpl
    ├── .gitignore.rust.tmpl
    ├── .gitignore.nodejs.tmpl
    ├── .gitignore.container.tmpl
    ├── .gitignore.secretos.tmpl
    ├── .gitignore.temporales.tmpl
    └── .gitignore.mcp.tmpl
```

tags: [opcional]

### Comando: Comandos

### Copiar el template de raíz

```bash
cp templates/gitignore/.gitignore.raiz.tmpl .gitignore
```

### Copiar template por ubicación y lenguaje

```bash
# Backend Java
cp templates/gitignore/.gitignore.java.tmpl source/backend/java/patos/.gitignore

# Backend Python
cp templates/gitignore/.gitignore.python.tmpl source/backend/python/servicio/.gitignore

# Backend Rust
cp templates/gitignore/.gitignore.rust.tmpl source/backend/rust/core/.gitignore

# Frontend Node.js
cp templates/gitignore/.gitignore.nodejs.tmpl source/frontend/nodejs/web/.gitignore

# Contenedores
cp templates/gitignore/.gitignore.container.tmpl containers/.gitignore
```

### Combinar complementos (el agente decide)

```bash
# En la raíz, combinar raíz + secretos
cat templates/gitignore/.gitignore.raiz.tmpl > .gitignore
cat templates/gitignore/.gitignore.secretos.tmpl >> .gitignore

# Combinar raíz + secretos + mcp
cat templates/gitignore/.gitignore.raiz.tmpl > .gitignore
cat templates/gitignore/.gitignore.secretos.tmpl >> .gitignore
cat templates/gitignore/.gitignore.mcp.tmpl >> .gitignore

# Temporales suelen ir en la raíz
cat templates/gitignore/.gitignore.temporales.tmpl >> .gitignore
```

tags: [opcional]

### Ejemplo: Ejemplos

### Proyecto multi-lenguaje (backend Java + frontend NodeJS)

```bash
# Raíz: transversal + secretos + mcp
cat templates/gitignore/.gitignore.raiz.tmpl > .gitignore
cat templates/gitignore/.gitignore.secretos.tmpl >> .gitignore
cat templates/gitignore/.gitignore.mcp.tmpl >> .gitignore

# Backend Java
cp templates/gitignore/.gitignore.java.tmpl source/backend/java/patos/.gitignore

# Frontend Node.js
cp templates/gitignore/.gitignore.nodejs.tmpl source/frontend/nodejs/web/.gitignore

# Contenedores
cp templates/gitignore/.gitignore.container.tmpl containers/.gitignore
```

### `.gitignore` raíz con Commitizen

```bash
cp templates/gitignore/.gitignore.raiz.tmpl .gitignore
# El template de raíz ya incluye:
#   .githooks/.tools/.commitizen-venv/

cat templates/gitignore/.gitignore.secretos.tmpl >> .gitignore
```

### Proyecto Python (solo backend)

```bash
cp templates/gitignore/.gitignore.raiz.tmpl .gitignore
cat templates/gitignore/.gitignore.secretos.tmpl >> .gitignore
cp templates/gitignore/.gitignore.python.tmpl source/backend/python/api/.gitignore
```

tags: [obligatorio]

### Restriccion: Restricciones

- **Todo repositorio debe tener un `.gitignore` en la raíz.** Es la primera línea de defensa para evitar que artefactos y secretos lleguen al repositorio.
- **Nunca versionar secretos ni credenciales:** `.env` (salvo `.env.example`), `*.pem`, `*.key`, `*.p12`, `*.jks`, carpetas `.aws/`, `.ssh/`, tokens. Si un secreto llega al historial de git, rotarlo inmediatamente.
- **Nunca versionar artefactos de build:** `target/`, `dist/`, `build/`, `node_modules/`, `__pycache__/`, `site/`.
- **Nunca versionar entornos virtuales:** `.venv/`, `venv/`, `env/`, `.githooks/.tools/.commitizen-venv/`.
- **El agente de IA elige qué templates aplicar** según el tipo de proyecto (backend Java, frontend NodeJS, etc.) y combina los complementos necesarios (secretos, temporales, MCP). No hay una combinación única para todos los proyectos.
- **Cada carpeta de proyecto (`source/<rol>/<lenguaje>/<proyecto>/`) debe tener su propio `.gitignore`** con las exclusiones de ese lenguaje además del `.gitignore` raíz.
- **La biblioteca `templates/gitignore/` es la fuente de referencia.** El placeholder `templates/repository-structure/.gitignore.tmpl` es mínimo; la biblioteca es la que contiene los patrones completos.
- **Los templates incluyen comentarios y opciones comentadas** para que el agente decida qué incluir según el framework o herramienta usada.

tags: [obligatorio]

### Referencia: Referencias

- [Regla 05: Control de Versiones](05-version-control_draft.md) — todo artefacto y secreto debe excluirse del versionado.
- [Regla 09: Estructura de Repositorio](09-repository-structure.md) — estructura `source/<rol>/<lenguaje>/<proyecto>/`.
- [Regla 11: Commitizen](11-commitizen.md) — `.githooks/.tools/.commitizen-venv/` debe ignorarse.
- [Regla 13: Gestión de Secretos](13-secrets.md) — `.secrets/*.enc.yaml` permitidos, `.env.*` ignorados.
- [templates/gitignore/](../templates/gitignore/) — biblioteca de templates de `.gitignore` por contexto.
- [templates/repository-structure/.gitignore.tmpl](../templates/repository-structure/.gitignore.tmpl) — placeholder del espejo.

tags: [obligatorio]

### Plantilla: Plantilla

- [templates/gitignore/.gitignore.raiz.tmpl](../templates/gitignore/.gitignore.raiz.tmpl)
- [templates/gitignore/.gitignore.java.tmpl](../templates/gitignore/.gitignore.java.tmpl)
- [templates/gitignore/.gitignore.python.tmpl](../templates/gitignore/.gitignore.python.tmpl)
- [templates/gitignore/.gitignore.rust.tmpl](../templates/gitignore/.gitignore.rust.tmpl)
- [templates/gitignore/.gitignore.nodejs.tmpl](../templates/gitignore/.gitignore.nodejs.tmpl)
- [templates/gitignore/.gitignore.container.tmpl](../templates/gitignore/.gitignore.container.tmpl)
- [templates/gitignore/.gitignore.secretos.tmpl](../templates/gitignore/.gitignore.secretos.tmpl)
- [templates/gitignore/.gitignore.temporales.tmpl](../templates/gitignore/.gitignore.temporales.tmpl)
- [templates/gitignore/.gitignore.mcp.tmpl](../templates/gitignore/.gitignore.mcp.tmpl)
- [templates/repository-structure/.gitignore.tmpl](../templates/repository-structure/.gitignore.tmpl) — placeholder

tags: [opcional]

---
id: build-tooling
title: Herramientas de Construcción
status: Definida
tags: [build, tooling, makefile, justfile, helpers, shell, python]
---

# Regla 01: Herramientas de Construcción

## Premisa

Todo proyecto debe tener un sistema de construcción declarativo y reproducible, independientemente del lenguaje. La responsabilidad es única en la capa de build: el `Makefile` orquesta objetivos y variables; la lógica específica vive en helpers reutilizables.

> **Nota:** esta regla describe el `Makefile` y `Justfile` de **proyectos consumidores** — los que un agente genera copiando las plantillas de [templates/](../templates/). El `Makefile` y `Justfile` en la raíz de este repositorio (`ether-my-best-practice`) son puramente operativos: publicar el sitio, validar reglas, lint y format.

## Estructura

```
.
├── Makefile
├── Justfile
└── helpers/
    ├── mk/
    │   ├── build.mk          # targets build, test, clean
    │   ├── container.mk      # targets runtime, image, ci
    │   ├── docs.mk           # targets docs, pages-build
    │   ├── github.mk         # target pages
    │   ├── lint.mk           # target lint
    │   ├── format.mk         # target format
    │   ├── java.mk
    │   ├── python.mk
    │   ├── javascript.mk
    │   └── rust.mk
    ├── just/
    │   ├── app.just
    │   ├── auth.just
    │   └── billing.just
    ├── shell/
    │   ├── build.sh
    │   ├── test.sh
    │   ├── clean.sh
    │   ├── container.sh
    │   ├── docs.sh
    │   ├── github.sh
    │   ├── lint.sh
    │   ├── format.sh
    │   ├── java.sh
    │   ├── python.sh
    │   ├── javascript.sh
    │   └── rust.sh
    └── python/
        └── *.py
```

**Flujo de delegación entre capas:**

```
Makefile ──→ helpers/mk/{dominio}.mk ──→ helpers/shell/{lenguaje}.sh / helpers/python/*.py
  │
  ├── Makefile recibe parámetros y define variables (LANG, BUILD_TOOL, MODULE, PROFILE).
  ├── helpers/mk/*.mk define los targets y los delega en helpers/shell o python.
  └── El helper shell o python ejecuta la herramienta nativa según flags (--tool, --goal).

Justfile ──→ helpers/just/*.just ──→ helpers/shell o python (operativas de aplicación)
  │        ──→ Makefile              (cuando necesita artefactos)
```

**Principio de capa única de ejecución:** los scripts en `helpers/shell/` son la fuente única de lógica ejecutable. Makefile y Justfile son fachadas finas que orquestan y delegan en los mismos helpers.

```
Justfile ──┐
            ├──> helpers/shell/{lenguaje}.sh  (capa compartida)
Makefile ──┘
```

## Nombres Sugeridos

### Archivos por lenguaje/demodule

- `helpers/mk/java.mk`, `python.mk`, `javascript.mk`, `rust.mk` — módulos make por lenguaje.
- `helpers/shell/java.sh`, `python.sh`, `javascript.sh`, `rust.sh` — scripts de build/test/serve por lenguaje.
- `helpers/shell/build.sh`, `test.sh`, `clean.sh`, `container.sh` — scripts genéricos.
- `helpers/shell/docs.sh`, `github.sh`, `lint.sh`, `format.sh` — scripts de infraestructura compartida.
- `helpers/just/app.just`, `auth.just`, `billing.just` — módulos just por dominio funcional.

### Variables estándar del Makefile

```
LANG       → java | python | javascript | rust
BUILD_TOOL → maven | gradle | uv | poetry | npm | pnpm | yarn | cargo
MODULE     → módulo/subproyecto (por defecto .)
PROFILE    → dev | ci | prod
SITE_DIR   → directorio de salida del sitio (por defecto site)
PAGES_WORKFLOW → static.yml
PAGES_REF      → main
```

### Targets Makefile y helpers

| Target | Módulo .mk | Helper |
|--------|-----------|--------|
| `build` | `helpers/mk/build.mk` | `helpers/shell/{lang}.sh --goal build` |
| `test` | `helpers/mk/build.mk` | `helpers/shell/{lang}.sh --goal test` |
| `clean` | `helpers/mk/build.mk` | `helpers/shell/{lang}.sh --goal clean` |
| `runtime` | `helpers/mk/container.mk` | `helpers/shell/container.sh --action runtime` |
| `image` | `helpers/mk/container.mk` | `helpers/shell/container.sh --action image` |
| `ci` | `helpers/mk/container.mk` | `helpers/shell/container.sh --action ci` |
| `docs` | `helpers/mk/docs.mk` | `helpers/shell/docs.sh --goal build` |
| `pages` | `helpers/mk/github.mk` | `helpers/shell/github.sh --action workflow-run` |
| `lint` | `helpers/mk/lint.mk` | `helpers/shell/lint.sh --tool {tool}` |
| `format` | `helpers/mk/format.mk` | `helpers/shell/format.sh --tool {tool}` |

### Operativas Justfile y helpers por lenguaje

| Goal | Java (`java.sh`) | JavaScript (`js.sh`) | Python (`python.sh`) | Rust |
|------|----------|--------------|--------------|------|
| `serve` | `mvn exec:java` / `gradle bootRun` | `npm run dev` / `pnpm dev` | `uv run uvicorn` / `flask run` | `cargo run` |
| `build` | `mvn package` / `gradle build` | `npm run build` / `pnpm build` | `uv build` / `poetry build` | `cargo build` |
| `test` | `mvn test` / `gradle test` | `npm test` / `pnpm test` | `uv run pytest` | `cargo test` |
| `lint` | `mvn checkstyle:check` | `npm run lint` / `pnpm lint` | `uv run ruff check` | `cargo clippy` |
| `format` | `mvn spotless:apply` | `npm run format` / `pnpm format` | `uv run ruff format` | `cargo fmt` |

## Comandos

### Build / Test / Clean (multi-lenguaje)

```bash
make build  LANG=java       BUILD_TOOL=maven  MODULE=api    PROFILE=dev
make test   LANG=python     BUILD_TOOL=uv     MODULE=service PROFILE=ci
make build  LANG=javascript BUILD_TOOL=pnpm   MODULE=web    PROFILE=dev
make test   LANG=rust       BUILD_TOOL=cargo   MODULE=core   PROFILE=ci
```

### CI en contenedor

```bash
make image LANG=java BUILD_TOOL=maven
make ci    LANG=java BUILD_TOOL=maven
```

### Documentación y publicación

```bash
make docs
make pages-build      # Validar + generar sitio
make pages            # Disparar workflow de GitHub Pages
```

### Calidad

```bash
make lint
make format
```

### Inclusión modular (Makefile)

```make
MK_FILES ?= $(wildcard helpers/mk/*.mk)
-include $(MK_FILES)
```

### Ejecución de helpers con flags

```bash
bash helpers/shell/java.sh       --tool maven  --goal build --module api --log-file /var/log/proyecto/log-java-20260807T120000Z.log
bash helpers/shell/javascript.sh --tool pnpm   --goal test  --module web --log-file /tmp/proyecto/log-javascript-20260807T120000Z.log
bash helpers/shell/python.sh     --tool uv     --goal serve --port 8000 --log-file /var/log/proyecto/log-python-20260807T120000Z.log
bash helpers/shell/rust.sh       --tool cargo  --goal run   --release    --log-file /tmp/proyecto/log-rust-20260807T120000Z.log
bash helpers/shell/github.sh     --action workflow-run --workflow static.yml --ref main --log-file /tmp/proyecto/log-github-20260807T120000Z.log
```

## Ejemplos

### Makefile (plantilla consumidora)

```make
.PHONY: help build test clean runtime image ci

LANG ?= java
BUILD_TOOL ?= maven
MODULE ?= .
PROFILE ?= dev
SITE_DIR ?= site
MK_FILES ?= $(wildcard helpers/mk/*.mk)

-include $(MK_FILES)

help:
	@echo "Tareas disponibles: make build, make test, make clean, make docs, make ci, ..."
```

### Justfile (operativas de aplicación)

```bash
just serve LANG=java BUILD_TOOL=maven
  → Justfile detecta LANG=java
  → bash helpers/shell/java.sh --tool maven --goal serve --port 8080
  → java.sh resuelve: mvn exec:java
```

### Flujo operativo (Justfile → Makefile)

```text
just create-user --username alice --email alice@example.com
  → helpers/just/app.just:create-user
    → helpers/shell/app.bash o helpers/python/app.py
      → ejecuta jar / npm run / binario generado por CI
```

### Build en contenedor

```bash
make image LANG=java BUILD_TOOL=maven  # Construye imagen de CI (Dockerfile.ci)
make ci    LANG=java BUILD_TOOL=maven  # Ejecuta build+test dentro del contenedor
```

### Auditoría de helpers (logging obligatorio)

Política de ruta:
1. `/var/log/<nombre-proyecto>/log-<script>-<timestamp>.log`
2. Fallback: `/tmp/<nombre-proyecto>/log-<script>-<timestamp>.log`

## Restricciones

### Prohibiciones absolutas

- **El `Makefile` nunca ejecuta comandos directos** de build, docs, lint ni format. Prohibido: `mkdocs build`, `uv run python`, `npm run`, `mvn`, `cargo` en el cuerpo del Makefile. Todo target debe delegar: `Makefile → helpers/mk/*.mk → helpers/shell/*.sh` o `helpers/python/*.py`.
- **`Makefile → Justfile` está prohibido.** La capa de build/artefactos pertenece a Makefile; la capa de tareas operativas pertenece a Justfile.
- **`Justfile → Makefile` está permitido** (cuando una operativa necesite artefactos generados por el build).
- **`Justfile → helpers/just → shell/python/binarios` está permitido.**
- **Nunca usar parámetros posicionales ambiguos** en helpers. Siempre flags explícitos (`--flag valor`).
- **Nunca ejecutar un helper sin auditoría.** Flujo obligatorio de logs: `/var/log/<proyecto>` → fallback `/tmp/<proyecto>`.

### Contrato de flags obligatorio para helpers

| Flag | Obligatorio | Descripción |
|------|-------------|-------------|
| `--action` o `--goal` | Sí | Operación a ejecutar |
| `--tool` | No (según helper) | Herramienta de construcción |
| `--log-file` | Sí | Ruta del log de auditoría |
| `--log-level` | No | Nivel de log (info por defecto) |
| `--command` | No | Comando directo (sobreescribe goal) |

### Estándares de implementación

- Shell helpers: `sh` o `bash`. Recomendado `bash` para parsing de flags o validaciones ricas.
- Python helpers: Python 3.11+ con dependencias gestionadas por `uv`. Ubicación: `helpers/python/`.
- Construcción en contenedor preferida: detectar `podman` → `docker`; fallar si ninguno disponible.

### Artefactos por lenguaje (rutas a limpiar y versionar)

- Java: `target/*.class`, `target/*.jar`
- Python: `dist/*`, `build/*`, `*.pyc`
- JavaScript: `dist/*`, `build/*`
- Rust: `target/release/*`

## Referencias

- [Regla 06: CI/CD](06-ci-cd.md)
- [templates/Makefile.tmpl](../templates/Makefile.tmpl)
- [templates/Justfile.tmpl](../templates/Justfile.tmpl)
- [templates/helpers/shell/](../templates/helpers/shell/): `build.sh`, `test.sh`, `clean.sh`, `container.sh`, `docs.sh`, `github.sh`, `lint.sh`, `format.sh`, `java.sh`, `javascript.sh`, `python.sh`, `rust.sh`
- [templates/helpers/mk/](../templates/helpers/mk/): `build.mk`, `container.mk`, `docs.mk`, `github.mk`, `lint.mk`, `format.mk`
- [templates/helpers/just/app.just.tmpl](../templates/helpers/just/app.just.tmpl)

## Plantilla

- [templates/Makefile.tmpl](../templates/Makefile.tmpl)
- [templates/Justfile.tmpl](../templates/Justfile.tmpl)
- [templates/helpers/mk/build.mk.tmpl](../templates/helpers/mk/build.mk.tmpl)
- [templates/helpers/mk/container.mk.tmpl](../templates/helpers/mk/container.mk.tmpl)
- [templates/helpers/mk/docs.mk.tmpl](../templates/helpers/mk/docs.mk.tmpl)
- [templates/helpers/mk/github.mk.tmpl](../templates/helpers/mk/github.mk.tmpl)
- [templates/helpers/mk/lint.mk.tmpl](../templates/helpers/mk/lint.mk.tmpl)
- [templates/helpers/mk/format.mk.tmpl](../templates/helpers/mk/format.mk.tmpl)
- [templates/helpers/just/app.just.tmpl](../templates/helpers/just/app.just.tmpl)

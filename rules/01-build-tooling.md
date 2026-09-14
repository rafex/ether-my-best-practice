---
id: build-tooling
title: Herramientas de Construcción
status: Definida
tags: [build, tooling, makefile, justfile, helpers, shell, python]
checksum: 921cf66f9d1bde0a52dd368fa8c6f5eba73332f88132baf1b19ceaf80d2bee60
---

# Regla 01: Herramientas de Construcción



### Premisa: Premisa

Todo proyecto debe tener un sistema de construcción declarativo y reproducible, independientemente del lenguaje. La responsabilidad se separa en tres capas: **Makefile** (construcción, artefactos, derivados de compilación), **Justfile** (task manager — orquesta acciones que pueden envolver `make` + operativa del binario, y tareas de día a día), y **helpers** (scripts que contienen la lógica real). Makefile y Justfile tienen lógica casi 0: solo proveen variables y orquestan llamadas. El script es el que realmente ejecuta.

> **Nota:** esta regla describe el `Makefile` y `Justfile` de **proyectos consumidores** — los que un agente genera copiando las plantillas de [templates/](https://github.com/rafex/ether-my-best-practice/blob/main/templates/). El `Makefile` y `Justfile` en la raíz de este repositorio (`ether-my-best-practice`) son puramente operativos: publicar el sitio, validar reglas, lint y format.

tags: [obligatorio]

### Estructura: Estructura

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
    │   ├── help.mk           # target man (manual de tareas)
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
    │   ├── man.sh             # muestra docs/man_<tarea>.md
    │   ├── java.sh
    │   ├── python.sh
    │   ├── javascript.sh
    │   └── rust.sh
    └── python/
        └── *.py
```

**Manuales de tareas:** cada target de Makefile, receta de Justfile o `--goal`/`--action` de un helper tiene su manual en `docs/man_<tarea>.md` (Markdown, formato tipo `man`). Viven siempre en `docs/`, nunca en `helpers/` — ver "Manual de tareas (`--man`)" en Comandos y Restricciones.

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

tags: [opcional]

### Nombre Sugerido: Nombres Sugeridos

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
TARGET         → nombre del target a documentar (uso: make man TARGET=build)
```

### Targets Makefile y helpers

| Target | Módulo .mk | Helper |
|--------|-----------|--------|
| `build` | `helpers/mk/build.mk` | `helpers/shell/{lang}.sh --goal build` |
| `test` | `helpers/mk/build.mk` | `helpers/shell/{lang}.sh --goal test` |
| `clean` | `helpers/mk/build.mk` | `helpers/shell/{lang}.sh --goal clean` |
| `man` | `helpers/mk/help.mk` | `helpers/shell/man.sh --target $(TARGET)` |
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

tags: [opcional]

### Comando: Comandos

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

### Manual de tareas (`--man`)

```bash
make man TARGET=build                            # Muestra docs/man_build.md (Makefile no reenvía flags a un target)
just commit-msg --man                             # Justfile sí reenvía flags: la receta pasa --man al helper
bash helpers/shell/build.sh --command "x" --man   # Uso directo del helper: --man corta antes de ejecutar
bash helpers/shell/man.sh --target lint           # Uso directo del helper dedicado de manuales
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

tags: [opcional]

### Ejemplo: Ejemplos

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
make image LANG=java BUILD_TOOL=maven  # Construye imagen de CI (Containerfile.ci)
make ci    LANG=java BUILD_TOOL=maven  # Ejecuta build+test dentro del contenedor
```

### Auditoría de helpers (logging obligatorio)

Política de ruta:
1. `/var/log/<nombre-proyecto>/log-<script>-<timestamp>.log`
2. Fallback: `/tmp/<nombre-proyecto>/log-<script>-<timestamp>.log`

### Manual de una tarea (`docs/man_build.md`)

```markdown
# build

## Nombre
build — compila el proyecto y genera artefactos

## Sinopsis
make build LANG=<lang> BUILD_TOOL=<tool> MODULE=<module> PROFILE=<profile>
just build --man

## Descripción
Delega en `helpers/shell/{lang}.sh --goal build`, que resuelve el comando
nativo (`mvn package`, `npm run build`, `cargo build`, ...) según `--tool`.

## Opciones
- LANG        java | python | javascript | rust
- BUILD_TOOL  maven | gradle | uv | poetry | npm | pnpm | yarn | cargo
- MODULE      módulo/subproyecto (por defecto .)
- PROFILE     dev | ci | prod

## Ejemplos
make build LANG=java BUILD_TOOL=maven MODULE=api PROFILE=dev
```

### `show_man` reutilizado por Makefile, Justfile y el helper directo

```bash
# helpers/shell/man.sh (invocado por `make man TARGET=build`)
show_man "$target"

# helpers/shell/build.sh (invocado por `just build --man` o directamente)
if [[ "$man" == "true" ]]; then
  show_man "build"
  exit 0
fi
```

tags: [obligatorio]

### Restriccion: Restricciones

### Prohibiciones absolutas

- **El `Makefile` nunca ejecuta comandos directos** de build, docs, lint ni format. Prohibido: `mkdocs build`, `uv run python`, `npm run`, `mvn`, `cargo` en el cuerpo del Makefile. Todo target debe delegar: `Makefile → helpers/mk/*.mk → helpers/shell/*.sh` o `helpers/python/*.py`.
- **`Makefile → Justfile` está prohibido.** La capa de build/artefactos pertenece a Makefile; la capa de tareas operativas pertenece a Justfile.
- **`Justfile → Makefile` está permitido** (cuando una operativa necesite artefactos generados por el build).
- **`Justfile → helpers/just → shell/python/binarios` está permitido.**
- **Justfile no debe ser un proxy pass de Makefile.** Recetas que solo delegan en `make` sin composición ni parámetros (`@validate: make validate`) son un antipatrón. Justfile existe para orquestar: componer varios pasos o capturar parámetros del usuario y pasarlos a scripts.
- **Makefile y Justfile tienen lógica casi 0.** Solo proveen variables y orquestan llamadas. La lógica real vive en helpers (`shell` o `python`).
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
| `--man` | Sí | Muestra `docs/man_<tarea>.md` y termina (exit 0) sin ejecutar `--action`/`--goal`/`--command` |

### Manual obligatorio por tarea (`--man`)

- **Todo target de Makefile, receta de Justfile y helper nuevo debe exponer su manual.** En Makefile, vía el target genérico `make man TARGET=<target>` (Make no reenvía flags a un target, así que `--man` no es viable ahí). En Justfile y en los helpers, vía el flag `--man`, porque `just` sí reenvía argumentos a la receta y esta los reenvía al helper.
- **El manual vive en `docs/man_<tarea>.md`, nunca en `helpers/`.** `<tarea>` coincide con el nombre del target de Makefile, la receta de Justfile o el valor de `--goal`/`--action` del helper. Ejemplo: el target `build` documenta en `docs/man_build.md`.
- **El helper nunca embebe el texto del manual en el propio script** (nada de heredocs largos ni bloques de `echo` con la ayuda completa). Siempre lee y muestra el archivo Markdown de `docs/` — la fuente de verdad es un único archivo reutilizado por `--man`, por `make man` y por cualquier otro consumidor (por ejemplo MkDocs).
- **Si `docs/man_<tarea>.md` no existe, el helper falla explícitamente** indicando la ruta esperada. No debe fallar en silencio ni inventar contenido.
- La visualización (`show_man`) es una función compartida en `lib/` (regla 15), no lógica duplicada en cada helper.

### Estándares de implementación

- Shell helpers: `sh` o `bash`. Recomendado `bash` para parsing de flags o validaciones ricas.
- Python helpers: Python 3.12+ con dependencias gestionadas por `uv`. Ubicación: `helpers/python/`.
- Construcción en contenedor preferida: detectar `podman` → `docker`; fallar si ninguno disponible.

### Artefactos por lenguaje (rutas a limpiar y versionar)

- Java: `target/*.class`, `target/*.jar`
- Python: `dist/*`, `build/*`, `*.pyc`
- JavaScript: `dist/*`, `build/*`
- Rust: `target/release/*`

tags: [obligatorio]

### Referencia: Referencias

- [Regla 06: CI](06-ci.md)
- [Regla 08: Stack Tecnológico](08-stack.md)
- [templates/Makefile.tmpl](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/Makefile.tmpl)
- [templates/Justfile.tmpl](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/Justfile.tmpl)
- [templates/helpers/shell/](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/helpers/shell/): `build.sh`, `test.sh`, `clean.sh`, `container.sh`, `docs.sh`, `github.sh`, `lint.sh`, `format.sh`, `man.sh`, `java.sh`, `javascript.sh`, `python.sh`, `rust.sh`
- [templates/helpers/mk/](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/helpers/mk/): `build.mk`, `container.mk`, `docs.mk`, `github.mk`, `help.mk`, `lint.mk`, `format.mk`
- [templates/helpers/just/app.just.tmpl](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/helpers/just/app.just.tmpl)
- [templates/repository-structure/docs/man_build.md.tmpl](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/docs/man_build.md.tmpl) — ejemplo de manual de tarea.

- [Regla 15: Reutilización de Scripts](15-script-reuse.md) — librerías comunes en lib/.

tags: [obligatorio]

### Plantilla: Plantilla

- [templates/Makefile.tmpl](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/Makefile.tmpl)
- [templates/Justfile.tmpl](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/Justfile.tmpl)
- [templates/helpers/mk/build.mk.tmpl](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/helpers/mk/build.mk.tmpl)
- [templates/helpers/mk/container.mk.tmpl](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/helpers/mk/container.mk.tmpl)
- [templates/helpers/mk/docs.mk.tmpl](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/helpers/mk/docs.mk.tmpl)
- [templates/helpers/mk/github.mk.tmpl](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/helpers/mk/github.mk.tmpl)
- [templates/helpers/mk/help.mk.tmpl](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/helpers/mk/help.mk.tmpl)
- [templates/helpers/mk/lint.mk.tmpl](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/helpers/mk/lint.mk.tmpl)
- [templates/helpers/mk/format.mk.tmpl](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/helpers/mk/format.mk.tmpl)
- [templates/helpers/shell/man.sh.tmpl](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/helpers/shell/man.sh.tmpl)
- [templates/helpers/just/app.just.tmpl](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/helpers/just/app.just.tmpl)
- [templates/repository-structure/docs/man_build.md.tmpl](https://github.com/rafex/ether-my-best-practice/blob/main/templates/repository-structure/docs/man_build.md.tmpl)

tags: [opcional]

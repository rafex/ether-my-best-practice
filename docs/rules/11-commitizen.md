---
id: commitizen
title: Commitizen — Commit Convencional y Release
status: Definida
tags: [commitizen, conventional-commits, release, changelog, versioning]
checksum: c7905ba1841d34e6c3fef64d8c13ca57211ebad2ea113646faa8308ed7e991b2
---

# Regla 11: Commitizen — Commit Convencional y Release



### Premisa: Premisa

Commitizen (`cz`) es la herramienta estándar para asistir la creación de commits convencionales y gestionar el release (bump de versión, changelog, tag). Se instala en un entorno virtual interno no trackeable (`.githooks/.tools/.commitizen-venv`) y se accede exclusivamente mediante recetas `just` (nunca `cz` directo). El wrapper `cz.sh` centraliza la lógica de bootstrap y ejecución.

> **Co-propiedad con [Regla 10: Git Hooks](10-githooks.md):** la regla 10 define los gates (lint/test/commit-msg); esta regla define la herramienta que los respalda — el asistente de commit convencional, la generación de changelog y el bump de versión. Ambas son **co-propietarias** del objetivo: commit + release gestionado.

tags: [obligatorio]

### Estructura: Estructura

### Componentes del sistema

```
proyecto/
├── .config/commitizen/                  # configuración de Commitizen (regla 14)
│       └── pyproject.toml                         # [tool.commitizen] configuración
├── CHANGELOG.md                            # generado por cz bump/changelog
├── VERSION                                 # gestionado por cz vía version_files
│
├── .githooks/
│   └── .tools/
│       ├── .gitkeep                        # estructura versionable
│       └── .commitizen-venv/               # NO trackeado (.gitignore)
│           └── bin/cz                      # ejecutable de Commitizen
│
├── helpers/
│   └── shell/
│       └── cz.sh                           # wrapper (bootstrap, commit, changelog, version, bump, init)
│
└── Justfile                                # recipes: just commit, just changelog, just version, ...
```

### Flujo de operación

```
just commit        → cz.sh --action commit   → .venv/bin/cz commit  (interactivo)
just changelog     → cz.sh --action changelog → .venv/bin/cz changelog
just version       → cz.sh --action version  → .venv/bin/cz version
just prepare-release → cz.sh --action bump   → .venv/bin/cz bump   (version+changelog+tag+commit)
just cz-init       → cz.sh --action init     → .venv/bin/cz init   (config interactivo)
just hooks-install → hooks.sh install        → cz.sh bootstrap     (crea .venv + instala commitizen)
```

### Configuración en pyproject.toml

```toml
[tool.commitizen]
name = "cz_conventional_commits"
version = "0.1.0"
version_provider = "commitizen"
version_scheme = "pep440"
tag_format = "v$version"
version_files = [
    "pyproject.toml:version",
    "VERSION",
    "Cargo.toml:version",
    "package.json:version",
]
update_changelog_on_bump = true
changelog_file = "CHANGELOG.md"
bump_message = "chore(release): v$new_version"
```

tags: [opcional]

### Comando: Comandos

### Instalación (bootstrap del venv)

```bash
just hooks-install
# → hooks.sh --action install → git config core.hooksPath .githooks
# → cz.sh --action bootstrap → uv venv / python3 -m venv + pip install commitizen
```

### Asistente de commit

```bash
just commit
# → cz commit (interactivo: selecciona tipo, scope, escribe mensaje)
```

### Generar changelog

```bash
just changelog
# → cz changelog
```

### Leer/bumpear versión

```bash
just version                    # leer versión actual
just version --bump minor       # bumpear a siguiente minor
```

### Release completo

```bash
just prepare-release
# → cz bump: bumpea versión + genera CHANGELOG.md + crea tag + commit "chore(release): vX.Y.Z"
```

### Configuración inicial (para agentes de IA)

```bash
just cz-init
# → cz init (interactivo — solo para humanos)
```

Para agentes de IA: **no usar `cz init`.** En su lugar, editar directamente `pyproject.toml` con la sección `[tool.commitizen]` usando `templates/pyproject.toml.tmpl` como base, ajustando `version_files` según los lenguajes del proyecto (Java → solo VERSION + pyproject.toml; Rust → + Cargo.toml; Node → + package.json).

### Bootstrap manual del venv (sin hooks)

```bash
bash helpers/shell/cz.sh --action bootstrap
```

tags: [opcional]

### Ejemplo: Ejemplos

### Flujo típico de un release

```bash
$ just version
1.2.0

$ just changelog
# Genera entradas en CHANGELOG.md desde el último tag

$ just prepare-release
# Bumpea a 1.3.0, actualiza CHANGELOG.md, crea tag v1.3.0,
# commit "chore(release): v1.3.0" y push
```

### Instalación en un proyecto nuevo

```bash
$ just hooks-install
Git hooks instalados: core.hooksPath = .githooks
Bootstrapping Commitizen venv in .githooks/.tools/.commitizen-venv...
Commitizen instalado en .githooks/.tools/.commitizen-venv

$ just commit
# Asistente interactivo: feat(auth): add JWT validation
```

### pyproject.toml mínimo para un backend Java

```toml
[tool.commitizen]
name = "cz_conventional_commits"
version = "0.1.0"
version_provider = "commitizen"
version_files = ["pyproject.toml:version", "../../VERSION"]
tag_format = "v$version"
update_changelog_on_bump = true
changelog_file = "../../CHANGELOG.md"
bump_message = "chore(release): v$new_version"
```

### Fallback: si Commitizen no está disponible

El `cz.sh` intenta hacer bootstrap automático. Si falla y existe el fallback, se pueden usar los helpers `changelog.py`/`version.py` directamente:

```bash
just version          # vía cz.sh → Commitizen
# fallback:
uv run python helpers/python/version.py
uv run python helpers/python/changelog.py
```

tags: [obligatorio]

### Restriccion: Restricciones

- **`cz` nunca se ejecuta directamente.** Toda interacción con Commitizen es mediante `just` y `cz.sh` (wrapper). Esto garantiza que el venv esté bootstrapeado y la auditoría funcione.
- **El venv `.githooks/.tools/.commitizen-venv/` no se versiona nunca.** Está en `.gitignore`. El bootstrap lo recrea en cualquier máquina.
- **`just commit` es interactivo.** No debe ser invocado por scripts de CI (el CI usa commits automáticos que deben pasar el hook `commit-msg` de validación).
- **`just prepare-release` ejecuta `cz bump`**, que bumpea la versión, actualiza `CHANGELOG.md`, crea el tag y commitea con `chore(release)`.
- **Los agentes de IA no deben ejecutar `just cz-init`** (es interactivo). Deben editar `pyproject.toml` directamente con la sección `[tool.commitizen]`.
- **El bootstrap usa `uv` si está disponible** (regla 08); si no, fallback `python3 -m venv`.
- **`cz bump` determina la versión automáticamente** desde los commits desde el último tag. Si se necesita una versión explícita, usar `just version --bump <part>` o editar `pyproject.toml:version` y usar `just changelog`.

tags: [obligatorio]

### Referencia: Referencias

- [Regla 10: Git Hooks](10-githooks.md) — **co-propietaria** del objetivo commit+release. Define los gates; esta regla define la herramienta.
- [Regla 01: Build Tooling](01-build-tooling.md) — helpers como capa única de ejecución (cz.sh).
- [Regla 05: Control de Versiones](05-version-control_draft.md) — Conventional Commits.
- [Regla 08: Stack Tecnológico](08-stack.md) — Python 3.12+, uv.
- [Commitizen Documentation](https://commitizen-tools.github.io/commitizen/)
- [templates/repository-structure/.config/commitizen/pyproject.toml.tmpl](../templates/repository-structure/.config/commitizen/pyproject.toml.tmpl) — configuración base.
- [templates/helpers/shell/cz.sh.tmpl](../templates/repository-structure/helpers/shell/cz.sh.tmpl) — wrapper.
- [templates/gitignore/.gitignore.raiz.tmpl](../templates/gitignore/.gitignore.raiz.tmpl) — incluye `.githooks/.tools/.commitizen-venv/`.
- [templates/repository-structure/.gitignore.tmpl](../templates/repository-structure/.gitignore.tmpl) — placeholder del espejo.

tags: [obligatorio]

### Plantilla: Plantilla

- [templates/repository-structure/.config/commitizen/pyproject.toml.tmpl](../templates/repository-structure/.config/commitizen/pyproject.toml.tmpl)
- [templates/helpers/shell/cz.sh.tmpl](../templates/repository-structure/helpers/shell/cz.sh.tmpl)
- [templates/gitignore/.gitignore.raiz.tmpl](../templates/gitignore/.gitignore.raiz.tmpl)
- [templates/repository-structure/.gitignore.tmpl](../templates/repository-structure/.gitignore.tmpl) — placeholder

tags: [opcional]

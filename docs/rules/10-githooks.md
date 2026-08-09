---
id: githooks
title: Git Hooks
status: Definida
tags: [git, hooks, pre-commit, pre-push, commit-msg, release, conventional-commits]
---

# Regla 10: Git Hooks

## Premisa

Todo proyecto debe tener gates locales de calidad mediante git hooks. Los hooks son **gates puros** (sin efectos laterales). **Cada hook tiene su propio script** (`pre-commit.sh`, `pre-push.sh`, `commit-msg.sh`) para máxima reutilización. Los dispatchers `.githooks/*` llaman a **Makefile o Justfile** según la naturaleza del gate, nunca a scripts directamente:
- `pre-commit` y `pre-push` → **gates de calidad/construcción → Makefile** (vía `.mk` que delega en el script).
- `commit-msg` → **operativa de mantenimiento → Justfile** (vía receta que delega en el script).
`hooks.sh` queda solo para `install` (bootstrap + `core.hooksPath`).

> **Co-propiedad con [Regla 11: Commitizen](11-commitizen.md):** esta regla define los gates (pre-commit, pre-push, commit-msg); la regla 11 define la herramienta que los respalda — Commitizen como asistente de commit convencional, generador de changelog y gestor de versiones. Ambas son **co-propietarias** del objetivo: commit + release gestionado.

## Estructura

### Árbol de hooks

```
proyecto/
├── .githooks/                       # git hooks (fuente única, no se copian)
│   ├── pre-commit                   # → make pre-commit
│   ├── pre-push                     # → make pre-push
│   └── commit-msg                   # → just commit-msg
│
├── helpers/
│   ├── mk/
│   │   ├── pre-commit.mk            # gate de calidad: lint + validate + secrets
│   │   └── pre-push.mk              # gate de test: test + ci
│   ├── shell/
│   │   ├── hooks.sh                 # solo install (bootstrap + core.hooksPath)
│   │   ├── pre-commit.sh            # orquesta: lint + validate + secrets-verify
│   │   ├── pre-push.sh              # orquesta: test + trufflehog
│   │   └── commit-msg.sh            # valida Conventional Commits
│   └── just/
│       └── hooks.just               # recipe @commit-msg → commit-msg.sh
│
├── VERSION                          # versión actual (bumpeada en prepare-release)
├── CHANGELOG.md                     # generado en prepare-release
└── Justfile                         # importa hooks.just
```

### Flujo de delegación

```
git commit  → .githooks/pre-commit  → make pre-commit  → pre-commit.mk  → pre-commit.sh  → orquesta scripts atómicos (lint + validate + secrets)
git push    → .githooks/pre-push    → make pre-push    → pre-push.mk    → pre-push.sh    → orquesta scripts atómicos (test + secrets)
git commit  → .githooks/commit-msg  → just commit-msg  → hooks.just     → commit-msg.sh  → valida Conventional Commits
```

Los dispatchers en `.githooks/` son scripts de 1 línea que **solo** invocan `make <target>` o `just <receta>`, **nunca** scripts directamente. La lógica de cada gate vive en su propio script (`pre-commit.sh`, `pre-push.sh`, `commit-msg.sh`), reutilizando scripts atómicos (`lint.sh`, `validate-rules.sh`, `secrets.sh verify`, `test.sh`).

### Instalación

```bash
just hooks-install
# → bash helpers/shell/hooks.sh --action install
# → git config core.hooksPath .githooks
```

No se copian ni symlinkean hooks a `.git/hooks/`. La configuración `core.hooksPath` apunta directamente a `.githooks/` (git 2.9+), manteniendo el repositorio como fuente única de verdad.

## Nombres Sugeridos

- Carpeta: `.githooks/` (oculta, en raíz del repositorio).
- Hooks: `pre-commit`, `pre-push`, `commit-msg` — nombres estándar de git.
- Helpers: `hooks.sh` (solo install), `pre-commit.sh`, `pre-push.sh`, `commit-msg.sh` — **un script por hook** (máxima reutilización).
- Módulos make: `pre-commit.mk` (gates de calidad), `pre-push.mk` (gates de test/ci).
- Módulos just: `hooks.just` (recipe `commit-msg`).
- Recipes Justfile: `hooks-install`, `prepare-release`, `version`, `changelog`.

## Comandos

### Instalación de hooks

```bash
just hooks-install              # git config core.hooksPath .githooks
```

### Lectura y bump de VERSION

```bash
uv run python helpers/python/version.py              # leer versión actual
uv run python helpers/python/version.py --bump patch
uv run python helpers/python/version.py --bump minor
uv run python helpers/python/version.py --bump major
uv run python helpers/python/version.py --version 1.2.0
```

### Generación de CHANGELOG

```bash
uv run python helpers/python/changelog.py
```

### Release completo

```bash
just prepare-release 1.2.0
# → version.py --version 1.2.0  (escribe VERSION)
# → changelog.py                 (escribe CHANGELOG.md desde git log)
# → git add VERSION CHANGELOG.md
# → git commit -m "chore(release): v1.2.0"
# → git tag -a v1.2.0 -m "Release v1.2.0"
# → git push origin v1.2.0
```

### Gates manuales (idéntico a lo que ejecutan los hooks)

```bash
make pre-commit      # → pre-commit.mk → pre-commit.sh → lint + validate + secrets
make pre-push        # → pre-push.mk → pre-push.sh → test + secrets
just commit-msg      # → hooks.just → commit-msg.sh
```

## Ejemplos

### Dispatcher pre-commit

```bash
#!/usr/bin/env bash
make pre-commit
```

### Dispatcher pre-push

```bash
#!/usr/bin/env bash
make pre-push
```

### Dispatcher commit-msg

```bash
#!/usr/bin/env bash
just commit-msg "$1"
```

### pre-commit.sh (orquesta scripts atómicos)

```bash
#!/usr/bin/env bash
# Orquesta los gates de calidad del pre-commit.
# Llamado por make pre-commit → pre-commit.mk.
bash helpers/shell/lint.sh || exit 1
bash helpers/shell/validate-rules.sh || exit 1
if command -v gitleaks >/dev/null 2>&1; then gitleaks git --staged; fi
```

### hooks.sh (solo install)

### commit-msg validación

```text
$ git commit -m "update stuff"
ERROR: el mensaje de commit no sigue Conventional Commits.
Formato esperado: tipo[(scope)][!]: descripción
Tipos válidos:    feat, fix, docs, style, refactor, test, chore, build, ci, perf, revert

$ git commit -m "feat(auth): add JWT validation"
[main abc1234] feat(auth): add JWT validation
```

### Flujo release completo

```bash
$ just prepare-release 1.2.0
VERSION updated: 1.2.0
CHANGELOG.md generated (version 1.2.0, changes since v1.1.0)
[main def5678] chore(release): v1.2.0
# ... tag creado y pusheado
```

## Restricciones

- **Los hooks NO rellenan CHANGELOG.md ni VERSION.** Hacerlo en pre-commit o post-commit produce worktree sucio, conflictos de merge y ruido en cada rama.
- **CHANGELOG.md y VERSION se generan exclusivamente en release-time** con `just prepare-release`, llamando a `helpers/python/changelog.py` y `version.py`.
- **Los hooks son gates puros:** lint/test/validation, sin efectos laterales. Si un hook escribe archivos, está mal diseñado.
- **No copiar hooks a `.git/hooks/`** ni usar symlinks. Usar `git config core.hooksPath .githooks` (fuente única de verdad).
- **Los dispatchers en `.githooks/` llaman a `make <target>` o `just <receta>`, nunca a scripts directamente.** La lógica vive en un script por hook (`pre-commit.sh`, `pre-push.sh`, `commit-msg.sh`) que orquesta scripts atómicos.
- **commit-msg valida Conventional Commits alineado con [Regla 05](05-version-control.md).** Merge commits y initial commit se ignoran.
- **Los hooks nunca deben tener dependencias externas** que no estén disponibles en el entorno de desarrollo (solo bash, git, y los helpers del proyecto).
- **Los hooks no deben romper el flujo de desarrollo.** Si un gate falla, debe mostrar un mensaje claro de qué corregir y cómo.

## Referencias

- [Regla 01: Build Tooling](01-build-tooling.md) — `make lint`, `make test`, capa de helpers.
- [Regla 05: Control de Versiones](05-version-control.md) — Conventional Commits.
- [Regla 06: CI](06-ci.md) — pipeline local como complemento a los hooks.
- [Regla 09: Estructura de Repositorio](09-repository-structure.md) — `.githooks/` en el árbol del proyecto.
- [Regla 11: Commitizen](11-commitizen.md) — asistente de commit + release (co-propietaria del objetivo).
- [Regla 13: Gestión de Secretos](13-secrets.md) — gitleaks (pre-commit) + trufflehog (pre-push).
- [templates/repository-structure/.githooks/](../templates/repository-structure/.githooks/) — dispatchers pre-commit, pre-push, commit-msg.
- [templates/helpers/shell/hooks.sh.tmpl](../templates/repository-structure/helpers/shell/hooks.sh.tmpl)
- [templates/helpers/shell/commit-msg.sh.tmpl](../templates/repository-structure/helpers/shell/commit-msg.sh.tmpl)
- [templates/helpers/python/changelog.py.tmpl](../templates/repository-structure/helpers/python/changelog.py.tmpl)
- [templates/helpers/python/version.py.tmpl](../templates/repository-structure/helpers/python/version.py.tmpl)

## Plantilla

- [templates/repository-structure/.githooks/](../templates/repository-structure/.githooks/)
- [templates/helpers/shell/hooks.sh.tmpl](../templates/repository-structure/helpers/shell/hooks.sh.tmpl)
- [templates/helpers/shell/commit-msg.sh.tmpl](../templates/repository-structure/helpers/shell/commit-msg.sh.tmpl)
- [templates/helpers/python/changelog.py.tmpl](../templates/repository-structure/helpers/python/changelog.py.tmpl)
- [templates/helpers/python/version.py.tmpl](../templates/repository-structure/helpers/python/version.py.tmpl)

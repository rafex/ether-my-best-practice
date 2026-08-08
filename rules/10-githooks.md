---
id: githooks
title: Git Hooks
status: Definida
tags: [git, hooks, pre-commit, pre-push, commit-msg, release, conventional-commits]
---

# Regla 10: Git Hooks

## Premisa

Todo proyecto debe tener gates locales de calidad mediante git hooks que reutilicen la capa única de ejecución de `helpers/`. Los hooks son **gates puros** (sin efectos laterales): lint antes de commit y test antes de push. El `CHANGELOG.md` y el archivo `VERSION` se generan exclusivamente en release (`just prepare-release`), nunca en hooks.

> **Co-propiedad con [Regla 11: Commitizen](11-commitizen.md):** esta regla define los gates (pre-commit, pre-push, commit-msg); la regla 11 define la herramienta que los respalda — Commitizen como asistente de commit convencional, generador de changelog y gestor de versiones. Ambas son **co-propietarias** del objetivo: commit + release gestionado.

## Estructura

### Árbol de hooks

```
proyecto/
├── .githooks/                       # git hooks (fuente única, no se copian)
│   ├── pre-commit                   # → hooks.sh --action pre-commit (lint)
│   ├── pre-push                     # → hooks.sh --action pre-push (test)
│   └── commit-msg                   # → hooks.sh --action commit-msg
│
├── helpers/
│   ├── shell/
│   │   ├── hooks.sh                 # lógica central de hooks
│   │   └── commit-msg.sh            # validador de Conventional Commits
│   └── python/
│       ├── changelog.py             # generador de CHANGELOG.md (release-time)
│       └── version.py               # lector/bumper de VERSION (release-time)
│
├── VERSION                          # versión actual (bumpeada en prepare-release)
├── CHANGELOG.md                     # generado en prepare-release
└── Justfile                         # recipes: hooks-install, prepare-release, version, changelog
```

### Flujo de delegación

```
git commit  → .githooks/pre-commit  → helpers/shell/hooks.sh --action pre-commit  → make lint
git push    → .githooks/pre-push    → helpers/shell/hooks.sh --action pre-push    → make test
git commit  → .githooks/commit-msg  → helpers/shell/hooks.sh --action commit-msg  → commit-msg.sh
```

Los dispatchers en `.githooks/` son scripts de 2 líneas que solo invocan `hooks.sh`. La lógica de lint/test/commit-msg vive en los helpers compartidos, reutilizando la cadena `Makefile → .mk → script`.

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
- Helpers: `hooks.sh` (despachador), `commit-msg.sh` (validación), `changelog.py`, `version.py`.
- Variables de entorno para sobrescribir gates: `PRE_COMMIT_TARGET` (default: `lint`), `PRE_PUSH_TARGET` (default: `test`).
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
bash helpers/shell/hooks.sh --action pre-commit     # make lint
bash helpers/shell/hooks.sh --action pre-push       # make test
bash helpers/shell/hooks.sh --action commit-msg .git/COMMIT_EDITMSG
```

## Ejemplos

### Dispatcher pre-commit

```bash
#!/usr/bin/env bash
exec bash helpers/shell/hooks.sh --action pre-commit
```

### Dispatcher con override de target (para repo docs)

```bash
#!/usr/bin/env bash
PRE_COMMIT_TARGET=validate exec bash helpers/shell/hooks.sh --action pre-commit
```

### hooks.sh (dispatch central)

```bash
case "$action" in
  pre-commit)
    local_target="${PRE_COMMIT_TARGET:-lint}"
    make "${local_target}"
    ;;
  pre-push)
    local_target="${PRE_PUSH_TARGET:-test}"
    make "${local_target}"
    ;;
  commit-msg)
    bash helpers/shell/commit-msg.sh "$msg_file"
    ;;
esac
```

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
- **Los dispatchers en `.githooks/` no contienen lógica.** Solo invocan `hooks.sh`. La lógica vive en helpers.
- **commit-msg valida Conventional Commits alineado con [Regla 05](05-version-control.md).** Merge commits y initial commit se ignoran.
- **Los hooks nunca deben tener dependencias externas** que no estén disponibles en el entorno de desarrollo (solo bash, git, y los helpers del proyecto).
- **Los hooks no deben romper el flujo de desarrollo.** Si un gate falla, debe mostrar un mensaje claro de qué corregir y cómo.

## Referencias

- [Regla 01: Build Tooling](01-build-tooling.md) — `make lint`, `make test`, capa de helpers.
- [Regla 05: Control de Versiones](05-version-control.md) — Conventional Commits.
- [Regla 06: CI/CD](06-ci-cd.md) — pipeline local como complemento a los hooks.
- [Regla 09: Estructura de Repositorio](09-repository-structure.md) — `.githooks/` en el árbol del proyecto.
- [Regla 11: Commitizen](11-commitizen.md) — asistente de commit + release (co-propietaria del objetivo).
- [templates/repository-structure/.githooks/](../templates/repository-structure/.githooks/) — dispatchers pre-commit, pre-push, commit-msg.
- [templates/helpers/shell/hooks.sh.tmpl](../templates/helpers/shell/hooks.sh.tmpl)
- [templates/helpers/shell/commit-msg.sh.tmpl](../templates/helpers/shell/commit-msg.sh.tmpl)
- [templates/helpers/python/changelog.py.tmpl](../templates/helpers/python/changelog.py.tmpl)
- [templates/helpers/python/version.py.tmpl](../templates/helpers/python/version.py.tmpl)

## Plantilla

- [templates/repository-structure/.githooks/](../templates/repository-structure/.githooks/)
- [templates/helpers/shell/hooks.sh.tmpl](../templates/helpers/shell/hooks.sh.tmpl)
- [templates/helpers/shell/commit-msg.sh.tmpl](../templates/helpers/shell/commit-msg.sh.tmpl)
- [templates/helpers/python/changelog.py.tmpl](../templates/helpers/python/changelog.py.tmpl)
- [templates/helpers/python/version.py.tmpl](../templates/helpers/python/version.py.tmpl)

---
id: version-control
title: Control de Versiones
status: Borrador
tags: [git, version-control, conventional-commits, branching, semver]
---

# Regla 05: Control de Versiones — ⚠️ *Borrador*



### Premisa: Premisa

Git es el estándar. Mensajes de commit claros y convencionales, branching predecible y versionado semántico facilitan el mantenimiento, la automatización de releases y la lectura por agentes de IA.

tags: [obligatorio]

### Restriccion: Restricciones

- **No hacer push a `main` directamente.** Todo cambio entra vía Pull Request con code review.
- **No usar mensajes de commit genéricos** (`fix`, `update`, `wip`). Siempre Conventional Commits.
- **No mantener branches muertas.** Eliminar la rama después del merge.
- **No crear tags sin seguir Semantic Versioning** (`vMAJOR.MINOR.PATCH`).

tags: [obligatorio]

### Ejemplo: Ejemplos

### Conventional Commits

```
feat(auth): add JWT token validation
fix(api): handle null pointer in user service
docs: update installation guide
refactor(core): extract validation to domain service
test(auth): add integration tests for login flow
chore: update dependencies
```

### Git Flow simplificado

```
main (producción)
  ↑
  ├─ release/v1.2.0
  │
develop (integración)
  ↑
  ├─ feature/nueva-funcionalidad
  ├─ bugfix/issue-123
  └─ hotfix/critico          (desde main)
```

### Semantic Versioning

```bash
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0
```

Formato: `v{MAJOR}.{MINOR}.{PATCH}`

tags: [obligatorio]

### Comportamiento: Trabajo en paralelo con worktrees

Usar `git worktree` para tareas paralelas (feature, hotfix, release) en **directorios hermanos** (`../wt-*`), compartiendo un solo repositorio. Cada worktree tiene su propia rama y directorio de trabajo, pero comparte el historial y los hooks del repositorio principal.

**Ventajas sobre `git stash` y cambio de rama:**
- No se pierde el contexto de la rama actual (builds, tests en curso, archivos abiertos).
- Se puede compilar/testear en paralelo sin `stash`/`checkout` costosos.
- Los hooks y gates (`pre-commit`, `pre-push`, `commit-msg`) se ejecutan **por worktree** (cada uno tiene su `HEAD` y `index` independientes).

```
repositorio/
├── .git/                    # compartido por todos los worktrees
├── src/                     # rama principal (main)
├── ../wt-feature-x/         # worktree hermano: rama feature/x
└── ../wt-hotfix/            # worktree hermano: rama hotfix/urgente
```

**Convención:** `../wt-<nombre-rama>` como path del worktree (ej. `../wt-feature-x`, `../wt-hotfix-123`), siempre fuera del repositorio (directorio hermano del raíz).

**Comandos canónicos:**

```bash
# Crear worktree + rama desde main
git worktree add ../wt-feature-x -b feature/x main

# Crear worktree desde una rama existente
git worktree add ../wt-hotfix-urgent hotfix/urgent

# Listar worktrees activos
git worktree list

# Proteger un worktree de ser eliminado accidentalmente
git worktree lock ../wt-feature-x --reason "en desarrollo activo"

# Desproteger
git worktree unlock ../wt-feature-x

# Eliminar worktree al terminar (después de merge/push)
git worktree remove ../wt-feature-x

# Limpiar metadatos huérfanos (worktrees eliminados sin remove)
git worktree prune
```

**Workflow típico:**
```
git worktree add ../wt-feature-x -b feature/x main
cd ../wt-feature-x
# ... desarrollar, commitear ...
cd -
git worktree remove ../wt-feature-x
git branch -D feature/x   # si ya se mergeó
git worktree prune
```

tags: [obligatorio]

### Restriccion: Restricciones de worktrees (complementarias)

- **Nunca borrar un worktree con `rm -rf` manual.** Usar `git worktree remove <path>` para eliminar el directorio y los metadatos administrativos. Un `rm -rf` deja metadatos huérfanos en `.git/worktrees/` que requieren `git worktree prune`.
- **`git worktree prune` debe ejecutarse regularmente** para limpiar worktrees eliminados incorrectamente (equivalente a `git gc` para worktrees).
- **Una rama solo puede estar en un worktree a la vez.** Intentar `git worktree add` sobre una rama ya en uso en otro worktree fallará (git lo impide).
- **`git worktree remove` no borra la rama**, solo el directorio de trabajo. La rama se elimina con `git branch -d` después del merge.
- **El trabajo no commiteado en un worktree se pierde si se ejecuta `git worktree remove` sin guardar.** Hacer commit o stash antes de eliminar.
- **Los worktrees no se pushean ni se comparten entre máquinas** — son locales al clon.

tags: [obligatorio]

### Referencia: Referencias

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Regla 10: Git Hooks](10-githooks.md) — commit-msg valida Conventional Commits en cada commit.

tags: [obligatorio]

---
id: version-control
title: Control de Versiones
status: Borrador
tags: [git, version-control, conventional-commits, branching, semver]
---

# Regla 05: Control de Versiones

## Premisa

Git es el estándar. Mensajes de commit claros y convencionales, branching predecible y versionado semántico facilitan el mantenimiento, la automatización de releases y la lectura por agentes de IA.

## Restricciones

- **No hacer push a `main` directamente.** Todo cambio entra vía Pull Request con code review.
- **No usar mensajes de commit genéricos** (`fix`, `update`, `wip`). Siempre Conventional Commits.
- **No mantener branches muertas.** Eliminar la rama después del merge.
- **No crear tags sin seguir Semantic Versioning** (`vMAJOR.MINOR.PATCH`).

## Ejemplos

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

## Referencias

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Regla 10: Git Hooks](10-githooks.md) — commit-msg valida Conventional Commits en cada commit.

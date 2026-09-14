# hooks-install

## Nombre

hooks-install — instala los git hooks del repositorio

## Sinopsis

```
just hooks-install
just hooks-install --man
bash helpers/shell/hooks.sh --action install --man
```

## Descripción

Configura `core.hooksPath = .githooks` y hace bootstrap de Commitizen
(`helpers/shell/cz.sh --action bootstrap`). Reporta si `gitleaks` y
`trufflehog` (regla 13) están instalados.

## Opciones

Sin flags propios; `*args` se reenvía tal cual al helper
`helpers/shell/hooks.sh --action install`.

## Ejemplos

```bash
just hooks-install
```

## Véase también

- [Regla 10: Git Hooks](rules/10-githooks.md)
- [Regla 01: Herramientas de Construcción](rules/01-build-tooling.md)

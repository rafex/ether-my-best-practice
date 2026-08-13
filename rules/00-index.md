# Índice de Reglas - Ether My Best Practice

## Estructura de Reglas

Este repositorio contiene un conjunto de premisas y estándares para el desarrollo de software. Las reglas y [plantillas](../templates/) son el objetivo del repositorio: definiciones que los agentes de IA consumen para generar proyectos consistentes.

> **Separación:** este repositorio distingue entre definiciones (`rules/` + `templates/`) y la infraestructura operativa del propio repositorio (`Makefile`, `Justfile`, `helpers/`). Las reglas describen cómo debe construirse un proyecto consumidor; el `Makefile` raíz solo publica el sitio y valida las reglas.

| # | Regla | Estado | Tema |
|---|-------|--------|------|
| 1 | **[01-build-tooling.md](01-build-tooling.md)** | Definida | Herramientas de construcción (Makefile, Justfile, helpers) |
| 2 | **[02-architecture_draft.md](02-architecture_draft.md)** | ⚠️ *Borrador* | Patrones arquitectónicos (Hexagonal, puertos y adaptadores) |
| 3 | **[03-testing_draft.md](03-testing_draft.md)** | ⚠️ *Borrador* | Estrategias de testing (TDD, pirámide de tests) |
| 4 | **[04-documentation_draft.md](04-documentation_draft.md)** | ⚠️ *Borrador* | Documentación como código (Markdown, MkDocs) |
| 5 | **[05-version-control_draft.md](05-version-control_draft.md)** | ⚠️ *Borrador* | Control de versiones (Git flow, Conventional Commits) |
| 6 | **[06-ci.md](06-ci.md)** | Definida | Integración Continua (pipelines, contenedores) |
| 7 | **[07-agents-mcp.md](07-agents-mcp.md)** | Definida | Reglas para agentes de IA y Model Context Protocol |
| 8 | **[08-stack.md](08-stack.md)** | Definida | Stack tecnológico recomendado (versiones, runtimes, contenedores) |
| 9 | **[09-repository-structure.md](09-repository-structure.md)** | Definida | Estructura de repositorio multi-lenguaje por rol |
| 10 | **[10-githooks.md](10-githooks.md)** | Definida | Git hooks — gates de lint/test/commit-msg y flujo de release |
| 11 | **[11-commitizen.md](11-commitizen.md)** | Definida | Commitizen — asistente de commit convencional y release |
| 12 | **[12-gitignore.md](12-gitignore.md)** | Definida | Gitignore — exclusión de archivos por contexto |
| 13 | **[13-secrets.md](13-secrets.md)** | Definida | Gestión de secretos con sops+age, gitleaks y trufflehog |
| 14 | **[14-config-files.md](14-config-files.md)** | Definida | Archivos de configuración (.config) — centralización por herramienta |
| 15 | **[15-script-reuse.md](15-script-reuse.md)** | Definida | Reutilización de Scripts — librerías comunes shell y python |
| 16 | **[16-cd.md](16-cd.md)** | Definida | Despliegue Continuo — CD portable, local-first, sops+age |
| 17 | **[17-code-clean-types-and-enums_draft.md](17-code-clean-types-and-enums_draft.md)** | ⚠️ *Borrador* | Código Limpio — Tipos fuertes y enums (evitar stringly-typed) |

> **Convención:** las reglas con `status: Borrador` en el frontmatter llevan el sufijo `_draft` en el nombre del archivo y `— ⚠️ *Borrador*` en el título H1. Contienen premisa y restricciones pero aún no alcanzan la profundidad completa.

## Cómo Usar Este Índice

Cada regla es un documento Markdown independiente que puede ser:
- Consultado por humanos
- Servido a través de MCP para agentes de IA
- Publicado en una página web con MkDocs

Las plantillas en [templates/](../templates/) complementan las reglas como cascarones listos para copiar a proyectos consumidores.

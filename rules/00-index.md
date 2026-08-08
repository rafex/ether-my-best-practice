# Índice de Reglas - Ether My Best Practice

## Estructura de Reglas

Este repositorio contiene un conjunto de premisas y estándares para el desarrollo de software. Las reglas y [plantillas](../templates/) son el objetivo del repositorio: definiciones que los agentes de IA consumen para generar proyectos consistentes.

> **Separación:** este repositorio distingue entre definiciones (`rules/` + `templates/`) y la infraestructura operativa del propio repositorio (`Makefile`, `Justfile`, `helpers/`). Las reglas describen cómo debe construirse un proyecto consumidor; el `Makefile` raíz solo publica el sitio y valida las reglas.

| # | Regla | Tema |
|---|-------|------|
| 1 | **[01-build-tooling.md](01-build-tooling.md)** | Herramientas de construcción (Makefile, Justfile, helpers) |
| 2 | **[02-architecture.md](02-architecture.md)** | Patrones arquitectónicos (Hexagonal, puertos y adaptadores) |
| 3 | **[03-testing.md](03-testing.md)** | Estrategias de testing (TDD, pirámide de tests) |
| 4 | **[04-documentation.md](04-documentation.md)** | Documentación como código (Markdown, MkDocs) |
| 5 | **[05-version-control.md](05-version-control.md)** | Control de versiones (Git flow, Conventional Commits) |
| 6 | **[06-ci-cd.md](06-ci-cd.md)** | Integración y despliegue continuo (Pipelines, GitHub Pages) |
| 7 | **[07-agents-mcp.md](07-agents-mcp.md)** | Reglas para agentes de IA y Model Context Protocol |
| 8 | **[08-stack.md](08-stack.md)** | Stack tecnológico recomendado (versiones, runtimes, contenedores) |
| 9 | **[09-repository-structure.md](09-repository-structure.md)** | Estructura de repositorio multi-lenguaje por rol |
| 10 | **[10-githooks.md](10-githooks.md)** | Git hooks — gates de lint/test/commit-msg y flujo de release |
| 11 | **[11-commitizen.md](11-commitizen.md)** | Commitizen — asistente de commit convencional y release |

> **Estado:** cada regla declara su estado (`Definida` | `Borrador`) en el frontmatter YAML del archivo. Las reglas en **Borrador** contienen premisa y restricciones pero aún no alcanzan la profundidad completa (Comandos, Estructura detallada, etc.).

## Cómo Usar Este Índice

Cada regla es un documento Markdown independiente que puede ser:
- Consultado por humanos
- Servido a través de MCP para agentes de IA
- Publicado en una página web con MkDocs

Las reglas cuyo frontmatter indica `status: Borrador` contienen una premisa y restricciones, pero aún no alcanzan la profundidad de las reglas `Definida`. Las plantillas en [templates/](../templates/) complementan las reglas como cascarones listos para copiar a proyectos consumidores.

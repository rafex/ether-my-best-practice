# Índice de Reglas - Ether My Best Practice

## Estructura de Reglas

Este repositorio contiene un conjunto de premisas y estándares para el desarrollo de software. Las reglas y [plantillas](../templates/) son el objetivo del repositorio: definiciones que los agentes de IA consumen para generar proyectos consistentes.

> **Separación:** este repositorio distingue entre definiciones (`rules/` + `templates/`) y la infraestructura operativa del propio repositorio (`Makefile`, `Justfile`, `helpers/`). Las reglas describen cómo debe construirse un proyecto consumidor; el `Makefile` raíz solo publica el sitio y valida las reglas.

| # | Regla | Estado |
|---|-------|--------|
| 1 | **[01-build-tooling.md](01-build-tooling.md)** - Herramientas de construcción (Makefile, Justfile, helpers) | Definida |
| 2 | **[02-architecture.md](02-architecture.md)** - Patrones arquitectónicos (Hexagonal, puertos y adaptadores) | Borrador |
| 3 | **[03-testing.md](03-testing.md)** - Estrategias de testing (TDD, pirámide de tests) | Borrador |
| 4 | **[04-documentation.md](04-documentation.md)** - Documentación como código (Markdown, MkDocs) | Borrador |
| 5 | **[05-version-control.md](05-version-control.md)** - Control de versiones (Git flow, commits) | Borrador |
| 6 | **[06-ci-cd.md](06-ci-cd.md)** - Integración y despliegue continuo (Pipelines, GitHub Pages) | Definida |
| 7 | **[07-agents-mcp.md](07-agents-mcp.md)** - Reglas para agentes de IA (Model Context Protocol) | Borrador |

## Cómo Usar Este Índice

Cada regla es un documento Markdown independiente que puede ser:
- Consultado por humanos
- Servido a través de MCP para agentes de IA
- Publicado en una página web con MkDocs

Las reglas marcadas como **Borrador** contienen una premisa y estructura básica, pero aún no alcanzan la profundidad de las reglas definidas. Las plantillas en [templates/](../templates/) complementan las reglas como cascarones listos para copiar a proyectos consumidores.

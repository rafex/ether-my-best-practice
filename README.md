# Ether My Best Practice

Plantilla de buenas prácticas para construir APIs REST con reglas consumibles por agentes de IA y plantillas reutilizables que sirven como cascarones de implementación.

## Objetivo

Este repositorio define una base de trabajo para proyectos donde:

- Las reglas de desarrollo viven como documentos versionados en [rules](rules).
- Los agentes de IA pueden consultar esas reglas mediante archivos o mediante MCP.
- Las plantillas en [templates](templates) funcionan como esqueletos que los agentes pueden copiar y adaptar para crear proyectos consistentes.

La intención no es solo documentar estándares, sino permitir que un agente entienda cómo debe construir una API REST siguiendo tu forma de trabajar.

## Qué contiene

- [rules](rules): reglas de arquitectura, testing, documentación, control de versiones, CI/CD y agentes/MCP.
- [templates](templates): cascarones reutilizables para Makefile, Justfile, configuración MCP y estructura de proyecto.
- [docs](docs): documentación MkDocs para navegar el estándar como sitio estático.
- [helpers/shell/validate-rules.sh](helpers/shell/validate-rules.sh): validación mínima de estructura y enlaces entre reglas.

## Cómo lo usaría un agente

1. Lee [rules/00-index.md](rules/00-index.md) para descubrir las reglas disponibles.
2. Consulta reglas concretas como [rules/02-architecture.md](rules/02-architecture.md) y [rules/07-agents-mcp.md](rules/07-agents-mcp.md).
3. Usa [templates](templates) como base para generar archivos iniciales de un proyecto API REST.
4. Mantiene trazabilidad porque las reglas y plantillas están versionadas en el mismo repositorio.

## Flujo recomendado

1. Mantener las reglas como fuente de verdad.
2. Exponerlas a agentes por lectura directa del repo o mediante MCP.
3. Usar las plantillas como punto de partida para nuevos servicios.
4. Ajustar los cascarones generados en el proyecto consumidor sin convertir este repositorio en un proyecto final.

## Validación

```bash
bash helpers/shell/validate-rules.sh
```

Para construir el sitio localmente:

```bash
mkdocs build
mkdocs serve
```

Para publicar en GitHub Pages usando el workflow del repositorio:

```bash
make pages-build
make pages
```
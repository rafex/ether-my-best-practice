---
id: agents-mcp
title: Agentes de IA y Model Context Protocol
status: Borrador
tags: [agents, ai, mcp, copilot, templates]
---

# Regla 07: Agentes de IA y Model Context Protocol (MCP)

## Premisa

Las reglas y plantillas de este repositorio deben ser accesibles a agentes de IA (Claude, GitHub Copilot, opencode) a través de lectura directa de archivos o mediante Model Context Protocol (MCP), para que el agente pueda generar proyectos consistentes con el estándar.

## Restricciones

- Las plantillas en [templates/](../templates/) **son cascarones reutilizables, no proyectos finales.** Un agente debe copiarlas y adaptarlas en el proyecto consumidor, nunca modificar este repositorio como si fuera el servicio destino.
- **No reescribir reglas ni plantillas en el prompt del agente.** El agente debe leer los archivos fuente de `rules/` y `templates/`, no recibir resúmenes que puedan desactualizarse.
- Un agente no debe aplicar reglas de este repo a menos que el proyecto declare explícitamente que las sigue.

## Ejemplos

### Flujo de trabajo de un agente

1. Leer `rules/00-index.md` para descubrir las reglas disponibles.
2. Consultar las reglas aplicables (ej. `rules/02-architecture.md` para estructura, `rules/07-agents-mcp.md` para contexto).
3. Copiar los templates de `templates/` como punto de partida.
4. Adaptar el cascarón en el proyecto consumidor sin modificar este repositorio.

### Prompt mínimo para un agente

```
Eres un asistente de codificación trabajando en un proyecto que sigue Ether Best Practices.

Reglas de contexto:
- Build: rules/01-build-tooling.md
- Arquitectura: rules/02-architecture.md
- Testing: rules/03-testing.md

Al generar código:
- Arquitectura hexagonal (puertos y adaptadores)
- Tests con TDD
- Conventional Commits
```

### MCP (Model Context Protocol)

Cada regla puede exponerse como recurso MCP para que agentes como Claude o Copilot la consulten:

```json
{
  "mcp_servers": {
    "ether-rules": {
      "command": "node",
      "args": ["mcp-server.js"],
      "env": { "RULES_DIR": "./rules" }
    }
  }
```

### Opciones de integración

1. **Lectura directa:** el agente clona el repo y lee archivos `.md`.
2. **Servidor MCP:** expone `ether://rules/{id}` como recursos.
3. **Embeddings + RAG:** vectorizar reglas para búsqueda semántica (opcional, avanzado).

## Referencias

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [templates/mcp-config.json.tmpl](../templates/mcp-config.json.tmpl)
- [templates/rule-template.md.tmpl](../templates/rule-template.md.tmpl)
- [Regla 04: Documentación](04-documentation.md)

## Plantilla

- [templates/mcp-config.json.tmpl](../templates/mcp-config.json.tmpl)
- [templates/rule-template.md.tmpl](../templates/rule-template.md.tmpl)

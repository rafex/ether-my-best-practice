---
id: agents-mcp
title: Agentes de IA y Model Context Protocol
status: Definida
tags: [agents, ai, mcp, server, resources, tools, prompts]
checksum: 8ac5529c3c0ade32017d72b000b511476d319ca9aff5a3d03121636875ebe4bb
---

# Regla 07: Agentes de IA y Model Context Protocol (MCP)



### Premisa: Premisa

Las reglas y plantillas de este repositorio deben ser accesibles a agentes de IA (Claude, GitHub Copilot, opencode) mediante el **Model Context Protocol (MCP)**, exponiendo resources (datos), tools (acciones) y prompts (plantillas de interacción). El servidor MCP `ether-rules` se implementa en Python con `uv` y reutiliza las librerías comunes (`helpers/python/lib/`) para logging, mensajes, y manejo de errores (regla 15).

> **El MCP es infraestructura opcional de este repositorio** para disponibilizar las definiciones a agentes. El template `mcp/` del espejo (`repository-structure/mcp/`) es una **sugerencia de intención**, no una obligación. Si un proyecto consumidor no usa agentes MCP, puede omitir la carpeta `mcp/` por completo.

tags: [obligatorio]

### Estructura: Estructura

### Servidor MCP

```
mcp/
├── source/
│   ├── server.py          # MCPServer: @mcp.resource, @mcp.tool, @mcp.prompt
│   ├── config.py          # rutas (RULES_DIR, TEMPLATES_DIR)
│   └── requirements.txt   # mcp>=1.0, PyYAML>=6.0
└── .venv/                 # no trackeado (uv run)
```

### Recursos expuestos (Resources)

| URI | Contenido |
|---|---|
| `rules://index` | Índice de reglas (00-index.md) |
| `rules://{id}` | Regla individual (ej. `01-build-tooling`) |
| `templates://index` | README del repositorio de templates |
| `templates://{path}` | Template por ruta (ej. `Makefile.tmpl`) |
| `gitignore://{context}` | `.gitignore.{context}.tmpl` (raiz, java, python, rust, nodejs, container, secretos, temporales, mcp) |
| `helpers://{lang}/{name}` | Helper/lib por lenguaje (ej. `shell/lint`, `python/changelog`) |
| `docs://{page}` | Documentación (index, getting-started, contributing) |

### Herramientas (Tools)

| Tool | Descripción | Reutiliza |
|---|---|---|
| `list_rules()` | Lista reglas con id, título, estado, tags | Frontmatter YAML |
| `get_rule(id)` | Contenido completo de una regla | — |
| `search_rules(query)` | Busca reglas por texto | BM25/grep |
| `list_templates()` | Lista todos los templates | `repository-structure/` |
| `get_template(path)` | Lee un template por ruta | — |
| `scaffold_project(slug, lang, dest)` | Genera cascarón: copia repository-structure + gitignore por lenguaje | `repository-structure/`, `gitignore/` |
| `check_project(dir)` | Valida proyecto contra reglas (reusa validate-rules.sh) | `validate-rules.sh` |
| `list_helpers(lang)` | Lista helpers por lenguaje | `helpers/` |
| `get_helper(lang, name)` | Lee un helper/lib | — |

### Plantillas de interacción (Prompts)

| Prompt | Guía |
|---|---|
| `scaffold_project(slug, stack)` | Generar proyecto consumidor completo |
| `implement_feature(rule_id, context)` | Implementar según una regla específica |
| `review_project(dir_path)` | Auditar proyecto contra el estándar |
| `configure_tool(herramienta)` | Configurar `.config/<herramienta>/` (regla 14) |
| `commit_workflow()` | Conventional Commits + Commitizen (regla 11) |

### Configuración del cliente

```json
{
  "mcpServers": {
    "ether-rules": {
      "command": "uv",
      "args": ["run", "--directory", "mcp", "python", "source/server.py"],
      "env": { "RULES_DIR": "rules", "TEMPLATES_DIR": "templates" }
    }
  }
}
```

tags: [opcional]

### Comando: Comandos

### Ejecutar el servidor MCP

```bash
uv run --directory mcp python source/server.py
```

### Instalar el MCP en un cliente (Claude, opencode)

```bash
# Copiar mcp-config.json al directorio de configuración del cliente
cat mcp-config.json

# O usar el template:
cp templates/repository-structure/mcp/mcp-config.json.tmpl mcp-config.json
```

### Verificar registro de tools/prompts/resources

```python
# Smoke test — desde el intérprete Python con uv
uv run --directory mcp python -c "
from source.server import mcp
print('Server:', mcp.name)
"
```

tags: [opcional]

### Ejemplo: Ejemplos

### Flujo completo de un agente con MCP

1. **Descubrir reglas:** `list_rules()` → `[{id: "01-build-tooling", status: "Definida", ...}, ...]`.
2. **Leer regla específica:** `get_rule("01-build-tooling")` → contenido completo.
3. **Buscar por contexto:** `search_rules("secretos sops")` → reglas 08, 12, 13.
4. **Obtener template:** `get_template("Makefile.tmpl")` → Makefile template.
5. **Generar proyecto:** `scaffold_project("patos", "java")` → cascarón en `./patos/`.
6. **Validar:** `check_project("./patos")` → 0 errores.

### Prompt de scaffolding en acción

El agente invoca el prompt `scaffold_project(slug="patos", stack="java+maven")` y recibe una guía detallada de 7 pasos para generar el proyecto, referenciando las reglas 01, 02, 03, 05, 08, 09, 12, 15.

tags: [obligatorio]

### Restriccion: Restricciones

- **El servidor MCP no requiere clonar el repositorio.** El cliente ejecuta `uv run` apuntando a la ruta del server; el server lee `rules/` y `templates/` del sistema de archivos local.
- **Las plantillas son cascarones reutilizables, no proyectos finales.** El agente copia y adapta, nunca modifica el repositorio de reglas.
- **No reescribir reglas en prompts de usuario.** El agente usa las tools `get_rule`/`search_rules`, no resúmenes desactualizados.
- **El venv del MCP (`mcp/.venv/`) no se versiona.** Está en `.gitignore`; `uv run` gestiona las dependencias automáticamente.
- **El servidor importa `lib/logs.py`, `lib/messages.py`, `lib/colors.py`, `lib/exceptions.py`** (regla 15) — la capa de libs es compartida entre helpers y MCP.
- **Los resources aceptan parámetros en la URI** (ej. `rules://{id}`) usando el formato de template de MCP.
- **`scaffold_project` genera en un destino dado por el agente**, no en el repositorio de reglas.

tags: [obligatorio]

### Referencia: Referencias

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Regla 15: Reutilización de Scripts](15-script-reuse.md) — libs comunes (logs, messages, colors, exceptions).
- [Regla 14: Archivos de Configuración](14-config-files.md) — `.config/` por herramienta.
- [Regla 01: Build Tooling](01-build-tooling.md) — helpers como capa única de ejecución.
- [mcp/pyproject.toml](../mcp/pyproject.toml) — paquete Python distribuible (wheel).
- [mcp/README.md](../mcp/README.md) — manual de instalación y uso.
- [templates/repository-structure/mcp/](../templates/repository-structure/mcp/) — plantillas del servidor MCP.

tags: [obligatorio]

### Plantilla: Plantilla

- [templates/repository-structure/mcp/mcp-config.json.tmpl](../templates/repository-structure/mcp/mcp-config.json.tmpl)
- [templates/repository-structure/mcp/source/server.py.tmpl](../templates/repository-structure/mcp/source/server.py.tmpl)
- [templates/repository-structure/mcp/source/config.py.tmpl](../templates/repository-structure/mcp/source/config.py.tmpl)
- [templates/repository-structure/mcp/source/requirements.txt.tmpl](../templates/repository-structure/mcp/source/requirements.txt.tmpl)

tags: [opcional]

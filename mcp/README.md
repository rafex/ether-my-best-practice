# Ether MCP — My Best Practices

Servidor **Model Context Protocol** que expone las [reglas](https://my-best-practice.rafex.io/rules/00-index/) y [templates](https://github.com/rafex/ether-my-best-practice) del estándar Ether Best Practices como Resources, Tools y Prompts para agentes de IA (Claude, opencode, Copilot).

## Requisitos previos

- Python 3.12 o superior
- [uv](https://docs.astral.sh/uv/) (gestor de paquetes)
- Conexión a internet (para la estrategia "sitio primero" de datos)

## Instalación

### Desde el wheel descargable (recomendado)

```bash
# Descargar el wheel desde https://github.com/rafex/ether-my-best-practice/releases/latest
uv tool install ./ether_mcp_my_best_practices-1.0.0-py3-none-any.whl
```

El comando `ether-mcp` quedará disponible en el PATH.

### Con uvx (ejecución directa sin instalar)

```bash
uvx ether-mcp-my-best-practices
```

## Configuración en el cliente

Añadir al archivo `mcp-config.json` de tu cliente (Claude Desktop, opencode, etc.):

```json
{
  "mcpServers": {
    "ether-rules": {
      "command": "uvx",
      "args": ["ether-mcp"],
      "env": {
        "RULES_DIR": "",
        "TEMPLATES_DIR": ""
      }
    }
  }
}
```

> Si has instalado con `uv tool install`, usa `"command": "ether-mcp"` en lugar de `uvx`.

## Estrategia de datos (resources)

El servidor resuelve los datos de reglas y templates en este orden:

1. **Variables de entorno** `RULES_DIR` / `TEMPLATES_DIR` (máxima prioridad) — para usar un clon local del repositorio.
2. **Sitio público** [`https://my-best-practice.rafex.io/ether-rules/`](https://my-best-practice.rafex.io/ether-rules/) — intenta descargar el contenido más actualizado a una caché local (`~/.cache/ether-mcp/`).
3. **Snapshot empaquetado** (fallback autocontenido dentro del wheel).

## Resources

| Resource | Descripción |
|---|---|
| `rules://index` | Índice de reglas |
| `rules://{rule_id}` | Regla por ID (ej. `build-tooling`, `11-commitizen`) |
| `templates://index` | Índice global de templates |
| `templates://{path}` | Template por ruta (ej. `repository-structure/Makefile.tmpl`) |
| `gitignore://{context}` | `.gitignore` por contexto (raiz, java, python, rust, nodejs, container, secretos, temporales, mcp) |
| `helpers://{lang}/{name}` | Helper por lenguaje y nombre |
| `docs://{page}` | Página de documentación |

## Tools

| Tool | Descripción |
|---|---|
| `list_rules()` | Lista reglas (id, título, estado, tags) |
| `get_rule(rule_id)` | Contenido completo de una regla |
| `search_rules(query)` | Busca reglas por texto |
| `list_templates()` | Lista todos los templates |
| `get_template(path)` | Lee un template |
| `scaffold_project(slug, lang, dest)` | Genera cascarón de proyecto |
| `check_project(dir)` | Valida proyecto contra reglas |
| `list_helpers(lang)` | Lista helpers por lenguaje |
| `get_helper(lang, name)` | Lee un helper |

## Prompts

| Prompt | Guía |
|---|---|
| `scaffold_project(slug, stack)` | Generar proyecto consumidor |
| `implement_feature(rule_id, context)` | Implementar según regla |
| `review_project(dir_path)` | Auditar proyecto |
| `configure_tool(herramienta)` | Configurar `.config/<herramienta>/` |
| `commit_workflow()` | Conventional Commits + Commitizen |

## Desinstalación

```bash
uv tool uninstall ether-mcp-my-best-practices
```

## Desarrollo local

Para ejecutar sin instalar, desde la raíz del repositorio:

```bash
uv run --directory mcp python ether_mcp_my_best_practices/server.py
```

O `just serve` para desarrollo completo con el sitio.

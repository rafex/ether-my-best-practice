# Descargar el MCP

El servidor MCP `ether-rules` está disponible como paquete Python instalable. Expone las reglas y templates de Ether Best Practices como **Resources, Tools y Prompts** para agentes de IA compatibles con el Model Context Protocol (Claude Desktop, opencode, GitHub Copilot, etc.).

## Descarga

El paquete se distribuye como wheel en los [Releases de GitHub](https://github.com/rafex/ether-my-best-practice/releases/latest). Consulta la **[guía de instalación por sistema operativo](mcp-install.md)** para instrucciones completas (Linux, macOS, Windows) y la configuración automática en Claude Code, Codex y opencode.

- **Última versión:** [Releases/latest](https://github.com/rafex/ether-my-best-practice/releases/latest)

## Instalación

### Requisitos

- Python 3.12 o superior
- [uv](https://docs.astral.sh/uv/) (gestor de paquetes) o pip 23+

### Instalar desde el wheel

```bash
# Descarga el wheel y ejecuta:
uv tool install ./ether_mcp_my_best_practices-*.whl
```

El comando `ether-mcp` quedará disponible en el PATH.

### Ejecución directa sin instalar

```bash
uvx ether-mcp-my-best-practices
```

## Configurar el cliente

Añade al archivo `mcp-config.json` de tu cliente:

```json
{
  "mcpServers": {
    "ether-rules": {
      "command": "uvx",
      "args": ["ether-mcp"],
      "env": {
        "RULES_REMOTE_URL": "https://my-best-practice.rafex.io/ether-rules"
      }
    }
  }
}
```

> Si instalaste con `uv tool install`, cambia `"command": "uvx"` por `"command": "ether-mcp"` y quita `"args"`.

## Resolución de las reglas (remoto → empaquetado)

El servidor resuelve las reglas, templates, helpers y docs en este orden:

1. **Override explícito** — variables `RULES_DIR`, `TEMPLATES_DIR`, `HELPERS_DIR`, `DOCS_DIR` si apuntan a un directorio existente.
2. **Remoto (web)** — descarga desde `RULES_REMOTE_URL` (por defecto `https://my-best-practice.rafex.io/ether-rules`, el contenido público que sirve el sitio [my-best-practice.rafex.io](https://my-best-practice.rafex.io)). Usa el manifest `checksums.json` para descargar **solo** los archivos nuevos o cuyo hash cambió, y los guarda en `~/.cache/ether-mcp/`.
3. **Empaquetado (bundled)** — usa el snapshot `data/` incluido en el wheel, si el remoto no está disponible.
4. **Clon local** — `MCP_ROOT/<dir>`.

Cada regla (`rules/*.md`) lleva su propio hash en el frontmatter (`checksum: <sha256>`), generado con `make checksums`. El manifest `checksums.json` se publica en el sitio (no se versiona en el repositorio) mediante `make publish-checksums`. Para forzar una fuente concreta, configura `RULES_REMOTE_URL` en el `env` del servidor:

```json
{
  "mcpServers": {
    "ether-rules": {
      "command": "uvx",
      "args": ["ether-mcp"],
      "env": {
        "RULES_REMOTE_URL": "https://my-best-practice.rafex.io/ether-rules"
      }
    }
  }
}
```

> Si `RULES_REMOTE_URL` no es accesible (sin red, error HTTP, etc.), el servidor cae automáticamente a la versión empaquetada sin interrumpir el servicio.

## Resources disponibles

| Resource | Ejemplo |
|---|---|
| `rules://index` | Índice de las 16 reglas |
| `rules://{rule_id}` | `rules://build-tooling` → regla 01 completa |
| `templates://index` | Todos los templates (repository-structure, gitignore, rule-template) |
| `templates://{path}` | `templates://gitignore/.gitignore.java.tmpl` |
| `gitignore://{context}` | `gitignore://java` |
| `helpers://{lang}/{name}` | `helpers://shell/lint` |
| `docs://{page}` | `docs://index` |

## Tools

| Tool | Uso |
|---|---|
| `list_rules()` | Lista reglas (id, título, estado, tags) |
| `get_rule(id)` | Contenido completo de una regla |
| `search_rules(query)` | Busca reglas por texto |
| `scaffold_project(slug, lang)` | Genera cascarón de proyecto desde repository-structure |
| `check_project(dir)` | Valida proyecto contra reglas |

## Desinstalar

```bash
uv tool uninstall ether-mcp-my-best-practices
```

## Desarrollo local

Si clonas este repositorio, puedes ejecutar el MCP sin instalar:

```bash
uv run --directory mcp python ether_mcp_my_best_practices/server.py
```

La [regla 07](rules/07-agents-mcp.md) documenta los Resources, Tools y Prompts en detalle.

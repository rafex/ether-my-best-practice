# Ether My Best Practice

Estándar de buenas prácticas multi-lenguaje con reglas versionadas consumibles por agentes de IA y plantillas reutilizables que sirven como cascarones de implementación.

## Objetivo

Este repositorio define una base de trabajo para proyectos donde:

- Las reglas de desarrollo viven como documentos versionados en [rules](rules) con frontmatter YAML, secciones estandarizadas y validación automática de estructura/enlaces.
- Los agentes de IA pueden consultar esas reglas por lectura directa o mediante el [servidor MCP](mcp/source/server.py) (`resources`, `tools`, `prompts`).
- Las plantillas en [templates](templates) funcionan como esqueletos que los agentes copian y adaptan para crear proyectos consistentes.

La intención no es solo documentar estándares, sino permitir que un agente entienda cómo debe construir una API REST — o cualquier componente backend/frontend — siguiendo tu forma de trabajar.

## Qué contiene

| Capa | Directorio | Contenido |
|---|---|---|
| **Definiciones** (objetivo) | [rules](rules) | 16 reglas con frontmatter — build tooling, arquitectura hexagonal, testing, documentación, version control, CI, agentes/MCP, stack, estructura de repo, githooks, commitizen, gitignore, secretos, .config, script reuse. Las marcadas `status: Definida` están completas; las `Borrador` contienen Premisa + Restricciones. |
| **Definiciones** (objetivo) | [templates](templates) | [repository-structure/](templates/repository-structure) (espejo del proyecto consumidor: `helpers/`, `containers/`, `.config/`, `.githooks/`, `source/`, `Makefile`, `Justfile`), [gitignore/](templates/gitignore) (biblioteca de `.gitignore` por contexto), [rule-template.md.tmpl](templates/rule-template.md.tmpl). |
| **Operativa** | [.config](.config) | Configuración centralizada de herramientas: commitizen (`pyproject.toml`), mkdocs (`mkdocs.yml` + `requirements.txt`), sops (`.sops.yaml`). |
| **Operativa** | [mcp](mcp) | Servidor MCP `ether-rules`: expone `rules://`, `templates://`, `gitignore://`, `helpers://`, `docs://` como resources + 9 tools (`scaffold_project`, `search_rules`, …) + 5 prompts. Infraestructura opcional de este repositorio para disponibilizar las definiciones a agentes. [mcp-config.json](mcp-config.json) para clientes. |
| **Operativa** | [helpers](helpers) | [validate-rules.sh](helpers/shell/validate-rules.sh) (estructura + enlaces + sincronía rules↔docs/rules), [rules-link.sh](helpers/shell/rules-link.sh) (hard links para MkDocs), [serve.sh](helpers/shell/serve.sh) (node static server), [hooks.sh](helpers/shell/hooks.sh) (gates pre-commit/pre-push con gitleaks/trufflehog), [cz.sh](helpers/shell/cz.sh), [secrets.sh](helpers/shell/secrets.sh) (sops+age), [github.sh](helpers/shell/github.sh) (workflows). Librerías comunes en `lib/` (shell: commons, logs, colors, messages, try-catch; python: commons, logs, colors, messages, exceptions). |
| **Operativa** | [docs](docs) | Documentación MkDocs: index, getting-started, contributing, `rules/` (hard links a las reglas). |
| **Operativa** | raíz | [Makefile](Makefile) (orquestación: validate, link-rules, docs, pages-build, pages, clean) y [Justfile](Justfile) (operativas: serve, serve-dev, link-rules, hooks-install, commit, changelog, version, prepare-release, cz-init, edit-secrets, env, secrets-verify, keygen). |

> **Separación de responsabilidades:** [rules](rules) y [templates](templates) son **el objetivo del repositorio** (lo que los agentes consumen). Todo lo demás — `.config/`, `mcp/`, `helpers/`, `docs/`, `Makefile`, `Justfile`, `.github/` — atiende únicamente a la **operación de este repositorio**: validar reglas, publicar el sitio, mantener la documentación y disponibilizar las definiciones vía MCP.

## Cómo lo usaría un agente

1. Lee [rules/00-index.md](rules/00-index.md) para descubrir las reglas disponibles (por lectura directa o vía `list_rules()` del MCP).
2. Consulta reglas concretas con `get_rule("08-stack")` / `search_rules("secretos")` o leyendo los archivos `.md`.
3. Usa [templates](templates) como base: `scaffold_project("patos", "java")` via MCP, o copia manualmente `repository-structure/` + `gitignore/<lenguaje>`.
4. Aplica las Restricciones, Comandos y Ejemplos de cada regla al generar código.
5. Valida con `check_project(dir)` vía MCP o ejecutando `bash helpers/shell/validate-rules.sh` en el proyecto generado.

También puede conectarse al servidor MCP configurando `mcp-config.json` en su cliente (Claude, opencode):

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

O ejecutarlo directamente: `uv run --directory mcp python source/server.py`.

## Operar este repositorio

### Validación y sitio

```bash
make validate      # Estructura, enlaces y sincronía rules↔docs/rules (0 errores)
make link-rules    # Hard links rules/ → docs/rules/ (necesario para MkDocs)
make docs          # Generar sitio estático (.config/mkdocs/mkdocs.yml)
make pages-build   # validate + link-rules + docs
make pages         # Disparar workflow de GitHub Pages (gh workflow run)
make clean         # Eliminar site/
```

### Just — operativas locales

```bash
just serve         # Build + npx serve site (static server en :8000)
just serve-dev     # MkDocs dev server con live-reload
just link-rules    # Crear/refrescar hard links rules/ → docs/rules/
```

### Just — githooks, commits y release

```bash
just hooks-install # Instalar git hooks + bootstrap Commitizen (core.hooksPath)
just commit        # Asistente de commit (Commitizen)
just changelog     # Generar CHANGELOG.md desde Conventional Commits
just version       # Leer/bumpear versión
just prepare-release # Bump + changelog + tag + commit "chore(release): vX.Y.Z"
just cz-init       # Configuración interactiva de Commitizen (para humanos)
```

### Just — secretos

```bash
just keygen              # age-keygen -o ~/.age/<proyecto>-key.txt
just edit-secrets dev    # sops edit .secrets/secrets.dev.enc.yaml
just env dev             # Generar .env.dev desde secrets.dev.enc.yaml
just secrets-verify      # gitleaks git --staged
```

El sitio se publica con [.github/workflows/static.yml](.github/workflows/static.yml) (wrapper: `make validate` + `make docs` → Pages). `[site/](site)` y `mcp/.venv/` no se versionan.

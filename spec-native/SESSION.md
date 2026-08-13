# SESSION

## Estado de trabajo — 2026-08-13

Última iniciativa activa: iteraciones incrementales sobre el estándar Ether Best Practices
(repo de reglas + templates + MCP). Todo el trabajo se commitea a `main` con Conventional Commits.

## Objetivo del repositorio

- **`rules/`** (16 reglas con frontmatter YAML + bloques tipados) y **`templates/`** son el objetivo:
  definiciones que agentes de IA consumen para generar proyectos consistentes.
- Lo demás (`helpers/`, `.config/`, `mcp/`, `Makefile`, `Justfile`, `.github/`) es infraestructura
  operativa del propio repositorio.

## Arquitectura clave (estable)

- **Taxonomía de 14 bloques tipados** en reglas: `Premisa`, `Restriccion`, `Ejemplo`, `Referencia`
  (obligatorios) + `Estructura`, `Diagrama`, `Comando`, `Nombre Sugerido`, `Plantilla`,
  `Comportamiento`, `Sugerencia`, `Flujo`, `Contrato`, `Matriz` (opcionales).
- **Compilador de reglas** `helpers/python/rules_compiler.py` (AST determinista): `--action parse|validate|render|new`.
  Definición interna en `rules/.config/RULES_COMPILER.md` (no expuesta).
- **`validate-rules.sh`** es wrapper bash que delega en el compilador.
- **Convención `_draft`**: reglas Borrador usan `NN-topic_draft.md` + `— ⚠️ *Borrador*` en H1.
  Actualmente en Borrador: 02-architecture, 03-testing, 04-documentation, 05-version-control.
- **Makefile = construcción** (`-include helpers/mk/*.mk`); **Justfile = task manager** (`import helpers/just/*.just`),
  NO proxy pass. Default = `help`/`--list`.
- **Scripts atómicos** en `helpers/shell/` + libs comunes en `helpers/{shell,python}/lib/` (regla 15).

## Cambios recientes (últimos commits)

1. `c117756` — Variables de entorno `.enviroments/` + symlink `.env` + merge secretos→variables (regla 13).
2. `5660b38` — Formatters (markdownlint-cli2/mdformat) + tags de relación entre docs (regla 04, mkdocs-macros).
3. `1d059d5` — Gestión de git worktrees (regla 05 + worktree.sh/just).
4. `cfd564b` — Cross-compilación en contenedores + QEMU (regla 06 + cross.sh).
5. `2b56da7` — Convención `_draft` para reglas Borrador (visual, MCP, auditoría).
6. `8ea9fd3` — Auditoría de adopción `audit_project` (MCP tool + audit.py CLI).
7. `ba6b2ac` — Release v0.3.0 (MCP wheel + checksum).

## MCP (servidor `ether-rules`)

- `mcp/ether_mcp_my_best_practices/` — paquete Python instalable (`uvx ether-mcp`).
- Resources (7), Tools (10 incl. `audit_project`, `scaffold_project`, `check_project`), Prompts (5).
- Estrategia de datos: env `MCP_ROOT` → web (`/ether-rules/`) → bundled (`data/`).
- Instalador `helpers/shell/mcp-install.sh` (Claude/Codex/opencode, checksum, idempotente).
- Release local: `just prepare-release` (bump) + `make package` + `make release` → GitHub Release.

## Comandos principales

```bash
make validate        # wrapper → rules_compiler.py --action validate --all
make lint            # bash -n + py_compile + markdownlint
make docs            # mkdocs build (docs_dir/site_dir ../../)
make link-rules      # hard links rules/ → docs/rules/
just prepare-release # bump version + changelog + tag (Commitizen)
just app             # levantar MCP
```

## Pendientes / próximos pasos

- Reglas 02-05 siguen en Borrador; elevarlas a Definida conforme se completen (worktrees, formatters ya añadidos a 04/05).
- `mkdocs-macros-plugin` (regla 04) documentado como snippet estático — falta integrarlo en un proyecto consumidor real.
- `cross.sh` (regla 06) y `worktree.sh`/`env.sh` son solo templates — verificar en proyecto consumidor.
- Verificar `make lint` incluye markdownlint-cli2 en CI del proyecto consumidor (no este repo).

## Notas

- `docs/rules/` son hard links (generados con `make link-rules`), no editar a mano.
- `site/`, `mcp/dist/`, `.venv/`, `_build.py`, `data/` no se versionan.

# Changelog

## [0.1.0] — 2026-08-07

### Added

- Initial release: estructura de reglas con frontmatter YAML y secciones unificadas.
- Regla 01: Herramientas de Construcción (Makefile, Justfile, helpers por lenguaje).
- Regla 02: Arquitectura Hexagonal.
- Regla 03: Estrategias de Testing y TDD.
- Regla 04: Documentación como Código (Markdown + MermaidJS + MkDocs).
- Regla 05: Control de Versiones (Git, Conventional Commits).
- Regla 06: Integración y Despliegue Continuo (CI).
- Regla 07: Agentes de IA y Model Context Protocol (MCP).
- Regla 08: Stack Tecnológico Recomendado.
- Regla 09: Estructura de Repositorio (monorepo multi-lenguaje por rol).
- Regla 10: Git Hooks (gates de lint/test/commit-msg y flujo de release).
- Templates reutilizables: Makefile, Justfile, helpers shell, Containerfile, project-structure.
- Validador de reglas con frontmatter YAML y secciones obligatorias.
- Dogfooding: MermaidJS en este sitio, Python 3.12 en CI.

## v0.2.0 (2026-08-09)

### Feat

- **rules**: sistema de bloques tipados + compilador de reglas (AST)
- **cd**: separar CI de CD + nueva regla 16-cd.md (CD portable, local-first)
- **cd**: empaquetar MCP como paquete distribuible + pipeline de release
- **mcp**: servidor MCP ether-rules con resources, tools y prompts
- add docs rules mirroring and mkdocs serve helpers
- move config files under .config and update templates
- add secrets management rule and SOPS templates
- add gitignore rule to index
- add gitignore template library
- reorganize repository structure templates
- add commitizen rule and container templates
- add githooks rule and scaffolding templates
- extend repository structure templates
- update docs, rules, and container templates

### Fix

- **release**: alinear versiones a 0.1.0, añadir __init__.py a version_files
- **cd**: corregir orquestación Makefile/Justfile — deploy compuesto, sin script→script
- **mcp**: cobertura completa de templates y match exacto de reglas

### Refactor

- capa completa helpers/mk/ + helpers/just/, scripts delegados, pre-commit
- **mcp**: mover servidor MCP a raíz del repositorio
- crear librerías comunes (lib/) y migrar helpers a máxima reutilización
- simplify build orchestration

---
id: documentation
title: Documentación como Código
status: Borrador
tags: [documentation, markdown, mkdocs, adr]
---

# Regla 04: Documentación

## Premisa

La documentación es código. Debe vivir junto al código fuente, versionarse con Git, ser fácil de mantener y generarse como sitio estático con MkDocs. Los diagramas deben ser código versionable: **MermaidJS** embebido en Markdown, no imágenes binarias (PNG, SVG exportado).

> Ver [Regla 08: Stack Tecnológico](08-stack.md) para la elección del stack de documentación.

## Restricciones

- **No mantener documentación fuera del repositorio** (wikis externas, Google Docs, Confluence no versionado).
- **No duplicar información** entre README, docs/ y docstrings. Cada tipo de documento tiene su propósito.
- El directorio `site/` **no se versiona** — se genera en CI y se publica como artefacto.
- Los enlaces entre documentos deben ser relativos y funcionales (el validador los comprueba).

## Ejemplos

### Estructura de documentación

```
docs/
├── index.md              # Portada
├── getting-started.md    # Inicio rápido
├── contributing.md       # Cómo contribuir
├── architecture/         # Documentación técnica
├── api/                  # Referencia de API
└── tutorials/            # Guías paso a paso
```

### Generar y servir

```bash
mkdocs build --site-dir site/
mkdocs serve
```

O con los targets del Makefile:

```bash
make docs             # mkdocs build
make serve            # mkdocs serve (operativa Justfile en proyectos consumidores)
```

### Publicación

Publicar en GitHub Pages a través de CI/CD: workflow genera `site/` y despliega como artefacto.

## Referencias

- [MkDocs](https://www.mkdocs.org/)
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- [mkdocs.yml](../mkdocs.yml)
- [Regla 01: Build Tooling](01-build-tooling.md) — `make docs`, `make serve`
- [Regla 06: CI/CD](06-ci-cd.md) — publicación en Pages
- [templates/helpers/shell/docs.sh.tmpl](../templates/repository-structure/helpers/shell/docs.sh.tmpl)

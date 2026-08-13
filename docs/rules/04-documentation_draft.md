---
id: documentation
title: Documentación como Código
status: Borrador
tags: [documentation, markdown, mkdocs, adr]
---

# Regla 04: Documentación — ⚠️ *Borrador*



### Premisa: Premisa

La documentación es código. Debe vivir junto al código fuente, versionarse con Git, ser fácil de mantener y generarse como sitio estático con MkDocs. Los diagramas deben ser código versionable: **MermaidJS** embebido en Markdown, no imágenes binarias (PNG, SVG exportado).

> Ver [Regla 08: Stack Tecnológico](08-stack.md) para la elección del stack de documentación.

tags: [obligatorio]

### Restriccion: Restricciones

- **No mantener documentación fuera del repositorio** (wikis externas, Google Docs, Confluence no versionado).
- **No duplicar información** entre README, docs/ y docstrings. Cada tipo de documento tiene su propósito.
- El directorio `site/` **no se versiona** — se genera en CI y se publica como artefacto.
- Los enlaces entre documentos deben ser relativos y funcionales (el validador los comprueba).

tags: [obligatorio]

### Ejemplo: Ejemplos

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

Publicar en GitHub Pages a través de CI: workflow genera `site/` y despliega como artefacto.

tags: [obligatorio]

### Comportamiento: Frontmatter, tags y relación entre documentos

Todo documento en `docs/` lleva frontmatter YAML que lo describe y lo conecta con el resto de la documentación. Los **tags** son el mecanismo principal para relacionar documentos entre sí, complementados con cross-links manuales.

**Frontmatter altamente recomendado (validado por linter):**
```yaml
---
title: Guía de Autenticación
description: Cómo implementar auth en APIs REST
tags: [api, security, guia]
---
```

**Vocabulario de tags consistente:**
- `api` — referencia de endpoints/contratos.
- `security` — autenticación, autorización, secretos.
- `guia` — guías paso a paso.
- `tutorial` — tutoriales de aprendizaje.
- `referencia` — documentación de referencia.
- `arquitectura` — decisiones de diseño.
- `onboarding` — inicio rápido para nuevos miembros.

**Relación entre documentos vía `mkdocs-macros-plugin`:**
La sección "Documentos relacionados" se genera con un snippet estático (documentado en la regla y en `mkdocs.yml.tmpl`), que agrupa los documentos que comparten el mismo tag. Se complementa con cross-links manuales (`[otro doc](otro.md)`). **Nunca se duplica contenido** — solo se enlaza.

tags: [opcional]

### Comando: Lint y format de documentación

```bash
# Lint de Markdown (markdownlint-cli2) sobre docs/
bash helpers/shell/lint.sh --tool markdown --module docs

# Formateo de Markdown (mdformat) — solo docs/, nunca rules/
bash helpers/shell/format.sh --tool markdown --module docs
```

Los formatters de Markdown se integran en los helpers genéricos multi-herramienta (`lint.sh`/`format.sh`) con la clave `markdown`, de modo que `make lint` y `make format` los incluyan.

tags: [opcional]

### Ejemplo: Documento con frontmatter + documentos relacionados

```markdown
---
title: Guía de Autenticación
description: Implementar auth en APIs REST
tags: [api, security, guia]
---

# Guía de Autenticación

## Documentos relacionados

<!-- Snippet estático de relacionados (mkdocs-macros) -->
{{ related_docs("security") }}
```

El snippet `{{ related_docs("security") }}` (definido como macro estática en el proyecto consumidor) renderiza automáticamente la lista de documentos con el tag `security`.

tags: [obligatorio]

### Restriccion: Restricciones de formatters y tags

- **Todo `docs/*.md` debe pasar `markdownlint` antes de publicar.** El CI/publicación falla si hay errores de lint.
- **Todo documento debe tener `tags` en su frontmatter.** La ausencia de `tags` produce un warning del linter.
- **`mdformat` y `markdownlint` aplican SOLO a `docs/`.** Nunca a `rules/` — los bloques tipados de las reglas no deben ser reordenados ni reformateados por herramientas genéricas.
- **Los tags son el mecanismo de relación** entre documentos; usar macros + cross-links, nunca duplicar contenido entre documentos.

tags: [obligatorio]

### Referencia: Referencias

- [MkDocs](https://www.mkdocs.org/)
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/) — documentos relacionados por tag
- [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) — lint de Markdown
- [mdformat](https://github.com/executablebooks/mdformat) — format de Markdown
- [mkdocs.yml](../.config/mkdocs/mkdocs.yml)
- [Regla 01: Build Tooling](01-build-tooling.md) — `make docs`, `make serve`
- [Regla 06: CI](06-ci.md) — publicación en Pages
- [templates/helpers/shell/docs.sh.tmpl](../templates/repository-structure/helpers/shell/docs.sh.tmpl)
- [templates/helpers/shell/lint.sh.tmpl](../templates/repository-structure/helpers/shell/lint.sh.tmpl)
- [templates/helpers/shell/format.sh.tmpl](../templates/repository-structure/helpers/shell/format.sh.tmpl)

tags: [obligatorio]

### Plantilla: Plantillas de documentación

- [templates/repository-structure/.config/mkdocs/mkdocs.yml.tmpl](../templates/repository-structure/.config/mkdocs/mkdocs.yml.tmpl)
- [templates/repository-structure/.config/mkdocs/requirements.txt.tmpl](../templates/repository-structure/.config/mkdocs/requirements.txt.tmpl)
- [templates/repository-structure/helpers/shell/docs.sh.tmpl](../templates/repository-structure/helpers/shell/docs.sh.tmpl)
- [templates/repository-structure/helpers/shell/lint.sh.tmpl](../templates/repository-structure/helpers/shell/lint.sh.tmpl)
- [templates/repository-structure/helpers/shell/format.sh.tmpl](../templates/repository-structure/helpers/shell/format.sh.tmpl)

tags: [opcional]

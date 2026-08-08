# AGENTS

## Propósito

Este repositorio mantiene reglas de mejores prácticas para APIs REST, documentación MkDocs y plantillas reutilizables pensadas para que agentes de IA puedan entender las reglas y generar cascarones de proyecto consistentes. Antes de proponer o aplicar cambios, usa como fuentes principales:

- [README.md](README.md)
- [docs/getting-started.md](docs/getting-started.md)
- [docs/contributing.md](docs/contributing.md)
- [rules/00-index.md](rules/00-index.md)
- [rules/07-agents-mcp.md](rules/07-agents-mcp.md)

## Qué editar

- Edita contenido fuente en [rules](rules), [docs](docs), [templates](templates), [helpers](helpers) y [mkdocs.yml](mkdocs.yml).
- No edites [site](site) manualmente. Es salida generada.
- Trata los archivos en [templates](templates) como plantillas genéricas y cascarones para proyectos consumidores. No conviertas placeholders en decisiones específicas de un proyecto consumidor.

## Convenciones del repositorio

- Las reglas viven en [rules](rules) con formato `NN-topic.md`.
- Toda regla distinta de [rules/00-index.md](rules/00-index.md) debe incluir frontmatter YAML (`id`, `title`, `status`, `tags`) y un `#` principal.
- Secciones obligatorias en toda regla: `## Premisa`, `## Restricciones`, `## Ejemplos`, `## Referencias`.
- Secciones opcionales (whitelist): `## Estructura`, `## Nombres Sugeridos`, `## Comandos`, `## Plantilla`. Las reglas con `status: Definida` requieren `## Comandos` y `## Estructura`.
- Si agregas una regla nueva, usa [templates/rule-template.md.tmpl](templates/rule-template.md.tmpl) como esqueleto. Luego actualiza el índice en [rules/00-index.md](rules/00-index.md) y la navegación en [mkdocs.yml](mkdocs.yml).
- Mantén el contenido y los comentarios en español salvo que un archivo existente requiera otro idioma.
- Conserva enlaces relativos entre reglas y documentación.

## Validación y comprobaciones

- Ejecuta [helpers/shell/validate-rules.sh](helpers/shell/validate-rules.sh) cuando cambies archivos en [rules](rules).
- Si tocas navegación o páginas de documentación, valida también con `mkdocs build` cuando MkDocs esté disponible en el entorno.
- No asumas que existe un Makefile o un archivo requirements en la raíz del repositorio actual; esos comandos aparecen como plantillas o ejemplos para proyectos consumidores.

## Patrones de cambio

- Al mejorar una regla existente, prioriza claridad, ejemplos correctos y referencias cruzadas útiles.
- Al crear una regla nueva, sigue la numeración existente, usa [templates/rule-template.md.tmpl](templates/rule-template.md.tmpl) y evita renumerar archivos ya publicados.
- Si cambias plantillas de proyecto, mantén coherencia con la estructura hexagonal descrita en [templates/repository-structure/README.md](templates/repository-structure/README.md) y en [rules/02-architecture.md](rules/02-architecture.md).
- Si modificas guía para agentes o MCP, mantén alineación con [rules/07-agents-mcp.md](rules/07-agents-mcp.md).
- Si el cambio afecta cómo un agente genera una API REST, ajusta tanto la regla aplicable como el template relacionado para que intención y cascarón no diverjan.

## Riesgos a evitar

- No rompas enlaces locales a otros archivos `NN-*.md`.
- No elimines referencias del índice central sin actualizar el resto de la documentación.
- No presentes como automatización real los placeholders de build, test, lint o format dentro de las plantillas.
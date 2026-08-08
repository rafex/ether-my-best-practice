# Contribuyendo

¡Las contribuciones son bienvenidas! Aquí te indicamos cómo hacerlo.

## Proceso

1. **Fork** el repositorio
2. Crea una **rama feature**: `git checkout -b feature/my-rule`
3. Haz commits con mensajes claros:
   ```bash
   git commit -m "feat: add rule for XYZ"
   git commit -m "docs: improve architecture section"
   ```
4. **Push** a tu fork
5. **Pull Request** con descripción clara

## Estilo de Contribución

### Estructura de una regla

Toda regla (`rules/NN-topic.md`) usa frontmatter YAML y un conjunto fijo de secciones:

```yaml
---
id: nn-topic
title: Título descriptivo
status: Borrador          # Definida | Borrador
tags: [tag1, tag2]
---
```

**Secciones obligatorias** (el validador falla si faltan):
- `## Premisa` — por qué existe esta regla.
- `## Restricciones` — qué **NO** hacer (prohibiciones explícitas).
- `## Ejemplos` — al menos un bloque de código correcto.
- `## Referencias` — enlaces a templates, otras reglas, fuentes externas.

**Secciones opcionales** (requeridas cuando `status: Definida`):
- `## Estructura` — tree de directorios/archivos.
- `## Comandos` — comandos canónicos que un agente debe usar.
- `## Nombres Sugeridos` — convenciones de naming.
- `## Plantilla` — enlace a los templates asociados.

Usa [templates/rule-template.md.tmpl](../templates/rule-template.md.tmpl) como punto de partida. Ejecuta `bash helpers/shell/validate-rules.sh` para validar la estructura antes de commitear.

### Nuevas Reglas

Si agregas una nueva regla:

1. Crear archivo `rules/NN-topic.md`
2. Seguir formato de reglas existentes
3. Actualizar `rules/00-index.md`
4. Agregar referencias cruzadas si aplica

### Mejoras a Reglas Existentes

- Clarificar ejemplos
- Agregar references
- Corregir errores o desactualización

### Plantillas

- Mantener genéricas y reutilizables
- Incluir comentarios de uso
- Documentar qué debe adaptarse

## Estándares de Código

- Markdown bien formateado
- Títulos jerárquicos coherentes
- Ejemplos de código correctos y testados
- Enlaces funcionales

## Reportar Problemas

Abre un **Issue** si:
- Encuentras errores en las reglas
- Una práctica no funciona en tu caso
- Tienes sugerencias de mejora

## Licencia

Al contribuir, aceptas que tu código se publique bajo MIT License.

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

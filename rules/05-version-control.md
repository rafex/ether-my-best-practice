# Regla 05: Control de Versiones

## Premisa

Git es el estándar. Mensajes de commit claros y convencionales facilitan el mantenimiento.

## Git Flow

```
main (production)
  ↑
  ├─ release/v1.2.0 (preparar release)
  │
develop (integración)
  ↑
  ├─ feature/new-feature (desarrollo)
  ├─ bugfix/issue-123 (correcciones)
  └─ hotfix/critical-fix (a partir de main)
```

## Convención de Commits

Usar **Conventional Commits**:

```
type(scope): description

[optional body]

[optional footer]
```

### Tipos

- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formateo (sin cambiar lógica)
- `refactor`: Reorganización de código
- `test`: Agregar o actualizar tests
- `chore`: Tareas de mantenimiento

### Ejemplos

```
feat(auth): add JWT token validation
fix(api): handle null pointer in user service
docs: update installation guide
```

## Branching

- Nombres en minúsculas con guiones: `feature/user-authentication`
- Borrar branches una vez merged
- Requiere code review antes de merge

## Etiquetas (Tags)

```
git tag -a v1.2.0 -m "Release 1.2.0"
git push origin v1.2.0
```

Formato: `v{MAJOR}.{MINOR}.{PATCH}` (Semantic Versioning)

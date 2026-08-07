# Regla 01: Herramientas de Construcción

## Premisa

Todo proyecto debe tener un sistema de construcción declarativo y reproducible, independientemente del lenguaje.

## Herramientas Recomendadas

### Makefile
- Clásica, universal, disponible en prácticamente todos los sistemas
- Ideal para tareas simple
- Usar para: build, test, clean, deploy

### Justfile
- Sintaxis más moderna que Makefile
- Mejor para proyectos complejos
- Reemplaza Makefile gradualmente

### npm scripts / cargo / gradle / maven
- Usar cuando sea nativo del ecosistema del proyecto

## Estructura Mínima

Todo proyecto debe tener:
```
make build    # Construir
make test     # Ejecutar tests
make clean    # Limpiar artefactos
make docs     # Generar documentación
```

## Plantilla

Ver `templates/Makefile.tmpl` y `templates/Justfile.tmpl`

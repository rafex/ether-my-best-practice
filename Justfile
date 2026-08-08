# Tareas operativas del repositorio ether-my-best-practice.
# Las tareas de build/artefactos pertenecen al Makefile.
# Justfile -> Makefile está permitido; Makefile -> Justfile, no.

# Mostrar tareas disponibles
@default:
    just --list

# Validar estructura y enlaces de las reglas
@validate:
    make validate

# Validar estilo de reglas y documentación
@lint:
    make lint

# Formatear reglas y documentación
@format:
    make format

# Generar sitio MkDocs
@docs:
    make docs

# Generar y publicar sitio (vía Makefile)
@pages-build:
    make pages-build

# Disparar workflow de GitHub Pages
@pages:
    make pages

# Servir documentación localmente
@serve:
    make serve

# Limpiar sitio generado
@clean:
    make clean

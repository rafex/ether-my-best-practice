# Justfile — Operativas del repositorio.
# Las tareas se organizan en helpers/just/*.just:
#   app.just        → levantar la aplicación (el MCP)
#   repository.just → operativas del repositorio
# Build/artefactos → Makefile (helpers/mk/*.mk)

import 'helpers/just/app.just'
import 'helpers/just/repository.just'

# Mostrar tareas disponibles
@default:
    just --list

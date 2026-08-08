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

# Disparar workflow de GitHub Pages (compartido con Makefile vía helpers/shell/github.sh)
@pages:
    bash helpers/shell/github.sh --action workflow-run --workflow static.yml --ref main

# Servir documentación localmente (repositorio de docs, LANG=docs implícito)
@serve:
    mkdocs serve

# Limpiar sitio generado
@clean:
    make clean

# Instalar git hooks (core.hooksPath → .githooks)
@hooks-install:
    bash helpers/shell/hooks.sh --action install

# Leer o bumpear VERSION (release-time, no hook)
@version bump="" lang="" tool="" module="" profile="" skip_tests="" app_justfile="" just_dir="":
    uv run python helpers/python/version.py {{if bump=="" { "" } else { "--bump " + bump } }}

# Generar CHANGELOG.md desde Conventional Commits (release-time)
@changelog lang="" tool="" module="" profile="" skip_tests="" app_justfile="" just_dir="":
    uv run python helpers/python/changelog.py

# Preparar para release: version + changelog + commit + tag + push
@prepare-release version lang="" tool="" module="" profile="" skip_tests="" app_justfile="" just_dir="":
    uv run python helpers/python/version.py --version {{version}}
    uv run python helpers/python/changelog.py
    git add VERSION CHANGELOG.md
    git commit -m "chore(release): v{{version}}"
    git tag -a v{{version}} -m "Release v{{version}}"
    git push origin v{{version}}

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

# Gestión de secretos (regla 13): generar clave age
@keygen:
    bash helpers/shell/secrets.sh --action keygen

# Editar secretos cifrados con sops+age (abre vi, encripta al guardar)
@edit-secrets env:
    bash helpers/shell/secrets.sh --action edit --env {{env}}

# Generar .env.<env> desde secretos cifrados
@env env:
    bash helpers/shell/secrets.sh --action env --env {{env}}

# Verificar que no hay secretos en plano staged
@secrets-verify:
    bash helpers/shell/secrets.sh --action verify

# Instalar git hooks + bootstrap Commitizen en venv interno
@hooks-install:
    bash helpers/shell/hooks.sh --action install

# Asistente interactivo de commit (Commitizen)
@commit:
    bash helpers/shell/cz.sh --action commit

# Generar CHANGELOG.md (Commitizen)
@changelog:
    bash helpers/shell/cz.sh --action changelog

# Leer o bumpear VERSION (Commitizen)
@version bump="":
    bash helpers/shell/cz.sh --action version {{if bump=="" { "" } else { "--bump " + bump } }}

# Preparar release: bump version + changelog + tag + commit (Commitizen)
@prepare-release:
    bash helpers/shell/cz.sh --action bump

# Configuración interactiva de Commitizen (cz init)
# Para agentes de IA: editar pyproject.toml con [tool.commitizen] (ver templates/repository-structure/pyproject.toml.tmpl).
@cz-init:
    bash helpers/shell/cz.sh --action init

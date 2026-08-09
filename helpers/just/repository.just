# repository.just — Operativas del repositorio.
# Las tareas de build/construcción pertenecen al Makefile (vía helpers/mk/).
# Justfile → Makefile está permitido; Makefile → Justfile, no.

# --- Construcción (delegado a Makefile) ---
@validate:
    make validate

@lint:
    make lint

@format:
    make format

@docs:
    make docs

@link-rules:
    make link-rules

@pages:
    make pages

@pages-build:
    make pages-build

@clean:
    make clean

# --- Desarrollo local ---
@serve-dev:
    mkdocs serve -f .config/mkdocs/mkdocs.yml

# --- Secretos (regla 13) ---
@keygen:
    bash helpers/shell/secrets.sh --action keygen

@edit-secrets env:
    bash helpers/shell/secrets.sh --action edit --env {{env}}

@env env:
    bash helpers/shell/secrets.sh --action env --env {{env}}

@secrets-verify:
    bash helpers/shell/secrets.sh --action verify

# --- Git hooks (regla 10) ---
@hooks-install:
    bash helpers/shell/hooks.sh --action install

# --- Commitizen (regla 11) ---
@commit:
    bash helpers/shell/cz.sh --action commit

@changelog:
    bash helpers/shell/cz.sh --action changelog

@version bump="":
    bash helpers/shell/cz.sh --action version {{if bump=="" { "" } else { "--bump " + bump } }}

@prepare-release:
    bash helpers/shell/cz.sh --action bump

@cz-init:
    bash helpers/shell/cz.sh --action init

---
id: config-files
title: Archivos de Configuración (.config)
status: Definida
tags: [config, dotfiles, organization, tools, structure]
---

# Regla 14: Archivos de Configuración (.config)

## Premisa

Todos los archivos de configuración de herramientas del proyecto se concentran en una carpeta `.config/` en la raíz del repositorio, organizados por subcarpeta según el dominio, producto o herramienta: `.config/<herramienta>/archivo`. Ningún archivo de configuración suelto debe quedar en la raíz. Cada herramienta (`mkdocs`, `commitizen`, `sops`) conoce la ruta de su configuración mediante flags explícitos (`-f`, `--config`), resolviendo la ruta desde `ROOT=$(pwd)` con fallback a ruta relativa.

## Estructura

### Árbol de `.config/`

```
.config/
├── commitizen/
│   └── pyproject.toml           # [tool.commitizen] con version_files
├── mkdocs/
│   ├── mkdocs.yml               # configuración del sitio
│   └── requirements.txt         # dependencias (pip install)
└── sops/
    └── .sops.yaml               # creation_rules con age recipients
```

> Las subcarpetas pueden crecer al agregar más herramientas (ej. `.config/eslint/`, `.config/husky/`, `.config/terraform/`).

### Cómo cada herramienta localiza su configuración

| Herramienta | Flag | Ruta de configuración |
|---|---|---|
| **MkDocs** | `-f` / `--config-file` | `.config/mkdocs/mkdocs.yml` |
| **Commitizen** | `--config` | `.config/commitizen/pyproject.toml` |
| **SOPS** | `--config` / `-c` | `.config/sops/.sops.yaml` |
| **pip** (MkDocs deps) | `-r` | `.config/mkdocs/requirements.txt` |

### Resolución de rutas

Los helpers (`cz.sh`, `secrets.sh`, `Makefile`) usan la variable `ROOT=$(pwd)`:
1. Intentan `$ROOT/.config/<herramienta>/archivo`.
2. Fallback: ruta relativa `.config/<herramienta>/archivo` (funciona si el CWD es la raíz del repo).
3. Si ninguna existe, usan la búsqueda por defecto de la herramienta.

## Comandos

### MkDocs

```bash
mkdocs build -f .config/mkdocs/mkdocs.yml --site-dir site
mkdocs serve -f .config/mkdocs/mkdocs.yml
pip install -r .config/mkdocs/requirements.txt
```

### Commitizen

```bash
cz --config .config/commitizen/pyproject.toml commit
cz --config .config/commitizen/pyproject.toml bump
cz --config .config/commitizen/pyproject.toml version
cz --config .config/commitizen/pyproject.toml changelog
```

### SOPS

```bash
sops --config .config/sops/.sops.yaml edit .secrets/secrets.dev.enc.yaml
sops --config .config/sops/.sops.yaml decrypt .secrets/secrets.dev.enc.yaml
```

### Verificar con Makefile y Justfile

```bash
make docs                    # → mkdocs build -f .config/mkdocs/mkdocs.yml
just serve                   # → mkdocs serve -f .config/mkdocs/mkdocs.yml
just commit                  # → cz --config .config/commitizen/pyproject.toml commit
just edit-secrets dev        # → sops --config .config/sops/.sops.yaml edit ...
```

## Ejemplos

### Configuración de Commitizen en `.config/commitizen/pyproject.toml`

```toml
[tool.commitizen]
name = "cz_conventional_commits"
version = "0.1.0"
version_provider = "commitizen"
version_scheme = "pep440"
tag_format = "v$version"
version_files = [
    "pyproject.toml:version",
    "../../VERSION",
    "../../Cargo.toml:version",
    "../../package.json:version",
]
update_changelog_on_bump = true
changelog_file = "../../CHANGELOG.md"
bump_message = "chore(release): v$new_version"
```

> Las rutas en `version_files` y `changelog_file` son relativas al archivo de configuración (`.config/commitizen/`). Para alcanzar la raíz del repo, se usa `../../`.

### Configuración de MkDocs en `.config/mkdocs/mkdocs.yml`

```yaml
site_name: Mi Proyecto
docs_dir: ../../docs
site_dir: ../../site

theme:
  name: material
  language: es

nav:
  - Inicio: index.md
  - Reglas:
      - Índice: ../../rules/00-index.md
```

> `docs_dir` y `site_dir` son relativos al archivo de configuración. La navegación se resuelve relativa a `docs_dir`.

### Resolución de ROOT en `cz.sh`

```bash
ROOT="$(pwd)"
CZ_CONFIG="${ROOT}/.config/commitizen/pyproject.toml"
if [[ -f "$CZ_CONFIG" ]]; then
    use_config="$CZ_CONFIG"
elif [[ -f ".config/commitizen/pyproject.toml" ]]; then
    use_config=".config/commitizen/pyproject.toml"
fi
# Usar con: cz --config "$use_config" <comando>
```

## Restricciones

- **Ningún archivo de configuración suelto en la raíz.** Todo archivo de configuración de herramienta vive en `.config/<herramienta>/`.
- **Una subcarpeta por herramienta.** Commitizen tiene su propia subcarpeta, MkDocs la suya, SOPS la suya. No mezclar configuraciones de herramientas distintas en la misma subcarpeta.
- **Los archivos de configuración se versionan** (contienen reglas públicas, no secretos). La excepción son los valores de secretos: nunca van en `.config/`, van en `.secrets/` cifrados con sops+age ([regla 13](13-secrets.md)).
- **Las rutas dentro de las configuraciones son relativas al archivo de configuración.** Por ejemplo, `version_files` en Commitizen y `docs_dir` en MkDocs usan rutas relativas al directorio del config.
- **Los helpers (`cz.sh`, `secrets.sh`, `Makefile`) son responsables de pasar el flag de configuración explícito** a cada herramienta (resolviendo desde `ROOT`).
- **Si la ruta de configuración cambia, se actualizan tanto el helper como la referencia en esta regla y en los templates.**
- **La estructura `.config/` escala** al agregar nuevas herramientas sin romper las existentes.

## Referencias

- [Regla 01: Build Tooling](01-build-tooling.md) — helpers como capa única de ejecución.
- [Regla 09: Estructura de Repositorio](09-repository-structure.md) — `.config/` en el árbol del proyecto.
- [Regla 11: Commitizen](11-commitizen.md) — `pyproject.toml` en `.config/commitizen/`.
- [Regla 13: Gestión de Secretos](13-secrets.md) — `.sops.yaml` en `.config/sops/`.
- [templates/repository-structure/.config/](../templates/repository-structure/.config/) — espejo de la estructura en templates.
- [templates/repository-structure/.config/commitizen/pyproject.toml.tmpl](../templates/repository-structure/.config/commitizen/pyproject.toml.tmpl)
- [templates/repository-structure/.config/mkdocs/mkdocs.yml.tmpl](../templates/repository-structure/.config/mkdocs/mkdocs.yml.tmpl)
- [templates/repository-structure/.config/sops/.sops.yaml.tmpl](../templates/repository-structure/.config/sops/.sops.yaml.tmpl)

## Plantilla

- [templates/repository-structure/.config/commitizen/pyproject.toml.tmpl](../templates/repository-structure/.config/commitizen/pyproject.toml.tmpl)
- [templates/repository-structure/.config/mkdocs/mkdocs.yml.tmpl](../templates/repository-structure/.config/mkdocs/mkdocs.yml.tmpl)
- [templates/repository-structure/.config/mkdocs/requirements.txt.tmpl](../templates/repository-structure/.config/mkdocs/requirements.txt.tmpl)
- [templates/repository-structure/.config/sops/.sops.yaml.tmpl](../templates/repository-structure/.config/sops/.sops.yaml.tmpl)

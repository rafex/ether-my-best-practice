---
id: ci-cd
title: Integración y Despliegue Continuo
status: Definida
tags: [ci, cd, pipeline, deployment, github-actions, containers]
---

# Regla 06: CI/CD

## Premisa

Toda integración y despliegue debe ser automatizado, repetible y declarativo. La base de CI debe ser auto-suficiente dentro del repositorio: primero pipeline local en contenedor, luego integración externa (GitHub Actions, GitLab CI, Jenkins) como envoltura opcional.

> **Nota:** esta regla describe el pipeline de **proyectos consumidores** generados desde [templates/](../templates/). El workflow real de este repositorio ([.github/workflows/static.yml](../.github/workflows/static.yml)) es un ejemplo de CI para publicar el sitio de documentación con MkDocs y GitHub Pages.

## Estructura

### Pipeline base

```
Commit → Build Image → Build/Test en Contenedor → Artefactos → Release
```

### Fases

```
1. Build Image → make image        (construye imagen de CI con toolchain fijo)
2. Build       → make build        (compila/construye, resuelve dependencias)
3. Test        → make test         (unit + integration + coverage)
4. Analysis    → sonar-scanner     (opcional: calidad de código, vulnerabilidades)
5. Deploy      → make deploy       (dev → staging → producción)
6. Documentation → mkdocs build    (publicar a GitHub Pages)
```

### Runtime de contenedor (detección automática)

```
podman (preferido) → docker → fallar con mensaje de instalación
```

### Estructura del repo (artefactos CI)

```
proyecto/
├── Makefile
├── Dockerfile.ci         # Imagen de CI con toolchain
├── .github/workflows/
│   └── ci.yml           # Wrapper: invoca make ci
├── src/
├── target/              # Artefactos generados
├── dist/
└── site/                # Sitio MkDocs (no trackeado)
```

## Comandos

### Pipeline local (auto-suficiente)

```bash
make image                       # Construir imagen de CI
make ci                          # Ejecutar build+test en contenedor
```

### Por fase

```bash
make build                       # Compilar/construir
make test                        # Unit + integration + coverage
make deploy                      # Deploy a ambiente
make docs                        # Generar sitio de documentación
```

### Runtime

```bash
make runtime                     # Detectar podman | docker
```

### Publicación

```bash
make pages-build                 # Validar + generar sitio
make pages                       # Disparar workflow de GitHub Pages
```

## Ejemplos

### GitHub Actions como wrapper (invoca targets existentes del Makefile)

```yaml
name: CI/CD

on: [push, pull_request]

jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build CI Image
        run: make image
      - name: Run Containerized CI
        run: make ci
```

### CI local en un paso

```bash
make image
make ci
```

### Publicación en GitHub Pages (wrapper)

```yaml
- name: Build Docs
  run: mkdocs build
- name: Deploy
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./site
```

## Restricciones

- **No depender de runners remotos** para validar la construcción. El pipeline local (`make ci`) debe funcionar en cualquier máquina con `podman` o `docker`.
- **No duplicar lógica** en los archivos de CI externa. GitHub Actions, GitLab CI o Jenkins deben ser **wrappers que invocan targets del Makefile** (`make ci`, `make docs`, `make deploy`), nunca reescribir la lógica de build.
- **Detectar runtime obligatoriamente:** `podman` → `docker`. Si ninguno existe, el pipeline debe fallar con mensaje claro y sugerir instalación.
- **No trackear artefactos generados** en el repositorio (`site/`, `target/`, `dist/`, `build/`).
- **El workflow debe ser declarativo** y ejecutable localmente sin configuración adicional de CI remoto.

## Referencias

- [Regla 01: Build Tooling](01-build-tooling.md) — `make image`, `make ci`, `make build`, `make test`
- [.github/workflows/static.yml](../.github/workflows/static.yml) — ejemplo de wrapper para GitHub Pages
- [templates/Makefile.tmpl](../templates/Makefile.tmpl) — targets `runtime`, `image`, `ci`
- [templates/helpers/mk/container.mk.tmpl](../templates/helpers/mk/container.mk.tmpl)
- [templates/helpers/shell/container.sh.tmpl](../templates/helpers/shell/container.sh.tmpl)

## Plantilla

- [templates/helpers/mk/container.mk.tmpl](../templates/helpers/mk/container.mk.tmpl)
- [templates/helpers/shell/container.sh.tmpl](../templates/helpers/shell/container.sh.tmpl)

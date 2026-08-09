---
id: ci
title: Integración Continua
status: Definida
tags: [ci, pipeline, build, test, containers, github-actions]
---

# Regla 06: Integración Continua



### Premisa: Premisa

Toda integración debe ser automatizada, repetible y declarativa. La base de CI debe ser auto-suficiente dentro del repositorio: primero pipeline local en contenedor, luego integración externa (GitHub Actions, GitLab CI, Jenkins) como envoltura opcional que solo **parametriza** variables.

> **Nota:** esta regla describe el pipeline de **Integración Continua** para proyectos consumidores. El **Despliegue Continuo** (CD portable, local-first, con sops+age) se define en la [Regla 16: CD](16-cd.md). El workflow real de este repositorio ([.github/workflows/static.yml](../.github/workflows/static.yml)) es un ejemplo de CI para publicar el sitio de documentación.

tags: [obligatorio]

### Estructura: Estructura

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
podman (preferido) → docker (con warning) → fallar con mensaje de instalación
```

El helper `container.sh` emite un warning cuando detecta Docker: *"Docker detectado. Podman es la opción recomendada según la regla 08-stack."*

### Estructura del repo (artefactos CI)

```
proyecto/
├── Makefile
├── Containerfile.ci      # Imagen de CI con toolchain
├── .github/workflows/
│   └── ci.yml           # Wrapper: invoca make ci
├── src/
├── target/              # Artefactos generados
├── dist/
└── site/                # Sitio MkDocs (no trackeado)
```

tags: [opcional]

### Comando: Comandos

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

tags: [opcional]

### Ejemplo: Ejemplos

### GitHub Actions como wrapper (invoca targets existentes del Makefile)

```yaml
name: CI

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

tags: [obligatorio]

### Restriccion: Restricciones

- **No depender de runners remotos** para validar la construcción. El pipeline local (`make ci`) debe funcionar en cualquier máquina con `podman` o `docker`.
- **No duplicar lógica** en los archivos de CI externa. GitHub Actions, GitLab CI o Jenkins deben ser **wrappers/parametrizadores que invocan targets del Makefile** (`make ci`, `make docs`) e inyectan variables. Nunca reescribir la lógica de build ni ser dueños de secretos de la aplicación.
- **Detectar runtime obligatoriamente:** `podman` → `docker`. Si ninguno existe, el pipeline debe fallar con mensaje claro y sugerir instalación.
- **No trackear artefactos generados** en el repositorio (`site/`, `target/`, `dist/`, `build/`).
- **El workflow debe ser declarativo** y ejecutable localmente sin configuración adicional de CI remoto.

tags: [obligatorio]

### Referencia: Referencias

- [Regla 01: Build Tooling](01-build-tooling.md) — `make image`, `make ci`, `make build`, `make test`
- [Regla 08: Stack Tecnológico](08-stack.md) — Containerfile, podman, imágenes base
- [Regla 16: Despliegue Continuo](16-cd.md) — CD portable, local-first, sops+age
- [.github/workflows/static.yml](../.github/workflows/static.yml) — ejemplo de wrapper parametrizador para GitHub Pages
- [templates/Makefile.tmpl](../templates/repository-structure/Makefile.tmpl) — targets `runtime`, `image`, `ci`
- [templates/helpers/mk/container.mk.tmpl](../templates/repository-structure/helpers/mk/container.mk.tmpl)
- [templates/helpers/shell/container.sh.tmpl](../templates/repository-structure/helpers/shell/container.sh.tmpl)

tags: [obligatorio]

### Plantilla: Plantilla

- [templates/helpers/mk/container.mk.tmpl](../templates/repository-structure/helpers/mk/container.mk.tmpl)
- [templates/helpers/shell/container.sh.tmpl](../templates/repository-structure/helpers/shell/container.sh.tmpl)

tags: [opcional]

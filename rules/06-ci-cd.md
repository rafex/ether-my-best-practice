# Regla 06: CI/CD

## Premisa

Toda integración y despliegue debe ser automatizado, repetible y declarativo.

La base de CI debe ser auto-suficiente dentro del repositorio: primero pipeline local en contenedor, luego integración externa (GitHub Actions, GitLab CI, Jenkins) como envoltura opcional.

## Pipeline Base (Auto-suficiente)

```
Commit → Build Image → Build/Test en Contenedor → Artefactos → Release
```

Objetivo operativo:

- No depender de runners remotos para validar la construcción.
- Poder ejecutar CI local con `make ci` en cualquier máquina con `podman` o `docker`.
- Generar artefactos reproducibles en rutas estándar (`target/`, `dist/`, `build/`).

## Runtime de Contenedor

El repositorio debe detectar automáticamente:

1. `podman` (preferido si está disponible)
2. `docker`

Si ninguno existe, el pipeline debe fallar con mensaje claro y sugerir instalación del runtime.

## Fases

### 1. Build Image

```bash
make image
```

- Construir imagen de CI (ejemplo `Dockerfile.ci`)
- Fijar toolchain y dependencias

### 2. Build

```bash
make build
```
- Compilar/construir
- Resolver dependencias
- Generar artefactos

### 3. Test

```bash
make test
```
- Unit tests
- Integration tests
- Coverage reports

### 4. Analysis (Opcional)

```bash
sonar-scanner
```
- Análisis de calidad de código
- Detección de vulnerabilidades
- Reporte de deuda técnica

### 5. Deploy

```bash
make deploy
```
- A desarrollo
- A staging
- A producción

### 6. Documentation

```bash
mkdocs build
# Publicar a GitHub Pages
```

## Herramientas

### Makefile + Contenedores (Obligatorio)
- Punto de entrada local y universal para CI
- Ejecución dentro de `podman` o `docker`
- Reproducible sin depender de plataforma externa

### GitHub Actions (Opcional)
- Integrado en GitHub
- YAML declarativo
- Debe invocar targets existentes (`make ci`, `make docs`), no duplicar lógica

### GitLab CI (Opcional)
- Integrado en GitLab
- `.gitlab-ci.yml`

### Jenkins (Opcional)
- Auto-hospedado
- Flexible pero más complejo

## Estructura Mínima de CI Local

```bash
make image
make ci
```

## Ejemplo de Integración GitHub Actions (Wrapper)

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

## Publicación en GitHub Pages

```yaml
- name: Build Docs
  run: mkdocs build
- name: Deploy
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./site
```

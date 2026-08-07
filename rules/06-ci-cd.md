# Regla 06: CI/CD

## Premisa

Toda integración y despliegue debe ser automatizado, repetible y declarativo.

## Pipeline Típico

```
Commit → Build → Test → SonarQube → Deploy → Release
```

## Fases

### 1. Build
```bash
make build
```
- Compilar/construir
- Resolver dependencias
- Generar artefactos

### 2. Test
```bash
make test
```
- Unit tests
- Integration tests
- Coverage reports

### 3. Analysis (Opcional)
```bash
sonar-scanner
```
- Análisis de calidad de código
- Detección de vulnerabilidades
- Reporte de deuda técnica

### 4. Deploy
```bash
make deploy
```
- A desarrollo
- A staging
- A producción

### 5. Documentation
```bash
mkdocs build
# Publicar a GitHub Pages
```

## Herramientas

### GitHub Actions (Recomendado para GitHub)
- Integrado en GitHub
- YAML declarativo
- Gratuito para público

### GitLab CI
- Integrado en GitLab
- `.gitlab-ci.yml`

### Jenkins
- Auto-hospedado
- Flexible pero más complejo

## Estructura Mínima de GitHub Actions

```yaml
name: CI/CD

on: [push, pull_request]

jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: make build
      - name: Test
        run: make test
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

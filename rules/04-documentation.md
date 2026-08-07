# Regla 04: Documentación

## Premisa

La documentación es código. Debe vivir junto al código fuente, versionarse con Git y ser fácil de mantener.

## Formato

**Markdown** es el estándar para toda documentación:
- Archivos `.md` en el repositorio
- Directorios `docs/` en proyectos
- Fácil de leer en GitHub y otros plataformas

## Estructura de Documentación

```
docs/
├── index.md           # Portada
├── getting-started.md # Inicio rápido
├── architecture/      # Documentación técnica
├── api/              # Referencia de API
└── tutorials/        # Guías paso a paso
```

## Generación de Sitio Web

Usar **MkDocs** para generar sitios estáticos:

```bash
pip install mkdocs mkdocs-material
mkdocs build    # Genera en site/
mkdocs serve    # Visualizar localmente
```

## Publicación

Publicar en **GitHub Pages** a través de CI/CD:
- Generar `site/` en cada release
- Pushear a rama `gh-pages`
- Configurar en Settings de GitHub

## Tipos de Documentación

1. **README.md** - Visión general del proyecto
2. **CONTRIBUTING.md** - Cómo contribuir
3. **Docstrings** - En el código fuente
4. **Decision Records (ADR)** - Decisiones arquitectónicas
5. **API Docs** - Referencia de endpoints/funciones

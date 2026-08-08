# Guía de Inicio Rápido

## Instalación

### Requisitos
- Git
- Make o Just
- Python (para MkDocs)

### Clonar el Repositorio

```bash
git clone https://github.com/rafex/ether-my-best-practice.git
cd ether-my-best-practice
```

### Instalar Dependencias

```bash
pip install -r .config/mkdocs/requirements.txt
```

## Usar las Reglas

Las reglas están en el directorio `rules/`:

```bash
# Ver índice de reglas
cat rules/00-index.md

# Ver una regla específica
cat rules/02-architecture.md
```

## Usar las Plantillas

Las plantillas están en `templates/`:

1. Copiar `Makefile.tmpl` → `Makefile` en tu proyecto
2. Adaptar según necesidades
3. Lo mismo con `Justfile.tmpl`
4. Usarlas como cascarón para que un agente genere una API REST consistente con las reglas del repositorio

```bash
cp templates/repository-structure/Makefile.tmpl mi-proyecto/Makefile
cp templates/repository-structure/Justfile.tmpl mi-proyecto/Justfile
```

También puedes tomar [templates/repository-structure/README.md](../templates/repository-structure/README.md) como base de estructura para un servicio nuevo y complementar el proyecto con las reglas de [../rules/02-architecture.md](../rules/02-architecture.md), [../rules/03-testing.md](../rules/03-testing.md) y [../rules/07-agents-mcp.md](../rules/07-agents-mcp.md).

## Generar Documentación

```bash
# Construir sitio estático
make docs

# Visualizar localmente (operativa de Justfile)
just serve
```

Luego abre `http://localhost:8000`

Si copias las plantillas de [templates](../templates) a otro proyecto, allí sí puedes exponer estos comandos mediante `make docs` o `just docs`.

## Publicar en GitHub Pages

El workflow de CI está en [.github/workflows/static.yml](../.github/workflows/static.yml):

```bash
make pages-build   # Validar reglas + generar sitio
make pages         # Disparar el workflow de GitHub Pages
```

El workflow invoca `make validate` + `make docs` como wrapper de los targets existentes. El directorio [site](../site/) no se sube al repositorio: se genera en el runner y se publica como artefacto de Pages.

## Integrar en tu Proyecto

Agrega referencia a las reglas en tu README:

```markdown
Este proyecto sigue [Ether My Best Practice](https://github.com/rafex/ether-my-best-practice).

Reglas aplicables:
- [Arquitectura Hexagonal](https://github.com/rafex/ether-my-best-practice/blob/main/rules/02-architecture.md)
- [Testing y TDD](https://github.com/rafex/ether-my-best-practice/blob/main/rules/03-testing.md)
```

Si el proyecto va a trabajar con agentes de IA, expón también estas reglas por lectura directa del repositorio o mediante MCP para que el agente pueda decidir cómo construir endpoints, tests, documentación y automatizaciones siguiendo este estándar.

## Integrar con MCP o agentes

La forma mínima de integrar este repositorio con un agente es:

1. Hacer disponible la carpeta [../rules/](../rules/) como contexto.
2. Indicar qué reglas son obligatorias para el proyecto consumidor.
3. Permitir que el agente use [../templates/](../templates/) como punto de partida para generar el esqueleto de la API REST.

El detalle de este enfoque está en [../rules/07-agents-mcp.md](../rules/07-agents-mcp.md).

## Próximos Pasos

1. Explora las [Reglas](../rules/00-index.md)
2. Copia las plantillas a tu proyecto
3. Configura CI/CD según [Regla 06](../rules/06-ci-cd.md)
4. Publica documentación en GitHub Pages

> **Nota:** el `Makefile` y `Justfile` en la raíz de este repositorio son para operar el repositorio mismo (validar reglas, publicar sitio). Las plantillas de build/CI que los agentes deben copiar a proyectos consumidores están en [templates/](../templates/).

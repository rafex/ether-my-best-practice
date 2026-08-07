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
pip install -r requirements.txt
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

```bash
cp templates/Makefile.tmpl mi-proyecto/Makefile
cp templates/Justfile.tmpl mi-proyecto/Justfile
```

## Generar Documentación

```bash
# Construir sitio estático
mkdocs build

# Visualizar localmente
mkdocs serve
```

Luego abre `http://localhost:8000`

Si copias las plantillas de [templates](templates) a otro proyecto, allí sí puedes exponer estos comandos mediante `make docs` o `just docs`.

## Integrar en tu Proyecto

Agrega referencia a las reglas en tu README:

```markdown
Este proyecto sigue [Ether My Best Practice](https://github.com/rafex/ether-my-best-practice).

Reglas aplicables:
- [Arquitectura Hexagonal](https://github.com/rafex/ether-my-best-practice/blob/main/rules/02-architecture.md)
- [Testing y TDD](https://github.com/rafex/ether-my-best-practice/blob/main/rules/03-testing.md)
```

## Próximos Pasos

1. Explora las [Reglas](../rules/00-index.md)
2. Copia las plantillas a tu proyecto
3. Configura CI/CD según [Regla 06](../rules/06-ci-cd.md)
4. Publica documentación en GitHub Pages

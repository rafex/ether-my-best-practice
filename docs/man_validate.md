# validate

## Nombre

validate — valida estructura, bloques tipados y enlaces de las reglas

## Sinopsis

```
make validate
make man TARGET=validate
just validate
```

## Descripción

Delega en `helpers/shell/validate-rules.sh`, que a su vez invoca el
compilador determinista (`helpers/python/rules_compiler.py --action
validate --all`) y valida frontmatter, enlaces entre reglas, enlaces a
`templates/`, sincronía `rules/ ↔ docs/rules/` y la presencia de la capa
de helpers (`mk/`, `just/`, `shell/`, `python/`).

## Opciones

Sin flags. Termina con `exit 1` si `ERRORS > 0`.

## Ejemplos

```bash
make validate
bash helpers/shell/validate-rules.sh
```

## Véase también

- [Regla 01: Herramientas de Construcción](rules/01-build-tooling.md)

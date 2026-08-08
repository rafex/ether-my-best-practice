#!/bin/bash

# Validar estructura de reglas, enlaces internos y plantillas asociadas

set -e

RULES_DIR="./rules"
TEMPLATES_DIR="./templates"
ERRORS=0

echo "Validando reglas..."

# Verificar que todos los archivos .md tienen estructura
for file in "$RULES_DIR"/*.md; do
    if [ -f "$file" ]; then
        echo "  Validando $file..."

        if ! grep -q "^# " "$file"; then
            echo "    FALTA título (# )"
            ((ERRORS++))
        fi

        if [ "$file" != "$RULES_DIR/00-index.md" ]; then
            if ! grep -q "## Premisa" "$file"; then
                echo "    FALTA sección 'Premisa'"
                ((ERRORS++))
            fi
        fi
    fi
done

# Verificar que index.md existe
if [ ! -f "$RULES_DIR/00-index.md" ]; then
    echo "FALTA 00-index.md"
    exit 1
fi

# Validar enlaces internos entre reglas
echo "Validando enlaces entre reglas..."
for file in "$RULES_DIR"/*.md; do
    if [ -f "$file" ]; then
        while IFS= read -r line; do
            while IFS= read -r link; do
                if [[ $link =~ ^[0-9]{2}-.*\.md$ ]]; then
                    if [ ! -f "$RULES_DIR/$link" ]; then
                        echo "  ROTO enlace a regla: $link en $file"
                        ((ERRORS++))
                    fi
                fi
            done < <(printf '%s\n' "$line" | grep -oE '\[[^]]+\]\([^)]+\)' | sed -E 's/^\[[^]]+\]\(([^)]+)\)$/\1/')
        done < "$file"
    fi
done

# Validar que el directorio de plantillas existe
if [ ! -d "$TEMPLATES_DIR" ]; then
    echo "FALTA directorio $TEMPLATES_DIR"
    exit 1
fi

# Validar enlaces a plantillas desde reglas y documentación
echo "Validando enlaces a plantillas..."
for file in "$RULES_DIR"/*.md docs/*.md; do
    if [ -f "$file" ]; then
        while IFS= read -r line; do
            while IFS= read -r link; do
                if [[ $link =~ ^\.\.?/templates/ ]]; then
                    local_path="${link#../}"
                    local_path="${local_path#./}"
                    if [[ $link =~ ^\.\./ ]]; then
                        target_file="$(dirname "$file")/../$local_path"
                    else
                        target_file="$(dirname "$file")/$local_path"
                    fi
                    target_file="$(cd "$(dirname "$target_file")" 2>/dev/null && realpath --relative-to="$PWD" "$(basename "$target_file")" 2>/dev/null || echo "$target_file")"
                    if [ ! -f "$local_path" ] && [ ! -d "$local_path" ]; then
                        echo "  ROTO enlace a plantilla: $link en $file"
                        ((ERRORS++))
                    fi
                fi
            done < <(printf '%s\n' "$line" | grep -oE '\[[^]]+\]\([^)]+\)' | sed -E 's/^\[[^]]+\]\(([^)]+)\)$/\1/')
        done < "$file"
    fi
done

# Validar que las plantillas referenciadas desde reglas existen
echo "Validando referencias a templates desde reglas..."
for file in "$RULES_DIR"/*.md; do
    if [ -f "$file" ]; then
        rule_name="$(basename "$file" .md)"
        while IFS= read -r line; do
            while IFS= read -r link; do
                if [[ $link =~ templates/ && ! $link =~ ^https?:// ]]; then
                    if [[ $link =~ ^\.\./ ]]; then
                        check_path="${link#../}"
                    elif [[ $link =~ ^\./ ]]; then
                        check_path="${link#./}"
                    else
                        check_path="$link"
                    fi
                    if [ ! -f "$check_path" ] && [ ! -d "$check_path" ]; then
                        echo "  ROTO referencia a template: $link en $file"
                        ((ERRORS++))
                    fi
                fi
            done < <(printf '%s\n' "$line" | grep -oE '\[[^]]+\]\([^)]+\)' | sed -E 's/^\[[^]]+\]\(([^)]+)\)$/\1/')
        done < "$file"
    fi
done

if [ $ERRORS -eq 0 ]; then
    echo "Todas las reglas y enlaces son validos"
    exit 0
else
    echo "Se encontraron $ERRORS errores"
    exit 1
fi

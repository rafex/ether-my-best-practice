#!/bin/bash

# Validar todas las reglas

set -e

RULES_DIR="./rules"
ERRORS=0

echo "🔍 Validando reglas..."

# Verificar que todos los archivos .md tienen estructura
for file in "$RULES_DIR"/*.md; do
    if [ -f "$file" ]; then
        echo "  Validando $file..."
        
        # Verificar que tiene título
        if ! grep -q "^# " "$file"; then
            echo "    ❌ Falta título (# )"
            ((ERRORS++))
        fi
        
        # Verificar que tiene premisa
        if [ "$file" != "$RULES_DIR/00-index.md" ]; then
            if ! grep -q "## Premisa" "$file"; then
                echo "    ⚠️  Falta sección 'Premisa'"
            fi
        fi
    fi
done

# Verificar que index.md existe y está actualizado
if [ ! -f "$RULES_DIR/00-index.md" ]; then
    echo "❌ Falta 00-index.md"
    exit 1
fi

# Verificar enlaces en Markdown
echo "🔗 Validando enlaces..."
for file in "$RULES_DIR"/*.md; do
    if [ -f "$file" ]; then
        # Encontrar referencias a otros archivos
        while IFS= read -r line; do
            while IFS= read -r link; do
                # Si es una referencia relativa local
                if [[ $link =~ ^[0-9]{2}-.*\.md$ ]]; then
                    if [ ! -f "$RULES_DIR/$link" ]; then
                        echo "  ❌ Enlace roto: $link en $file"
                        ((ERRORS++))
                    fi
                fi
            done < <(printf '%s\n' "$line" | grep -oE '\[[^]]+\]\([^)]+\)' | sed -E 's/^\[[^]]+\]\(([^)]+)\)$/\1/')
        done < "$file"
    fi
done

if [ $ERRORS -eq 0 ]; then
    echo "✅ Todas las reglas son válidas"
    exit 0
else
    echo "❌ Se encontraron $ERRORS errores"
    exit 1
fi

#!/bin/bash

# Wrapper de validación de reglas — orquesta y delega en el compilador.
# Valida: frontmatter, bloques tipados (AST, vía rules_compiler.py),
# enlaces internos y referencias a plantillas.

set -e

RULES_DIR="./rules"
TEMPLATES_DIR="./templates"
ERRORS=0
WARNINGS=0

INDEX_FILE="00-index.md"

echo "Validando reglas..."
echo ""

# === Compilador (motor determinista de bloques tipados) ===
echo "=== Compilador de Reglas (AST) ==="
COMPILER="helpers/python/rules_compiler.py"
if [ -f "$COMPILER" ]; then
	python3 "$COMPILER" --action validate --all 2>&1 || {
		((ERRORS++))
	}
else
	echo "  WARNING Compilador no encontrado en $COMPILER"
	((WARNINGS++))
fi
echo ""

# === Frontmatter y enlaces (wrapper bash) ===
echo "Validando estructura de reglas..."
for file in "$RULES_DIR"/*.md; do
	[ -f "$file" ] || continue
	base="$(basename "$file")"

	if ! grep -q "^# " "$file"; then
		echo "  ERROR falta título (# ) en $base"
		((ERRORS++))
	fi

	[[ "$base" == "$INDEX_FILE" ]] && { echo "  Validando $base (índice)..."; continue; }

	# Frontmatter
	first_line="$(head -1 "$file")"
	if [[ "$first_line" != "---" ]]; then
		echo "  ERROR falta frontmatter (---) en $base"
		((ERRORS++))
	fi
done

# === Validar enlaces entre reglas ===
echo ""
echo "Validando enlaces entre reglas..."
for file in "$RULES_DIR"/*.md; do
	[ -f "$file" ] || continue
	base="$(basename "$file")"
	while IFS= read -r line; do
		while IFS= read -r link; do
			if [[ $link =~ ^[0-9]{2}-.*\.md$ ]]; then
				if [ ! -f "$RULES_DIR/$link" ]; then
					echo "  ERROR enlace a regla roto: $link en $base"
					((ERRORS++))
				fi
			fi
		done < <(printf '%s\n' "$line" | grep -oE '\[[^]]+\]\([^)]+\)' | sed -E 's/^\[[^]]+\]\(([^)]+)\)$/\1/')
	done < "$file"
done

# === Validar enlaces a plantillas ===
echo ""
if [ ! -d "$TEMPLATES_DIR" ]; then
	echo "ERROR falta directorio $TEMPLATES_DIR"
	exit 1
fi
echo "Validando enlaces a plantillas..."
for file in "$RULES_DIR"/*.md docs/*.md; do
	[ -f "$file" ] || continue
	base="$(basename "$file")"
	while IFS= read -r line; do
		while IFS= read -r link; do
			if [[ $link =~ ^\.\.?/templates/ ]]; then
				local_path="${link#../}"
				local_path="${local_path#./}"
				if [ ! -f "$local_path" ] && [ ! -d "$local_path" ]; then
					echo "  ERROR enlace a plantilla roto: $link en $base"
					((ERRORS++))
				fi
			fi
		done < <(printf '%s\n' "$line" | grep -oE '\[[^]]+\]\([^)]+\)' | sed -E 's/^\[[^]]+\]\(([^)]+)\)$/\1/')
	done < "$file"
done

# === Sincronía rules/ ↔ docs/rules/ ===
echo ""
echo "Validando sincronía rules/ ↔ docs/rules/..."
DOCS_RULES_DIR="./docs/rules"
if [ -d "$DOCS_RULES_DIR" ]; then
	for f in "$RULES_DIR"/*.md; do
		base="$(basename "$f")"
		linked="$DOCS_RULES_DIR/$base"
		if [ ! -f "$linked" ]; then
			echo "  ERROR docs/rules/$base: missing (run 'just link-rules')"
			((ERRORS++))
		elif ! diff -q "$f" "$linked" >/dev/null 2>&1; then
			echo "  ERROR docs/rules/$base: content differs (run 'just link-rules')"
			((ERRORS++))
		fi
	done
	echo "  Sincronía verificada."
else
	echo "  WARNING docs/rules/ directory missing."
	((WARNINGS++))
fi

# === Capa de helpers ===
echo ""
echo "Validando estructura de helpers/..."
HELPERS_MK_DIR="./helpers/mk"
HELPERS_JUST_DIR="./helpers/just"
if [ ! -d "$HELPERS_MK_DIR" ]; then
	echo "  ERROR falta helpers/mk/"
	((ERRORS++))
fi
if [ ! -d "$HELPERS_JUST_DIR" ]; then
	echo "  ERROR falta helpers/just/"
	((ERRORS++))
fi
if [ -d "$HELPERS_MK_DIR" ] && [ -d "$HELPERS_JUST_DIR" ]; then
	echo "  Capa de helpers completa (mk/ + just/ + shell/ + python/)."
fi

echo ""
echo "----------------------------------------"
echo "Errores: $ERRORS  |  Warnings: $WARNINGS"
echo "----------------------------------------"

if [ "$ERRORS" -eq 0 ]; then
	echo "Validación de reglas superada."
	exit 0
else
	echo "Se encontraron $ERRORS error(es)."
	exit 1
fi

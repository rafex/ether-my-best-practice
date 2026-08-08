#!/bin/bash

# Valida estructura de reglas: frontmatter, secciones obligatorias,
# madurez por estado, enlaces internos y referencias a plantillas.

set -e

RULES_DIR="./rules"
TEMPLATES_DIR="./templates"
ERRORS=0
WARNINGS=0

# ------------------------------------------------------------------
# Lista blanca de secciones permitidas para reglas (excluye 00-index)
# ------------------------------------------------------------------
MANDATORY_SECTIONS=("Premisa" "Restricciones" "Ejemplos" "Referencias")
OPTIONAL_SECTIONS=("Estructura" "Nombres Sugeridos" "Comandos" "Plantilla")
# Índice no requiere frontmatter ni estas secciones
INDEX_FILE="00-index.md"

# ------------------------------------------------------------------
# Extrae el contenido entre los delimitadores --- de un frontmatter YAML
# ------------------------------------------------------------------
extract_frontmatter() {
	local file="$1"
	awk '
		/^---$/ { c++; next }
		c == 1 { print }
		c == 2 { exit }
	' "$file"
}

# ------------------------------------------------------------------
# Extrae el valor de un campo del frontmatter (id:, title:, status:, tags:)
# ------------------------------------------------------------------
get_frontmatter_value() {
	local fm="$1"
	local field="$2"
	echo "$fm" | grep -E "^${field}:" | head -1 | sed -E "s/^${field}:\s*//" | xargs
}

# ------------------------------------------------------------------
# Valida una regla individual
# ------------------------------------------------------------------
validate_rule() {
	local file="$1"
	local basename
	basename="$(basename "$file")"

	echo "  Validando $basename..."

	# --- Frontmatter ---
	local first_line
	first_line="$(head -1 "$file")"
	if [[ "$first_line" != "---" ]]; then
		echo "    ERROR falta frontmatter (---)"
		((ERRORS++))
	else
		local fm
		fm="$(extract_frontmatter "$file")"

		local has_closing
		has_closing="$(grep -c '^---$' "$file" || true)"
		if [[ "$has_closing" -lt 2 ]]; then
			echo "    ERROR frontmatter no cerrado (falta segundo ---)"
			((ERRORS++))
		fi

		local f_id f_title f_status f_tags
		f_id="$(get_frontmatter_value "$fm" "id")"
		f_title="$(get_frontmatter_value "$fm" "title")"
		f_status="$(get_frontmatter_value "$fm" "status")"
		f_tags="$(get_frontmatter_value "$fm" "tags")"

		if [[ -z "$f_id" ]]; then
			echo "    ERROR falta id: en frontmatter"
			((ERRORS++))
		fi
		if [[ -z "$f_title" ]]; then
			echo "    ERROR falta title: en frontmatter"
			((ERRORS++))
		fi
		if [[ "$f_status" != "Definida" && "$f_status" != "Borrador" ]]; then
			echo "    ERROR status: debe ser 'Definida' o 'Borrador' (encontrado: '$f_status')"
			((ERRORS++))
		fi
		if [[ -z "$f_tags" ]]; then
			echo "    ERROR falta tags: en frontmatter"
			((ERRORS++))
		fi
	fi

	# --- Secciones obligatorias ---
	for sec in "${MANDATORY_SECTIONS[@]}"; do
		if ! grep -q "^## $sec" "$file"; then
			echo "    ERROR falta sección obligatoria '## $sec'"
			((ERRORS++))
		fi
	done

	# --- Secciones fuera de la lista blanca (warning) ---
	local all_headers
	all_headers="$(grep '^## ' "$file" | sed 's/^## //' || true)"
	local full_whitelist=("${MANDATORY_SECTIONS[@]}" "${OPTIONAL_SECTIONS[@]}" "Plantilla")
	while IFS= read -r header; do
		[[ -z "$header" ]] && continue
		local found=false
		for w in "${full_whitelist[@]}"; do
			if [[ "$header" == "$w" ]]; then
				found=true
				break
			fi
		done
		if [[ "$found" == false ]]; then
			echo "    WARNING sección '## $header' no está en la lista blanca (¿typo?)"
			((WARNINGS++))
		fi
	done <<< "$all_headers"

	# --- Regla de madurez: Definida requiere Comandos + Estructura ---
	if [[ "$f_status" == "Definida" ]]; then
		if ! grep -q "^## Comandos" "$file"; then
			echo "    ERROR status=Definida requiere '## Comandos'"
			((ERRORS++))
		fi
		if ! grep -q "^## Estructura" "$file"; then
			echo "    ERROR status=Definida requiere '## Estructura'"
			((ERRORS++))
		fi
	fi
}

# ==================================================================
# MAIN
# ==================================================================

echo "Validando reglas..."

# Verificar que 00-index.md existe
if [ ! -f "$RULES_DIR/$INDEX_FILE" ]; then
	echo "ERROR falta $INDEX_FILE"
	exit 1
fi

# Validar cada regla .md
for file in "$RULES_DIR"/*.md; do
	if [ ! -f "$file" ]; then continue; fi

	base="$(basename "$file")"

	# Título obligatorio para todos
	if ! grep -q "^# " "$file"; then
		echo "  ERROR falta título (# ) en $base"
		((ERRORS++))
	fi

	# 00-index se valida por separado (sin frontmatter ni secciones obligatorias)
	if [[ "$base" == "$INDEX_FILE" ]]; then
		echo "  Validando $base (índice)..."
		continue
	fi

	validate_rule "$file"
done

# Validar enlaces internos entre reglas
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

# Validar directorio de plantillas
echo ""
if [ ! -d "$TEMPLATES_DIR" ]; then
	echo "ERROR falta directorio $TEMPLATES_DIR"
	exit 1
fi

# Validar enlaces a plantillas desde reglas y docs
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

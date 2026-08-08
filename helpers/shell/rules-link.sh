#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
# Helper de enlaces de reglas → documentación (hard links).
# Crea/verifica hard links de rules/*.md → docs/rules/*.md para que
# MkDocs las incluya en el sitio (docs_dir es docs/).
#
# Contrato (regla 01):
#   --goal link|check
#   --log-file /ruta/al/log
#
# link:  mkdir -p docs/rules && ln -f rules/*.md docs/rules/
#        Hard link real → mismo inode; editar rules/ actualiza docs/.
#
# check: verifica que cada rules/*.md tenga contraparte en docs/rules/
#        con contenido idéntico (detecta drift en clones).
#
# Auditoría: /var/log/<proyecto>/log-rules-link-<ts>.log
#             Fallback → /tmp/<proyecto>/log-rules-link-<ts>.log
# ------------------------------------------------------------------

goal=""
log_file=""
workspace="$(pwd)"

project_name="$(basename "$workspace")"
script_name="rules-link"
ts="$(date -u +%Y%m%dT%H%M%SZ)"

init_log() {
	if [[ -z "$log_file" ]]; then
		if mkdir -p "/var/log/$project_name" 2>/dev/null && [[ -w "/var/log/$project_name" ]]; then
			log_file="/var/log/$project_name/log-$script_name-$ts.log"
		else
			mkdir -p "/tmp/$project_name"
			log_file="/tmp/$project_name/log-$script_name-$ts.log"
		fi
	fi
	mkdir -p "$(dirname "$log_file")"
}

while [[ $# -gt 0 ]]; do
	case "$1" in
		--goal)     goal="${2:-}"; shift 2 ;;
		--log-file) log_file="${2:-}"; shift 2 ;;
		*)
			echo "Unknown flag: $1" >&2
			exit 1 ;;
	esac
done

if [[ -z "$goal" ]]; then
	echo "Missing required flag --goal" >&2
	exit 1
fi

init_log
exec > >(tee -a "$log_file") 2>&1

echo "Audit log: $log_file"
echo "Goal: $goal"
echo "Workspace: $workspace"

RULES_DIR="$workspace/rules"
DOCS_RULES_DIR="$workspace/docs/rules"

case "$goal" in
	link)
		if [ ! -d "$RULES_DIR" ]; then
			echo "No rules directory found at $RULES_DIR" >&2
			exit 1
		fi
		mkdir -p "$DOCS_RULES_DIR"
		echo "Creating hard links from $RULES_DIR → $DOCS_RULES_DIR..."
		count=0
		for f in "$RULES_DIR"/*.md; do
			base="$(basename "$f")"
			ln -f "$f" "$DOCS_RULES_DIR/$base"
			echo "  linked: $base"
			count=$((count + 1))
		done
		echo "$count rules linked to $DOCS_RULES_DIR"
		echo "docs/rules/: $(ls "$DOCS_RULES_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ') files"
		;;
	check)
		errors=0
		if [ ! -d "$RULES_DIR" ]; then
			echo "No rules directory found at $RULES_DIR" >&2
			exit 1
		fi
		if [ ! -d "$DOCS_RULES_DIR" ]; then
			echo "docs/rules/ directory missing. Run with --goal link first." >&2
			exit 1
		fi
		echo "Checking synchronization rules ↔ docs/rules..."
		for f in "$RULES_DIR"/*.md; do
			base="$(basename "$f")"
			linked="$DOCS_RULES_DIR/$base"
			if [ ! -f "$linked" ]; then
				echo "  MISSING: $base not found in docs/rules/"
				errors=$((errors + 1))
			elif ! diff -q "$f" "$linked" >/dev/null 2>&1; then
				echo "  DRIFT:   $base differs between rules/ and docs/rules/"
				errors=$((errors + 1))
			fi
		done
		if [ $errors -eq 0 ]; then
			echo "All rules synchronized."
		else
			echo "Found $errors synchronization error(s). Run 'just link-rules' to fix." >&2
		fi
		;;
	*)
		echo "Unknown goal: $goal. Expected link|check" >&2
		exit 1 ;;
esac

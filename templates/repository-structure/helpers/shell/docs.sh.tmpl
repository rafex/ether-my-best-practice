#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/logs.sh"
source "$SCRIPT_DIR/lib/messages.sh"
init_log "docs"

# ------------------------------------------------------------------
# docs.sh — Helper de documentación: build, serve.
# Reutilizable por Makefile (vía helpers/mk/docs.mk) y Justfile.
#
# Contrato (regla 01):
#   --goal build|serve       Operación
#   --file .config/mkdocs/mkdocs.yml   Archivo de configuración MkDocs
#   --site-dir site          Directorio de salida del sitio
#   --command (opcional)     Comando directo (sobreescribe goal)
#   --log-file /ruta/al/log  Obligatorio
#   --log-level info         (opcional)
#
# Auditoría: helpers/shell/lib/logs.sh (regla 15)
# ------------------------------------------------------------------

goal=""
mkdocs_file=""
site_dir="site"
command_line=""
log_file=""
workspace="$(pwd)"

while [[ $# -gt 0 ]]; do
	case "$1" in
		--goal)      goal="${2:-}"; shift 2 ;;
		--file)      mkdocs_file="${2:-}"; shift 2 ;;
		--site-dir)  site_dir="${2:-}"; shift 2 ;;
		--command)   command_line="${2:-}"; shift 2 ;;
		--log-file)  log_file="${2:-}"; shift 2 ;;
		--log-level) log_level="${2:-}"; shift 2 ;;
		*)
			die "Unknown flag: $1"
			;;
	esac
done

if [[ -n "$command_line" ]]; then goal=""; fi
if [[ -z "$goal" && -z "$command_line" ]]; then
	die "Missing required flag --goal or --command"
fi

log_info "Goal: $goal"
log_info "MkDocs file: ${mkdocs_file:-default}"
log_info "Site dir: $site_dir"

	resolve_cmd() {
	local file_flag=""
	if [[ -n "$mkdocs_file" ]]; then
		file_flag="-f $mkdocs_file"
	fi
	case "$goal" in
		build) echo "mkdocs build $file_flag --site-dir \"$workspace/$site_dir\"" ;;
		serve) echo "mkdocs serve $file_flag" ;;
		*)     echo "" ;;
	esac
}

if [[ -n "$command_line" ]]; then
	cmd="$command_line"
else
	cmd="$(resolve_cmd)"
	if [[ -z "$cmd" ]]; then
		die "Unknown goal: $goal"
	fi
fi

log_info "Executing: $cmd"
bash -lc "$cmd"

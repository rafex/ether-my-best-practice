#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/logs.sh"
source "$SCRIPT_DIR/lib/messages.sh"
init_log "github"


# Helper de GitHub para operación de este repositorio.
# Atiende: disparar workflows, publicar el sitio.
# Compartido por Makefile y Justfile raíz.

action=""
workflow=""
ref="main"
repo=""
log_file=""
log_level="info"
workspace="$(pwd)"

while [[ $# -gt 0 ]]; do
	case "$1" in
		--action)
			action="${2:-}"; shift 2 ;;
		--workflow)
			workflow="${2:-}"; shift 2 ;;
		--ref)
			ref="${2:-}"; shift 2 ;;
		--repo)
			repo="${2:-}"; shift 2 ;;
		--log-file)
			log_file="${2:-}"; shift 2 ;;
		--log-level)
			log_level="${2:-}"; shift 2 ;;
		*)
			echo "Unknown flag: $1" >&2
			exit 1 ;;
	esac
done

if [[ -z "$action" ]]; then
	echo "Missing required flag --action" >&2
	exit 1
fi
if [[ -z "$workflow" ]]; then
	echo "Missing required flag --workflow" >&2
	exit 1
fi

project_name="$(basename "$workspace")"
script_name="github"
ts="$(date -u +%Y%m%dT%H%M%SZ)"

if [[ -z "$log_file" ]]; then
	if mkdir -p "/var/log/$project_name" 2>/dev/null && [[ -w "/var/log/$project_name" ]]; then
		log_file="/var/log/$project_name/log-$script_name-$ts.log"
	else
		mkdir -p "/tmp/$project_name"
		log_file="/tmp/$project_name/log-$script_name-$ts.log"
	fi
fi

mkdir -p "$(dirname "$log_file")"
exec > >(tee -a "$log_file") 2>&1

echo "Audit log: $log_file"
echo "Action: $action"
echo "Workflow: $workflow"
echo "Ref: $ref"

case "$action" in
	workflow-run)
		if ! command -v gh >/dev/null 2>&1; then
			echo "GitHub CLI (gh) no está disponible. Instala gh para disparar workflows." >&2
			exit 1
		fi
		gh_args=()
		if [[ -n "$repo" ]]; then
			gh_args+=(--repo "$repo")
		fi
		echo "Disparando workflow $workflow en ref=$ref..."
		gh workflow run "$workflow" --ref "$ref" "${gh_args[@]}"
		echo "Workflow $workflow disparado correctamente en $ref"
		;;
	*)
		echo "Unknown action: $action" >&2
		exit 1 ;;
esac

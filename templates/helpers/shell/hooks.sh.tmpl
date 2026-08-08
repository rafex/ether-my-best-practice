#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
# Helper compartido de Git Hooks — instalación y ejecución de gates.
# Reutiliza la cadena Makefile → .mk → script para lint y test.
#
# Contrato (regla 01):
#   --action install|pre-commit|pre-push|commit-msg
#   --target    (opcional) sobrescribe el target de make por defecto
#   --log-file /ruta/al/log            Obligatorio
#   --log-level info                   (opcional)
#
# Variables de entorno para sobrescribir gates:
#   PRE_COMMIT_TARGET=validate  make validate en vez de make lint
#   PRE_PUSH_TARGET=docs        make docs en vez de make test
#
# Para agentes de IA: este script es la capa única de ejecución de
# git hooks. Los dispatchers en .githooks/ solo lo invocan con
# --action. La lógica de lint/test/commit-msg vive aquí.
#
# Instalación:
#   bash helpers/shell/hooks.sh --action install
#   → git config core.hooksPath .githooks
#
# Auditoría: /var/log/<proyecto>/log-hooks-<ts>.log
#             Fallback → /tmp/<proyecto>/log-hooks-<ts>.log
# ------------------------------------------------------------------

action=""
target=""
message_file=""
log_file=""
log_level="info"
workspace="$(pwd)"

while [[ $# -gt 0 ]]; do
	case "$1" in
		--action)
			action="${2:-}"; shift 2 ;;
		--target)
			target="${2:-}"; shift 2 ;;
		--log-file)
			log_file="${2:-}"; shift 2 ;;
		--log-level)
			log_level="${2:-}"; shift 2 ;;
		*)
			if [[ -z "$message_file" && "$action" == "commit-msg" ]]; then
				message_file="$1"; shift
			else
				echo "Unknown flag: $1" >&2
				exit 1
			fi
			;;
	esac
done

if [[ -z "$action" ]]; then
	echo "Missing required flag --action" >&2
	exit 1
fi

project_name="$(basename "$workspace")"
script_name="hooks"
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
echo "Workspace: $workspace"

case "$action" in
	install)
		git config core.hooksPath .githooks
		echo "Git hooks instalados: core.hooksPath = .githooks"
		;;
	pre-commit)
		local_target="${target:-${PRE_COMMIT_TARGET:-lint}}"
		echo "Running pre-commit: make ${local_target}"
		make "${local_target}"
		echo "pre-commit passed: make ${local_target}"
		;;
	pre-push)
		local_target="${target:-${PRE_PUSH_TARGET:-test}}"
		echo "Running pre-push: make ${local_target}"
		make "${local_target}"
		echo "pre-push passed: make ${local_target}"
		;;
	commit-msg)
		if [[ -z "$message_file" ]]; then
			message_file="${1:-}"
		fi
		if [[ -z "$message_file" || ! -f "$message_file" ]]; then
			echo "Missing commit message file for commit-msg validation" >&2
			exit 1
		fi
		echo "Validating commit message: $message_file"
		if [ -f "helpers/shell/commit-msg.sh" ]; then
			bash helpers/shell/commit-msg.sh "$message_file"
		else
			echo "No commit-msg helper found. Expected helpers/shell/commit-msg.sh"
			exit 1
		fi
		echo "commit-msg passed"
		;;
	*)
		echo "Unknown action: $action. Expected install|pre-commit|pre-push|commit-msg" >&2
		exit 1 ;;
esac

#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
# Helper de Serve — levanta el sitio estático localmente.
# Reutiliza make docs (que incluye link-rules) y npx serve.
#
# Contrato (regla 01):
#   --action serve                      Operación (única hoy)
#   --site-dir site                     Directorio del sitio generado
#   --port 8000                         Puerto del servidor
#   --log-file /ruta/al/log             Obligatorio
#   --log-level info                    (opcional)
#
# Flujo:
#   make docs (build + link-rules) → npx serve <site-dir> -l <port>
#
# Auditoría: /var/log/<proyecto>/log-serve-<ts>.log
#             Fallback → /tmp/<proyecto>/log-serve-<ts>.log
# ------------------------------------------------------------------

action=""
site_dir="site"
port="8000"
log_file=""
log_level="info"
workspace="$(pwd)"

project_name="$(basename "$workspace")"
script_name="serve"
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
		--action)   action="${2:-}"; shift 2 ;;
		--site-dir) site_dir="${2:-}"; shift 2 ;;
		--port)     port="${2:-}"; shift 2 ;;
		--log-file) log_file="${2:-}"; shift 2 ;;
		--log-level) log_level="${2:-}"; shift 2 ;;
		*)
			echo "Unknown flag: $1" >&2
			exit 1 ;;
	esac
done

if [[ -z "$action" ]]; then
	echo "Missing required flag --action" >&2
	exit 1
fi

init_log
exec > >(tee -a "$log_file") 2>&1

echo "Audit log: $log_file"
echo "Action: $action"
echo "Site dir: $site_dir"
echo "Port: $port"

case "$action" in
	serve)
		echo "Building site (make docs)..."
		make docs
		echo "Site ready at $site_dir/"
		echo "Starting static server on http://localhost:$port ..."
		cd "$workspace"
		npx serve "$site_dir" -l "$port"
		;;
	*)
		echo "Unknown action: $action. Expected serve" >&2
		exit 1 ;;
esac

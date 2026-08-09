#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/logs.sh"
source "$SCRIPT_DIR/lib/messages.sh"
init_log "release"

# ------------------------------------------------------------------
# release.sh — CD pipeline: package, release, deploy.
# Orquestado por Makefile, usado por el workflow release.yml.
#
# Contrato (regla 01):
#   --action package|release|deploy|version
#
# Auditoría: helpers/shell/lib/logs.sh (regla 15)
# ------------------------------------------------------------------

action=""
mcp_dir="mcp"
output_dir="${mcp_dir}/dist"
workspace="$(pwd)"
project_name="$(basename "$workspace")"

while [[ $# -gt 0 ]]; do
	case "$1" in
		--action) action="${2:-}"; shift 2 ;;
		*)
			echo "Unknown flag: $1" >&2
			exit 1 ;;
	esac
done

if [[ -z "$action" ]]; then
	die "Missing required flag --action" >&2
fi

header "CD: Ether Best Practices — $action"

case "$action" in
	package)
		step 1 2 "Sincronizando libs al paquete MCP..."
		if [[ -d "helpers/python/lib" ]]; then
			rm -rf "$mcp_dir/ether_mcp_my_best_practices/lib"
			cp -r "helpers/python/lib" "$mcp_dir/ether_mcp_my_best_practices/lib"
			log_info "  Libs copiadas a ether_mcp_my_best_practices/lib/"
		fi

		step 2 2 "Construyendo wheel con uv build..."
		(cd "$mcp_dir" && uv build --out-dir dist)
		success "Package generado en $output_dir/"
		ls -la "$output_dir"/*.whl 2>/dev/null || die "Wheel no generado"
		;;

	release)
		if ! command -v gh >/dev/null 2>&1; then
			die "GitHub CLI (gh) no está disponible."
		fi

		version="$(cat VERSION 2>/dev/null || echo "0.0.0")"
		tag="v${version}"
		wheel="$(ls "$output_dir"/*.whl 2>/dev/null | head -1)"
		if [[ -z "$wheel" ]]; then
			die "No se encontró wheel en $output_dir/. Ejecuta make package primero."
		fi

		step 1 1 "Creando GitHub Release $tag con asset..."
		gh release create "$tag" \
			--title "$tag — Ether Best Practices" \
			--generate-notes \
			"$wheel"

		success "Release $tag publicado. Descargar en:"
		success "  https://github.com/rafex/ether-my-best-practice/releases/tag/$tag"
		;;

	deploy)
		step 1 3 "Ejecutando validate..."
		bash "$workspace/helpers/shell/validate-rules.sh" || die "validate falló"

		step 2 3 "Empaquetando..."
		bash "$workspace/helpers/shell/release.sh" --action package || die "package falló"

		step 3 3 "Publicando release..."
		bash "$workspace/helpers/shell/release.sh" --action release || die "release falló"

		success "Deploy completo. Enlace del portal:"
		success "  https://github.com/rafex/ether-my-best-practice/releases/latest"
		;;

	*)
		die "Unknown action: $action. Expected package|release|deploy." >&2
		;;
esac

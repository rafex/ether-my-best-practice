#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/logs.sh"
source "$SCRIPT_DIR/lib/messages.sh"
init_log "release"

# ------------------------------------------------------------------
# release.sh — CD pipeline: package, release.
# Orquestado por Makefile: make package / make release.
# No incluye deploy — la orquestación la hace el Makefile.
#
# Contrato (regla 01):
#   --action package|release
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
		step 1 3 "Sincronizando libs y snapshots al paquete MCP..."
		if [[ -d "helpers/python/lib" ]]; then
			rm -rf "$mcp_dir/ether_mcp_my_best_practices/lib"
			cp -r "helpers/python/lib" "$mcp_dir/ether_mcp_my_best_practices/lib"
			log_info "  Libs copiadas a ether_mcp_my_best_practices/lib/"
		fi
		# Generar build ID
		build_id="$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")"
		echo "BUILD = \"$build_id\"" > "$mcp_dir/ether_mcp_my_best_practices/_build.py"
		log_info "  Build ID: $build_id"
		# Copiar snapshots de datos (rules, templates, helpers, docs)
		data_dir="$mcp_dir/ether_mcp_my_best_practices/data"
		rm -rf "$data_dir"
		mkdir -p "$data_dir"
		for d in rules templates helpers docs; do
			if [[ -d "$workspace/$d" ]]; then
				cp -r "$workspace/$d" "$data_dir/$d"
				log_info "  Snapshot: $d → data/$d"
			fi
		done

		step 2 3 "Construyendo wheel con uv build..."
		mkdir -p "$output_dir"
		rm -f "$output_dir"/*.whl "$output_dir"/*.whl.sha256 "$output_dir"/*.tar.gz
		(cd "$mcp_dir" && uv build --out-dir dist)

		# Generar checksum
		for wheel in "$output_dir"/*.whl; do
			if [ -f "$wheel" ]; then
				sha256sum "$wheel" | sed "s|$output_dir/||g" > "$wheel.sha256"
				log_info "  Checksum: ${wheel}.sha256"
			fi
		done

		wheel="$(ls "$output_dir"/*.whl 2>/dev/null | head -1 || true)"
		if [[ -n "$wheel" ]]; then
			step 3 3 "Verificando wheel en aislamiento..."
			RULES_REMOTE_URL="http://127.0.0.1:1/unavailable" uv run \
				--isolated --no-project --with "$wheel" python -c \
				'from ether_mcp_my_best_practices import server as s; assert len(s.list_rules()) == 18; assert hasattr(s, "check_project"); print("MCP wheel smoke test: OK")'
		fi

		success "Package generado en $output_dir/"
		ls -la "$output_dir"/*.whl 2>/dev/null || die "Wheel no generado"
		;;

	release)
		if ! command -v gh >/dev/null 2>&1; then
			die "GitHub CLI (gh) no está disponible."
		fi

		version="$(cat VERSION 2>/dev/null || echo "0.0.0")"
		tag="v${version}"
		wheel="$(find "$output_dir" -maxdepth 1 -type f -name "*-${version}-*.whl" -print -quit 2>/dev/null || true)"
		checksum="${wheel}.sha256"
		if [[ -z "$wheel" || ! -f "$checksum" ]]; then
			die "No se encontró el wheel ${version} y su checksum en $output_dir/. Ejecuta make package primero."
		fi

		step 1 1 "Creando GitHub Release $tag con assets..."
		gh release create "$tag" \
			--title "$tag — Ether Best Practices" \
			--generate-notes \
			"$wheel" \
			"$checksum"

		success "Release $tag publicado. Descargar en:"
		success "  https://github.com/rafex/ether-my-best-practice/releases/tag/$tag"
		;;

	*)
		die "Unknown action: $action. Expected package|release." >&2
		;;
esac

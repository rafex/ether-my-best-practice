#!/usr/bin/env bash
# ------------------------------------------------------------------
# mcp-install.sh — Instalador inteligente del MCP ether-rules.
# Descarga el wheel de GitHub releases/latest con cURL, instala vía
# uv y configura los clientes Claude, Codex y opencode.
#
# Ejecutable directo: curl -sL <url> | bash
# Operativa del repo: just app-install
#
# Contrato:
#   --action install|install-client <name>|status|uninstall
#
# Server: ether-rules → comando: uvx ether-mcp
# ------------------------------------------------------------------
set -euo pipefail

action=""
client=""
workspace="$(pwd)"

while [[ $# -gt 0 ]]; do
	case "$1" in
		--action) action="${2:-}"; shift 2 ;;
		*) client="${1:-}"; shift ;;
	esac
done

info()  { echo "[INFO]  $*"; }
warn()  { echo "[WARN]  $*" >&2; }
error() { echo "[ERROR] $*" >&2; }
success(){ echo "[OK]    $*"; }

case "${OS:-}" in Windows*) IS_WINDOWS=true ;; *) IS_WINDOWS=false ;; esac
if [[ "$(uname -s 2>/dev/null)" == *"_NT"* ]]; then IS_WINDOWS=true; fi

client_present() {
	command -v "$1" >/dev/null 2>&1
}

# ─── Descargar ───────────────────────────────────────────────────────
download_wheel() {
	local tmp_dir="/tmp/ether-mcp-$$"
	mkdir -p "$tmp_dir"
	info "Descargando última versión desde GitHub releases..."
	local api_json
	api_json="$(curl -sL https://api.github.com/repos/rafex/ether-my-best-practice/releases/latest 2>/dev/null || true)"
	if [[ -z "$api_json" ]]; then
		error "No se pudo obtener la información del release."
		return 1
	fi
	local wheel_url sha_url
	wheel_url="$(echo "$api_json" | python3 -c "import sys,json; assets=json.load(sys.stdin).get('assets',[]); urls=[a['browser_download_url'] for a in assets if a['name'].endswith('.whl')]; print(urls[0] if urls else '')" 2>/dev/null || true)"
	sha_url="$(echo "$api_json" | python3 -c "import sys,json; assets=json.load(sys.stdin).get('assets',[]); urls=[a['browser_download_url'] for a in assets if a['name'].endswith('.whl.sha256')]; print(urls[0] if urls else '')" 2>/dev/null || true)"
	if [[ -z "$wheel_url" ]]; then
		error "No se encontró el wheel en el último release."
		return 1
	fi
	info "Descargando: $wheel_url"
	curl -sL "$wheel_url" -o "$tmp_dir/ether_mcp.whl"
	if [[ -n "$sha_url" ]]; then
		info "Descargando checksum..."
		curl -sL "$sha_url" -o "$tmp_dir/ether_mcp.whl.sha256"
		info "Verificando checksum..."
		if (cd "$tmp_dir" && sha256sum -c ether_mcp.whl.sha256 2>/dev/null); then
			success "Checksum verificado."
		else
			error "Checksum NO coincide. Abortando instalación."
			rm -rf "$tmp_dir"
			return 1
		fi
	else
		warn "No se encontró checksum en el release — continuando sin verificar."
	fi
	echo "$tmp_dir"
}

# ─── Configurar cliente ──────────────────────────────────────────────
configure_client() {
	local name="$1"
	local cfg_dir cfg_file

	if client_present "$name"; then
		case "$name" in
			claude)  "$name" mcp add --scope user ether-rules -- uvx ether-mcp 2>&1 && return ;;
			codex)   "$name" mcp add ether-rules -- uvx ether-mcp 2>&1 && return ;;
			opencode) "$name" mcp add ether-rules -- uvx ether-mcp 2>&1 && return ;;
		esac
		info "CLI falló para $name — configurando manualmente..."
	fi

	# Fallback: escribir archivo de config
	case "$name" in
		claude)
			if $IS_WINDOWS; then cfg_dir="$APPDATA/Claude"; cfg_file="$HOME/.claude.json"; else cfg_dir="$HOME/.config/claude"; cfg_file="$HOME/.claude.json"; fi
			;;
		codex)
			if $IS_WINDOWS; then cfg_dir="$USERPROFILE/.codex"; cfg_file="$USERPROFILE/.codex/config.toml"; else cfg_dir="$HOME/.codex"; cfg_file="$HOME/.codex/config.toml"; fi
			;;
		opencode)
			if $IS_WINDOWS; then cfg_dir="$APPDATA/opencode"; cfg_file="$APPDATA/opencode/opencode.json"; else cfg_dir="$HOME/.config/opencode"; cfg_file="$HOME/.config/opencode/opencode.json"; fi
			;;
	esac
	mkdir -p "$cfg_dir"

	case "$name" in
		claude|opencode)
			local cfg_json="$cfg_file"
			if [[ -f "$cfg_json" ]]; then
				python3 -c "
import json, sys
with open('$cfg_json') as f: cfg = json.load(f)
cfg.setdefault('mcpServers', {})['ether-rules'] = {'command': 'uvx', 'args': ['ether-mcp']}
with open('$cfg_json', 'w') as f: json.dump(cfg, f, indent=2)
" 2>/dev/null && return
			fi
			# crear nuevo
			python3 -c "
import json
cfg = {'mcpServers': {'ether-rules': {'command': 'uvx', 'args': ['ether-mcp']}}}
with open('$cfg_json', 'w') as f: json.dump(cfg, f, indent=2)
" 2>/dev/null || true
			;;
		codex)
			local cfg_toml="$cfg_file"
			if [[ -f "$cfg_toml" ]]; then
				echo '' >> "$cfg_toml"
				echo '[mcp_servers.ether-rules]' >> "$cfg_toml"
				echo 'command = "uvx"' >> "$cfg_toml"
				echo 'args = ["ether-mcp"]' >> "$cfg_toml"
			else
				echo '[mcp_servers.ether-rules]' > "$cfg_toml"
				echo 'command = "uvx"' >> "$cfg_toml"
				echo 'args = ["ether-mcp"]' >> "$cfg_toml"
			fi
			;;
	esac
}

# ─── Instalar ────────────────────────────────────────────────────────
do_install() {
	info "Instalador ether-rules para Claude · Codex · opencode"

	if ! command -v python3 >/dev/null 2>&1; then
		die "Python 3.12+ requerido. No se encontró python3."
	fi
	if ! command -v uv >/dev/null 2>&1; then
		warn "uv no detectado. Se recomienda instalarlo: curl -LsSf https://astral.sh/uv/install.sh | sh"
		warn "Continuando con pip como fallback..."
	fi

	local tmp_dir
	tmp_dir="$(download_wheel)" || exit 1

	info "Instalando MCP..."
	if command -v uv >/dev/null 2>&1; then
		uv tool install "$tmp_dir/ether_mcp.whl"
	else
		pip install --user "$tmp_dir/ether_mcp.whl"
	fi
	success "MCP ether-rules instalado (comando: ether-mcp)."

	info "Configurando clientes..."
	for c in claude codex opencode; do
		if client_present "$c"; then
			info "  Configurando $c..."
			configure_client "$c"
			success "  $c → ether-rules configurado."
		else
			info "  $c: no detectado en PATH (saltando)."
		fi
	done

	rm -rf "$tmp_dir"
	success "Instalación completada."
	success "Verifica con: claude mcp list  /  codex mcp list  /  opencode mcp list"
}

do_install_client() {
	configure_client "$client" && success "$client configurado con ether-rules."
}

do_status() {
	info "Estado de ether-rules en los clientes:"
	for c in claude codex opencode; do
		if client_present "$c"; then
			echo -n "  $c: "
			if "$c" mcp list 2>/dev/null | grep -qi ether-rules; then
				success "configurado"
			else
				warn "no configurado"
			fi
		else
			info "  $c: no instalado"
		fi
	done
	if command -v uv >/dev/null 2>&1 && uv tool list 2>/dev/null | grep -qi ether-mcp; then
		success "ether-mcp instalado (uv tool list)"
	else
		warn "ether-mcp no instalado como herramienta uv"
	fi
}

do_uninstall() {
	info "Desinstalando ether-rules..."
	for c in claude codex opencode; do
		if client_present "$c"; then
			"$c" mcp remove ether-rules 2>/dev/null || true
		fi
	done
	if command -v uv >/dev/null 2>&1; then
		uv tool uninstall ether-mcp-my-best-practices 2>/dev/null || true
	fi
	success "Desinstalación completada."
}

# ─── Main ─────────────────────────────────────────────────────────────
die() { error "$@"; exit 1; }

case "$action" in
	install)       do_install ;;
	install-client) do_install_client ;;
	status)        do_status ;;
	uninstall)     do_uninstall ;;
	*)             echo "Usage: $0 --action install|install-client <name>|status|uninstall" >&2; exit 1 ;;
esac

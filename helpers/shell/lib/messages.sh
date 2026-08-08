#!/usr/bin/env bash
# ------------------------------------------------------------------
# messages.sh — Mensajes de UI para helpers shell.
# Source: source "$(dirname "${BASH_SOURCE[0]}")/lib/messages.sh"
#
# Requiere: logs.sh, colors.sh (deben sourcearse antes).
# Funciones: success, error, warning, info, step, die, header.
#
# Para agentes de IA: usar mensajes estandarizados en vez de echo
# para mantener consistencia UI y auditoría.
# ------------------------------------------------------------------

# success <message>
success() { echo -e "$(colorize COLOR_GREEN "✓") $(log_info "$@")"; }

# error <message>
error()  { echo -e "$(colorize COLOR_RED "✗") $(log_error "$@")" >&2; }

# warning <message>
warning(){ echo -e "$(colorize COLOR_YELLOW "⚠") $(log_warn "$@")"; }

# info <message>
info()   { echo -e "$(colorize COLOR_CYAN "ℹ") $(log_info "$@")"; }

# step <N> <total> <message>  → "step 2/5: message"
step() {
	local n="$1"
	local total="$2"
	shift 2
	echo -e "$(colorize COLOR_BLUE "▶") [${n}/${total}] $*"
}

# die <message> [exit_code=1]
die() {
	local msg="$1"
	local code="${2:-1}"
	error "$msg"
	exit "$code"
}

# header <message>  → línea decorativa en negrita
header() {
	local msg="$1"
	local line
	printf -v line '%*s' "${#msg}" ''
	line="${line// /─}"
	echo
	echo "$(colorize COLOR_BOLD "$msg")"
	echo "$(colorize COLOR_BOLD "$line")"
}

#!/usr/bin/env bash
# ------------------------------------------------------------------
# messages.sh — Mensajes de UI para helpers shell.
# Source: source "$(dirname "${BASH_SOURCE[0]}")/lib/messages.sh"
#
# Requisito: logs.sh (debe sourcearse antes).
# Auto-sourcea colors.sh si no se ha hecho.
# Funciones: success, error, warning, info, step, die, header.

# Auto-source colors.sh si no se ha hecho
if [[ -z "${COLOR_ENABLED:-}" ]]; then
    _lib_dir="$(dirname "${BASH_SOURCE[0]:-$0}")"
    if [[ -f "$_lib_dir/colors.sh" ]]; then
        source "$_lib_dir/colors.sh"
    fi
fi
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

#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/logs.sh"
source "$SCRIPT_DIR/lib/messages.sh"
init_log "format"

# ------------------------------------------------------------------
# format.sh — Placeholder de formateo (regla 01).
# Pendiente de implementar con tool específico (shfmt, ruff format, etc.).
# ------------------------------------------------------------------
warning "Format pendiente de implementar — placeholder de regla 01."

#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/logs.sh"
source "$SCRIPT_DIR/lib/messages.sh"
init_log "lint"

# ------------------------------------------------------------------
# lint.sh — Validación de sintaxis de helpers shell y python.
# Llamado por make lint (vía helpers/mk/lint.mk) o pre-commit.
#
# Valida: bash -n en todos los .sh de helpers/shell/ + lib/
#         python3 -m py_compile en todos los .py de helpers/python/ + lib/
#
# Auditoría: helpers/shell/lib/logs.sh (regla 15)
# ------------------------------------------------------------------

workspace="$(pwd)"
failed=0
checked=0

header "Lint: helpers shell"
for f in "$workspace"/helpers/shell/*.sh; do
    [[ -f "$f" ]] || continue
    name="$(basename "$f")"
    if bash -n "$f" 2>/dev/null; then
        log_info "  OK: $name"
    else
        error "  FAIL: $name"
        failed=$((failed + 1))
    fi
    checked=$((checked + 1))
done

# lib shell
for f in "$workspace"/helpers/shell/lib/*.sh; do
    [[ -f "$f" ]] || continue
    name="$(basename "$f")"
    if bash -n "$f" 2>/dev/null; then
        log_info "  OK: lib/$name"
    else
        error "  FAIL: lib/$name"
        failed=$((failed + 1))
    fi
    checked=$((checked + 1))
done

header "Lint: helpers python"
for f in "$workspace"/helpers/python/*.py; do
    [[ -f "$f" ]] || continue
    name="$(basename "$f")"
    if python3 -m py_compile "$f" 2>/dev/null; then
        log_info "  OK: $name"
    else
        error "  FAIL: $name"
        failed=$((failed + 1))
    fi
    checked=$((checked + 1))
done

# lib python
for f in "$workspace"/helpers/python/lib/*.py; do
    [[ -f "$f" ]] || continue
    name="$(basename "$f")"
    if python3 -m py_compile "$f" 2>/dev/null; then
        log_info "  OK: lib/$name"
    else
        error "  FAIL: lib/$name"
        failed=$((failed + 1))
    fi
    checked=$((checked + 1))
done

echo ""
if [[ $failed -eq 0 ]]; then
    success "Lint superado: $checked archivos, 0 errores."
else
    die "Lint fallido: $failed error(es) de $checked archivos."
fi

#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
# Validador de Conventional Commits para git hook commit-msg.
# Llamado por hooks.sh --action commit-msg.
#
# Regla 05: todo commit debe seguir Conventional Commits.
# Formato: type(scope)[!]: description
#
# Tipos válidos: feat|fix|docs|style|refactor|test|chore|build|ci|perf|revert
#
# Ignora: merge commits, initial commit, revert automático.
#
# Uso:
#   bash helpers/shell/commit-msg.sh <archivo-del-mensaje>
#   exit 0 → commit válido
#   exit 1 → commit rechazado
# ------------------------------------------------------------------

msg_file="${1:-}"
if [[ -z "$msg_file" || ! -f "$msg_file" ]]; then
	echo "commit-msg: no se recibió archivo de mensaje de commit" >&2
	exit 0
fi

msg="$(head -1 "$msg_file" 2>/dev/null || true)"

# Ignorar merges, revert automáticos e initial commit
if [[ "$msg" =~ ^Merge ]] || [[ "$msg" =~ ^Revert ]] || [[ "$msg" == "Revert "* ]]; then
	exit 0
fi
if echo "$msg" | grep -qE '^Initial commit'; then
	exit 0
fi

# Validar formato Conventional Commits
if echo "$msg" | grep -qE '^(feat|fix|docs|style|refactor|test|chore|build|ci|perf|revert)(\([a-zA-Z0-9._-]+\))?!?: .+'; then
	exit 0
fi

echo "" >&2
echo "ERROR: el mensaje de commit no sigue Conventional Commits." >&2
echo "" >&2
echo "Formato esperado: tipo[(scope)][!]: descripción" >&2
echo "Tipos válidos:    feat, fix, docs, style, refactor, test, chore," >&2
echo "                   build, ci, perf, revert" >&2
echo "" >&2
echo "Tu mensaje:       $msg" >&2
echo "" >&2
exit 1

#!/usr/bin/env python3
"""
audit.py — Auditoría de adopción de Ether Best Practices.
Evalúa un repositorio consumidor contra las reglas Definida.

CLI:  uv run python helpers/python/audit.py --path <dir> [--format markdown|json]
Módulo: importable desde audit_project (MCP tool).

Autocontenido: implementa list_rules + parse_frontmatter sin depender del MCP.
"""

import argparse
import json as mod_json
import os
import sys
from typing import Optional

# Resolver RULES_DIR desde el repo actual
ROOT = os.environ.get("MCP_ROOT", os.getcwd())
# Helpers inline (sin depender de lib/messages.py para portabilidad)
def _info(msg: str) -> None:
    print(f"[INFO]  {msg}", file=sys.stderr)

def _error(msg: str) -> None:
    print(f"[ERROR] {msg}", file=sys.stderr)

def _header(msg: str) -> None:
    line = "─" * len(msg)
    print(f"\n{msg}\n{line}", file=sys.stderr)


RULES_DIR = os.environ.get("RULES_DIR", os.path.join(ROOT, "rules"))


def list_rules_files() -> list[str]:
    """Lista archivos de reglas (NN-topic.md)."""
    if not os.path.isdir(RULES_DIR):
        return []
    return sorted(
        f for f in os.listdir(RULES_DIR)
        if f.endswith(".md") and f[0].isdigit() and os.path.isfile(os.path.join(RULES_DIR, f))
    )


def parse_frontmatter(filepath: str) -> dict:
    """Extrae frontmatter YAML de un archivo .md."""
    if not os.path.isfile(filepath):
        return {}
    with open(filepath) as f:
        content = f.read()
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        import yaml
        return yaml.safe_load(parts[1]) or {}
    except ImportError:
        # Fallback manual para id y status (mínimo, sin depender de PyYAML)
        fm = {}
        for line in parts[1].splitlines():
            line = line.strip()
            if line.startswith("id:"):
                fm["id"] = line.split(":", 1)[1].strip()
            elif line.startswith("status:"):
                fm["status"] = line.split(":", 1)[1].strip()
        return fm

# ---------------------------------------------------------------------------
# Matriz de auditoría: rule_id → lista de paths (relativos a la raíz del repo)
# Solo reglas status=Definida.
# Cada check es un path que DEBE existir para sumar puntos.
# ---------------------------------------------------------------------------
AUDIT_MATRIX: dict[str, list[str]] = {
    "build-tooling": [
        "Makefile", "Justfile",
        "helpers/mk", "helpers/shell", "helpers/just",
        "helpers/shell/lib",
    ],
    "ci": [
        "helpers/mk/container.mk",
        ".github/workflows",
    ],
    "agents-mcp": [
        "mcp-config.json",
    ],
    "stack": [
        "containers",
    ],
    "repository-structure": [
        "source/backend", "source/frontend", "source/shared",
        ".config",
    ],
    "githooks": [
        ".githooks", ".githooks/pre-commit", ".githooks/pre-push",
        ".githooks/commit-msg", "helpers/shell/hooks.sh",
    ],
    "commitizen": [
        ".config/commitizen/pyproject.toml", "CHANGELOG.md", "VERSION",
    ],
    "gitignore": [
        ".gitignore",
    ],
    "secrets": [
        ".sops.yaml", ".secrets",
    ],
    "config-files": [
        ".config/commitizen", ".config/mkdocs", ".config/sops",
    ],
    "script-reuse": [
        "helpers/shell/lib", "helpers/python/lib",
    ],
    "cd": [
        "helpers/just/cd.just", "helpers/just/github.just",
        ".github/workflows/release.yml",
    ],
}

# Labels for display
RULE_LABELS: dict[str, str] = {
    "build-tooling": "01 Build Tooling",
    "ci": "06 CI",
    "agents-mcp": "07 Agentes y MCP",
    "stack": "08 Stack Tecnológico",
    "repository-structure": "09 Estructura de Repositorio",
    "githooks": "10 Git Hooks",
    "commitizen": "11 Commitizen",
    "gitignore": "12 Gitignore",
    "secrets": "13 Gestión de Secretos",
    "config-files": "14 Archivos de Configuración",
    "script-reuse": "15 Reutilización de Scripts",
    "cd": "16 CD",
}

LEVEL_LABELS = {
    "Adoptado": "≥80% · Cumple la mayoría del estándar",
    "Parcial": "40–79% · Implementación en curso",
    "Mínimo": "<40% · Solo esqueleto inicial",
}


def score_level(ratio: float) -> str:
    if ratio >= 0.8:
        return "Adoptado"
    if ratio >= 0.4:
        return "Parcial"
    return "Mínimo"


def icon_from_ratio(ratio: float) -> str:
    if ratio >= 0.8:
        return "✅"
    if ratio >= 0.4:
        return "⚠️"
    return "❌"


def rules_defined() -> list[str]:
    """Retorna lista de rule_id con status=Definida desde frontmatter."""
    defined = []
    for fname in list_rules_files():
        fm = parse_frontmatter(os.path.join(RULES_DIR, fname))
        if fm.get("status") == "Definida":
            defined.append(fm.get("id", fname.replace(".md", "")))
    return defined


def audit_dir(target: str, ids: Optional[list[str]] = None) -> dict:
    """Audita un directorio, retorna {repo, global, level, rules: [...]}."""
    if ids is None:
        ids = rules_defined()
    if not os.path.isdir(target):
        return {"repo": target, "global": 0.0, "level": "Mínimo",
                "rules": [], "error": "Directorio no encontrado"}

    repo_name = os.path.basename(os.path.abspath(target))
    rule_scores = []
    total = 0
    max_score = 0

    for rid in ids:
        checks = AUDIT_MATRIX.get(rid, [])
        if not checks:
            continue
        found = 0
        check_details = []
        for path in checks:
            full = os.path.join(target, path)
            exists = os.path.isfile(full) or os.path.isdir(full)
            if exists:
                found += 1
            check_details.append((path, exists))

        ratio = found / len(checks) if checks else 0
        score = round(ratio * 3)  # 0-3
        rule_scores.append({
            "rule_id": rid,
            "label": RULE_LABELS.get(rid, rid),
            "score": score,
            "max": 3,
            "ratio": round(ratio, 2),
            "checks": check_details,
        })
        total += score
        max_score += 3

    global_ratio = total / max_score if max_score else 0
    level = score_level(global_ratio)
    has_items = [(r["rule_id"], r["label"], r["ratio"]) for r in rule_scores if r["ratio"] > 0]
    missing = [(r["rule_id"], r["label"]) for r in rule_scores if r["ratio"] == 0]

    return {
        "repo": repo_name,
        "global": round(global_ratio, 2),
        "global_pct": round(global_ratio * 100),
        "level": level,
        "total_rules": len(ids),
        "rules": rule_scores,
        "has": has_items,
        "missing": missing,
    }


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def render_markdown(audit: dict) -> str:
    lines = [
        f"# Auditoría de {audit['repo']} — Ether Best Practices",
        "",
        f"| | |",
        f"|---|---|",
        f"| **Adopción global** | **{audit['global_pct']}%** ({audit['total_rules']} reglas) |",
        f"| **Nivel** | **{audit['level']}** ({LEVEL_LABELS.get(audit['level'], '')}) |",
        "",
        "## Por regla",
        "",
    ]

    for r in audit["rules"]:
        icon = icon_from_ratio(r["ratio"])
        lines.append(f"{icon} **{r['label']}**: {r['score']}/{r['max']}")
        for path, exists in r["checks"]:
            mark = "✓" if exists else "✗"
            lines.append(f"  - {mark} `{path}`")
        lines.append("")

    # Lo que tiene
    if audit.get("has"):
        lines.append("## Lo que tiene")
        for rid, label, _ratio in audit["has"]:
            lines.append(f"- {label}")
        lines.append("")

    # Lo que falta (priorizado)
    if audit.get("missing"):
        lines.append("## Lo que falta")
        for rid, label in audit["missing"]:
            lines.append(f"- {label} — ver `get_rule(\"{rid}\")`")
        lines.append("")

    # Recomendaciones
    lines.append("## Recomendaciones")
    lines.append(f"Nivel actual: **{audit['level']}**. ")
    if audit["level"] == "Mínimo":
        lines.append("Prioriza las reglas de `Lo que falta` comenzando por 01-build-tooling y 09-repository-structure como base.")
    elif audit["level"] == "Parcial":
        lines.append("Cubre las reglas ausentes de `Lo que falta`. Usa `scaffold_project` para generar cascarón, o consulta cada regla con `get_rule(id)`.")
    else:
        lines.append("Buena adopción. Revisa las reglas con puntaje parcial (`get_rule(id)`) para alcanzar el máximo.")

    return "\n".join(lines)


def render_json(audit: dict) -> str:
    return mod_json.dumps(audit, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Main (CLI)
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Auditar adopción de Ether Best Practices en un repositorio"
    )
    parser.add_argument("--path", default=".", help="Ruta al repositorio a auditar")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json"],
                        help="Formato de salida")
    parser.add_argument("--log-file", help="Ruta de auditoría")
    args = parser.parse_args()

    _header("Auditoría Ether Best Practices")
    defined_ids = rules_defined()
    _info(f"{len(defined_ids)} reglas Definida encontradas")

    result = audit_dir(args.path, ids=defined_ids)
    if "error" in result:
        _error(result["error"])
        sys.exit(1)

    if args.format == "json":
        print(render_json(result))
    else:
        print(render_markdown(result))

    _info(f"Auditoría completada — Nivel: {result['level']} ({result['global_pct']}%)")


if __name__ == "__main__":
    main()

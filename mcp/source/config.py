"""
config.py — Rutas y utilidades para el servidor MCP ether-rules.
Reutiliza el patrón de commons.py (regla 15).
"""

import os
import sys
from typing import Optional

ROOT = os.environ.get("MCP_ROOT", os.getcwd())
RULES_DIR = os.environ.get("RULES_DIR", os.path.join(ROOT, "rules"))
TEMPLATES_DIR = os.environ.get("TEMPLATES_DIR", os.path.join(ROOT, "templates"))
GITIGNORE_DIR = os.path.join(TEMPLATES_DIR, "gitignore")
HELPERS_DIR = os.environ.get("HELPERS_DIR", os.path.join(ROOT, "helpers"))
REPO_STRUCTURE_DIR = os.path.join(TEMPLATES_DIR, "repository-structure")
DOCS_DIR = os.environ.get("DOCS_DIR", os.path.join(ROOT, "docs"))


def resolve(relative: str) -> str:
    """Resuelve ruta relativa a ROOT."""
    return os.path.join(ROOT, relative)


def list_rules_files() -> list[str]:
    """Lista todos los archivos de reglas (NN-topic.md)."""
    files = sorted(
        f
        for f in os.listdir(RULES_DIR)
        if f.endswith(".md") and f[0].isdigit()
    )
    return files


def parse_frontmatter(filepath: str) -> dict:
    """Extrae frontmatter YAML de un archivo .md con --- delimiters."""
    if not os.path.isfile(filepath):
        return {}
    with open(filepath) as f:
        content = f.read()
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    import yaml  # type: ignore

    return yaml.safe_load(parts[1]) or {}


def list_all_templates() -> list[str]:
    """Lista todos los templates globales (repository-structure, gitignore, rule-template)."""
    templates = []
    skip_dirs = {".githooks", "site", ".venv", "__pycache__"}
    for root, dirs, files in os.walk(TEMPLATES_DIR):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            if f == ".gitkeep" or f == ".DS_Store":
                continue
            rel = os.path.relpath(os.path.join(root, f), TEMPLATES_DIR)
            templates.append(rel)
    return sorted(templates)


from typing import Optional


def find_rule_by_id(rule_id: str) -> Optional[str]:
    """Encuentra archivo de regla por id exacto de frontmatter, fallback a filename."""
    for fname in list_rules_files():
        # Match exacto por frontmatter id
        fm = parse_frontmatter(os.path.join(RULES_DIR, fname))
        if fm.get("id") == rule_id:
            return fname
    # Fallback: substring en filename
    for fname in list_rules_files():
        if rule_id in fname:
            return fname
    return None


def templates_index() -> str:
    """Genera un índice global de templates agrupado por dominio."""
    lines = [
        "# Índice de Templates",
        "",
        "## repository-structure (cascarón completo del proyecto)",
    ]
    for f in list_all_templates():
        if f.startswith("repository-structure/"):
            name = f.replace("repository-structure/", "")
            lines.append(f"- repository-structure/{name}")
    lines.append("")
    lines.append("## gitignore (biblioteca por contexto)")
    for f in list_all_templates():
        if f.startswith("gitignore/"):
            name = f.replace("gitignore/", "")
            lines.append(f"- gitignore/{name}")
    lines.append("")
    lines.append("## rule-template (template para crear reglas)")
    for f in list_all_templates():
        if f.startswith("rule-template"):
            lines.append(f"- {f}")
    return "\n".join(lines)

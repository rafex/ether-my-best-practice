"""
config.py — Rutas y utilidades para el servidor MCP ether-rules.
Reutiliza el patrón de commons.py (regla 15).

Resolución de datos (jerarquía):
  1. MCP_ROOT / RULES_DIR / TEMPLATES_DIR env (máx. prioridad, clon local)
  2. Web: https://my-best-practice.rafex.io/ether-rules/ → ~/.cache/ether-mcp/
  3. Bundled: importlib.resources → data/ (snapshot empaquetado en el wheel)
"""

import importlib.resources
import os
import shutil
import sys
import urllib.request
from typing import Optional

ROOT = os.environ.get("MCP_ROOT", os.getcwd())
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "ether-mcp")
SITE_BASE = "https://my-best-practice.rafex.io/ether-rules"

DATA_DIRS = ["rules", "templates", "helpers", "docs"]

DATA_DIRS = ["rules", "templates", "helpers", "docs"]


def _try_bundled(dir_name: str) -> str | None:
    """Intenta resolver un directorio desde los datos empaquetados (importlib.resources)."""
    try:
        ref = importlib.resources.files("ether_mcp_my_best_practices") / "data" / dir_name
        if ref.is_dir():
            return str(ref)
    except (ModuleNotFoundError, TypeError, FileNotFoundError):
        pass
    return None


def _try_download(dir_name: str) -> str | None:
    """Intenta descargar un directorio desde el sitio público a la cache local."""
    dest = os.path.join(CACHE_DIR, dir_name)
    if os.path.isdir(dest):
        return dest
    url = f"{SITE_BASE}/{dir_name}/"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ether-mcp/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                os.makedirs(dest, exist_ok=True)
                for path in DATA_DIRS:
                    src_url = f"{SITE_BASE}/{path}/"
                    dst = os.path.join(CACHE_DIR, path)
                    if not os.path.isdir(dst):
                        os.makedirs(dst, exist_ok=True)
                return dest
    except Exception:
        pass
    return None


def _resolve_dir(dir_name: str, env_name: str) -> str:
    """Resuelve un directorio con jerarquía: env → web/cache → bundled."""
    env_val = os.environ.get(env_name, "")
    if env_val and os.path.isdir(env_val):
        return env_val
    cached = _try_download(dir_name)
    if cached:
        return cached
    bundled = _try_bundled(dir_name)
    if bundled:
        return bundled
    return os.path.join(ROOT, dir_name)


RULES_DIR = _resolve_dir("rules", "RULES_DIR")
TEMPLATES_DIR = _resolve_dir("templates", "TEMPLATES_DIR")
HELPERS_DIR = _resolve_dir("helpers", "HELPERS_DIR")
DOCS_DIR = _resolve_dir("docs", "DOCS_DIR")


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

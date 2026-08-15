"""
config.py — Rutas y utilidades para el servidor MCP ether-rules.
Reutiliza el patrón de commons.py (regla 15).

Resolución de datos (jerarquía):
  1. RULES_DIR / TEMPLATES_DIR / HELPERS_DIR / DOCS_DIR env (override explícito)
  2. Web (remoto): descarga desde RULES_REMOTE_URL usando checksums.json
     → ~/.cache/ether-mcp/ (solo archivos nuevos o con hash distinto)
  3. Bundled: importlib.resources → data/ (snapshot empaquetado en el wheel)
  4. MCP_ROOT / <dir> (clon local del repositorio)
"""

import importlib.resources
import json
import os
import shutil
import sys
import urllib.request
from typing import Optional

from ether_mcp_my_best_practices.lib.commons import content_hash

ROOT = os.environ.get("MCP_ROOT", os.getcwd())
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "ether-mcp")
REMOTE_BASE = os.environ.get(
    "RULES_REMOTE_URL",
    "https://my-best-practice.rafex.io/ether-rules",
)
MANIFEST_NAME = "checksums.json"
HTTP_TIMEOUT = 8
USER_AGENT = "ether-mcp/1.0"

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


def _http_get(url: str) -> bytes:
    """GET de una URL con timeout y headers. Lanza excepción si falla."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status} para {url}")
        return resp.read()


_MANIFEST_CACHE: Optional[dict[str, str]] = None


def _fetch_manifest() -> dict[str, str]:
    """Descarga checksums.json remoto y devuelve el mapa {rel_path: sha256}.

    El resultado se memoiza a nivel de módulo: se descarga una sola vez por
    proceso (las cuatro llamadas de _resolve_dir comparten el mismo manifest).
    """
    global _MANIFEST_CACHE
    if _MANIFEST_CACHE is not None:
        return _MANIFEST_CACHE
    data = _http_get(f"{REMOTE_BASE}/{MANIFEST_NAME}")
    obj = json.loads(data.decode("utf-8"))
    _MANIFEST_CACHE = obj.get("files", {})
    return _MANIFEST_CACHE


def _safe_rel(rel_path: str) -> bool:
    """Rechaza rutas con traversal o absolutas."""
    if rel_path.startswith("/") or ".." in rel_path.split("/"):
        return False
    return True


def _cache_path(rel_path: str) -> str:
    return os.path.join(CACHE_DIR, rel_path)


def _is_up_to_date(rel_path: str, expected: str) -> bool:
    """True si el archivo en caché coincide con el hash esperado."""
    dest = _cache_path(rel_path)
    if not os.path.isfile(dest):
        return False
    try:
        with open(dest, "rb") as f:
            local = f.read().decode("utf-8", errors="replace")
    except OSError:
        return False
    return content_hash(rel_path, local) == expected


def _try_download(dir_name: str) -> str | None:
    """Sincroniza un directorio desde el remoto a la caché, por checksum.

    Descarga el manifest y, para cada archivo bajo dir_name/, solo descarga
    los que faltan o cuyo hash cambió. Devuelve la ruta cacheada si al final
    hay al menos un archivo; si no, None (→ fallback a bundled).
    """
    try:
        manifest = _fetch_manifest()
    except Exception:
        return None

    prefix = f"{dir_name}/"
    targets = [p for p in manifest if p.startswith(prefix) and _safe_rel(p)]
    if not targets:
        return None

    for rel in targets:
        expected = manifest[rel]
        if _is_up_to_date(rel, expected):
            continue
        try:
            data = _http_get(f"{REMOTE_BASE}/{rel}")
        except Exception:
            continue
        dest = _cache_path(rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as f:
            f.write(data)

    dest_dir = os.path.join(CACHE_DIR, dir_name)
    if os.path.isdir(dest_dir) and os.listdir(dest_dir):
        return dest_dir
    return None


def _resolve_dir(dir_name: str, env_name: str) -> str:
    """Resuelve un directorio con jerarquía: env → web → bundled → MCP_ROOT."""
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

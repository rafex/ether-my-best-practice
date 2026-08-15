#!/usr/bin/env python3
"""
commons.py — Utilidades comunes para helpers Python.

Proporciona: PROJECT_ROOT, sys.path con lib, wrapper argparse,
utilidades de rutas, ejecución de subprocesos.

Para agentes de IA: importar esta lib al inicio de cualquier helper
Python para obtener el entorno base y evitar duplicación.
"""

import argparse
import hashlib
import os
import re
import subprocess
import sys
from typing import Optional

PROJECT_ROOT = os.getcwd()

# Añadir el directorio lib al path para imports locales
_LIB_DIR = os.path.dirname(os.path.abspath(__file__))
if _LIB_DIR not in sys.path:
    sys.path.insert(0, _LIB_DIR)


def add_common_args(parser: argparse.ArgumentParser) -> None:
    """Añade flags comunes a un ArgumentParser."""
    parser.add_argument("--log-file", help="Ruta del log de auditoría")
    parser.add_argument("--log-level", default="info", help="Nivel de log (info, debug)")
    parser.add_argument("--workspace", default=PROJECT_ROOT, help="Directorio del proyecto")


def resolve_path(relative: str) -> str:
    """Resuelve ruta relativa al PROJECT_ROOT."""
    return os.path.join(PROJECT_ROOT, relative)


def ensure_dir(path: str) -> None:
    """Crea un directorio si no existe."""
    os.makedirs(path, exist_ok=True)


def run_cmd(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Ejecuta un comando de sistema con subprocess.run."""
    return subprocess.run(cmd, capture_output=False, text=True, check=check)


# ---------------------------------------------------------------------------
# Checksums de contenido (regla 17 — detección de cambios para el MCP)
# ---------------------------------------------------------------------------

CHECKSUM_LINE_RE = re.compile(r"^checksum:\s*.*$")


def split_frontmatter(text: str) -> tuple[Optional[str], str]:
    """Separa frontmatter YAML de un markdown.

    Devuelve (header, body) donde header incluye las líneas de apertura y
    cierre `---` (con saltos de línea). Si no hay frontmatter, (None, text).
    """
    if not text.startswith("---"):
        return None, text
    lines = text.splitlines(keepends=True)
    if len(lines) < 2:
        return None, text
    for i in range(1, len(lines)):
        if lines[i].rstrip("\n").rstrip("\r") == "---":
            return "".join(lines[: i + 1]), "".join(lines[i + 1:])
    return None, text


def content_hash(rel_path: str, text: str) -> str:
    """Hash sha256 estable de un archivo por ruta relativa.

    Para reglas (`rules/*.md`) el hash excluye el campo `checksum` del
    frontmatter, de modo que sea idempotente tras incrustar el propio hash.
    Para el resto de archivos (templates, helpers, docs) el hash es del
    contenido completo.
    """
    if rel_path.startswith("rules/") and rel_path.endswith(".md"):
        header, body = split_frontmatter(text)
        if header is not None:
            filtered = "".join(
                ln for ln in header.splitlines(keepends=True)
                if not CHECKSUM_LINE_RE.match(ln.rstrip("\n").rstrip("\r"))
            )
            text = filtered + body
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def inject_checksum(text: str, checksum: str) -> str:
    """Inserta (o reemplaza) el campo `checksum` en el frontmatter.

    Devuelve el texto sin cambios si el archivo no tiene frontmatter.
    """
    header, body = split_frontmatter(text)
    if header is None:
        return text
    header_lines = header.splitlines(keepends=True)
    inner = [
        ln for ln in header_lines[1:-1]
        if not CHECKSUM_LINE_RE.match(ln.rstrip("\n").rstrip("\r"))
    ]
    new_header = "".join([
        header_lines[0],
        *inner,
        f"checksum: {checksum}\n",
        header_lines[-1],
    ])
    return new_header + body

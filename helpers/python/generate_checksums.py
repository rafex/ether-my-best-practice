#!/usr/bin/env python3
"""
generate_checksums.py — Genera checksums de contenido + manifest para el MCP.

Recorre rules/, templates/, helpers/ y docs/ y produce `checksums.json` en la
raíz del repositorio. Para las reglas (rules/*.md con frontmatter YAML) además
incrusta el hash en el propio frontmatter (`checksum: <sha256>`), de modo que
cada regla conozca su propia firma y el MCP pueda detectar actualizaciones
remotas sin re-descargar todo el árbol.

Uso:
    uv run python helpers/python/generate_checksums.py
    uv run python helpers/python/generate_checksums.py --root <repo> --out checksums.json

Reutiliza helpers/python/lib/commons.py (regla 15).
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from lib.commons import content_hash, inject_checksum, split_frontmatter  # noqa: E402

DATA_DIRS = ["rules", "templates", "helpers", "docs"]
SKIP_DIRS = {
    ".git", "site", "dist", "__pycache__", ".venv", "venv",
    "node_modules", "build", ".mypy_cache", ".pytest_cache",
}
SKIP_FILES = {".gitkeep", ".DS_Store"}
SKIP_PREFIXES = ("docs/rules/",)


def walk_files(root: str):
    """Genera (rel_path, full_path) para todos los archivos gestionados."""
    for d in DATA_DIRS:
        base = os.path.join(root, d)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [x for x in dirnames if x not in SKIP_DIRS]
            for fn in sorted(filenames):
                if fn in SKIP_FILES:
                    continue
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, root)
                if rel.startswith(SKIP_PREFIXES):
                    continue
                yield rel, full


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera checksums y manifest")
    parser.add_argument("--root", default=os.getcwd(), help="Raíz del repositorio")
    parser.add_argument("--out", default="checksums.json", help="Ruta del manifest")
    args = parser.parse_args()

    root = args.root
    manifest: dict[str, str] = {}
    injected = 0

    for rel, full in walk_files(root):
        with open(full, "rb") as f:
            raw = f.read()
        text = raw.decode("utf-8", errors="replace")

        if rel.startswith("rules/") and rel.endswith(".md") and text.startswith("---"):
            header, _body = split_frontmatter(text)
            if header is not None:
                checksum = content_hash(rel, text)
                new_text = inject_checksum(text, checksum)
                if new_text != text:
                    with open(full, "w") as f:
                        f.write(new_text)
                    text = new_text
                    injected += 1

        manifest[rel] = content_hash(rel, text)

    version = ""
    vpath = os.path.join(root, "VERSION")
    if os.path.isfile(vpath):
        with open(vpath) as f:
            version = f.read().strip()

    doc = {
        "version": version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": manifest,
    }
    out = os.path.join(root, args.out)
    with open(out, "w") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"checksums.json generado: {len(manifest)} archivos "
          f"({injected} reglas con checksum incrustado, version {version or 'n/a'}).")


if __name__ == "__main__":
    main()

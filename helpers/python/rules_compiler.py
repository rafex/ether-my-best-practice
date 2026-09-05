#!/usr/bin/env python3
"""
rules_compiler.py — Compilador de Reglas (motor determinista AST).

Parse, validate, render y crear reglas tipadas con bloques estructurados.
Reutiliza helpers/python/lib/ (regla 15).

Uso:
    uv run python helpers/python/rules_compiler.py --action parse <rule_id>
    uv run python helpers/python/rules_compiler.py --action validate --all
    uv run python helpers/python/rules_compiler.py --action render <rule_id> --in-place
    uv run python helpers/python/rules_compiler.py --action new --slug nn-topic --title "Titulo"
"""

import argparse
import os
import re
import sys
from typing import Optional

import yaml  # type: ignore

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from lib.logs import get_logger
from lib.messages import success, error, warning, info, die, step

log = get_logger("rules-compiler")


class RuleCompilerError(ValueError):
    """Error determinista al leer o interpretar una regla."""

RULES_DIR = os.environ.get("RULES_DIR", os.path.join(os.getcwd(), "rules"))
TEMPLATE_PATH = os.path.join(os.environ.get("TEMPLATES_DIR", os.path.join(os.getcwd(), "templates")),
                             "rule-template.md.tmpl")

# ---------------------------------------------------------------------------
# Taxonomía de 14 tipos
# ---------------------------------------------------------------------------
MANDATORY_TYPES = {"Premisa", "Restriccion", "Ejemplo", "Referencia"}
OPTIONAL_TYPES = {
    "Estructura", "Diagrama", "Comando", "Nombre Sugerido", "Plantilla",
    "Comportamiento", "Sugerencia", "Flujo", "Contrato", "Matriz",
}
ALL_TYPES = MANDATORY_TYPES | OPTIONAL_TYPES

BLOCK_HEADER_RE = re.compile(r"^(#{2,6})\s+([^:\n]+):\s*(.*)$")
TAGS_RE = re.compile(r"^tags:\s*\[(.*)\]$")


def _typed_header(line: str) -> Optional[tuple[str, str, str]]:
    """Retorna un encabezado tipado solo si el tipo pertenece a la taxonomía."""
    match = BLOCK_HEADER_RE.match(line)
    if not match:
        return None
    level, block_type, name = match.groups()
    block_type = block_type.strip()
    if block_type not in ALL_TYPES:
        return None
    return level, block_type, name.strip()


def _update_fence(line: str, fence: Optional[str]) -> Optional[str]:
    """Actualiza el estado de un fence Markdown simple (``` o ~~~)."""
    stripped = line.lstrip()
    if fence is None:
        if stripped.startswith("```"):
            return "```"
        if stripped.startswith("~~~"):
            return "~~~"
        return None
    if stripped.startswith(fence):
        return None
    return fence

# ---------------------------------------------------------------------------
# AST
# ---------------------------------------------------------------------------

class RuleAST:
    """Representa una regla como AST."""
    def __init__(self):
        self.id: str = ""
        self.title: str = ""
        self.status: str = ""
        self.tags: list[str] = []
        self.heading: str = ""
        self.blocks: list[dict] = []
        self.filepath: str = ""


def parse_frontmatter_and_heading(text: str) -> tuple[dict, str]:
    """Extrae frontmatter YAML y el heading (# Regla NN: ...)."""
    fm = {}
    body = text
    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == "---":
        closing = next(
            (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
            None,
        )
        if closing is None:
            raise RuleCompilerError("frontmatter sin delimitador de cierre '---'")
        raw_frontmatter = "".join(lines[1:closing])
        try:
            parsed = yaml.safe_load(raw_frontmatter)
        except yaml.YAMLError as exc:
            raise RuleCompilerError(f"frontmatter YAML inválido: {exc}") from exc
        if parsed is not None and not isinstance(parsed, dict):
            raise RuleCompilerError("frontmatter YAML debe ser un mapa")
        fm = parsed or {}
        body = "".join(lines[closing + 1:])

    heading = ""
    m = re.search(r"^(# .+)", body, re.MULTILINE)
    if m:
        heading = m.group(1).strip()
    return fm, heading


def parse_blocks(text: str) -> list[dict]:
    """Extrae bloques tipados: ### Tipo: Nombre + contenido + tags."""
    blocks = []
    lines = text.splitlines()
    i = 0
    fence = None
    while i < len(lines):
        if fence is not None:
            fence = _update_fence(lines[i], fence)
            i += 1
            continue

        header = _typed_header(lines[i])
        if header:
            level, block_type, name = header
            content_lines = []
            i += 1
            block_tags = []
            block_fence = None
            while i < len(lines):
                if block_fence is None and _typed_header(lines[i]):
                    break
                tag_m = TAGS_RE.match(lines[i]) if block_fence is None else None
                if tag_m and not block_fence:
                    block_tags = [t.strip() for t in tag_m.group(1).split(",") if t.strip()]
                    i += 1
                    break
                content_lines.append(lines[i])
                block_fence = _update_fence(lines[i], block_fence)
                i += 1
            content = "\n".join(content_lines).strip()
            blocks.append({
                "type": block_type,
                "name": name,
                "content": content,
                "tags": block_tags,
            })
        else:
            fence = _update_fence(lines[i], fence)
            i += 1
    return blocks


def parse_rule(filepath: str) -> Optional[RuleAST]:
    """Parse un archivo de regla completo → AST."""
    if not os.path.isfile(filepath):
        return None
    with open(filepath, encoding="utf-8") as f:
        text = f.read()
    fm, heading = parse_frontmatter_and_heading(text)
    ast = RuleAST()
    ast.filepath = filepath
    ast.id = fm.get("id", "")
    ast.title = fm.get("title", "")
    ast.status = fm.get("status", "")
    ast.tags = fm.get("tags")
    ast.heading = heading
    ast.blocks = parse_blocks(text)
    return ast


# ---------------------------------------------------------------------------
# Validate
# ---------------------------------------------------------------------------

def validate_ast(ast: RuleAST) -> list[str]:
    """Valida un AST. Retorna lista de errores (vacíos = OK)."""
    errs = []
    base = os.path.basename(ast.filepath) if ast.filepath else "?"

    if not isinstance(ast.id, str) or not ast.id.strip():
        errs.append(f"{base}: falta id en frontmatter")
    if not isinstance(ast.title, str) or not ast.title.strip():
        errs.append(f"{base}: falta title en frontmatter")
    if ast.status not in ("Definida", "Borrador"):
        errs.append(f"{base}: status inválido '{ast.status}'")
    if not isinstance(ast.tags, list):
        errs.append(f"{base}: tags debe ser una lista en frontmatter")
    elif not all(isinstance(tag, str) for tag in ast.tags):
        errs.append(f"{base}: todos los tags deben ser texto")
    if not ast.heading:
        errs.append(f"{base}: falta título H1")

    # Warnings de convención para reglas Borrador
    # Solo se aplican si el archivo es una regla (no 00-index ni DEFINITION)
    if ast.status == "Borrador":
        if not base.startswith("00-") and not base.startswith("DEFINITION"):
            if not base.endswith("_draft.md"):
                errs.append(f"WARNING {base}: Borrador debería nombrarse NN-topic_draft.md")
            if "Borrador" not in ast.heading:
                errs.append(f"WARNING {base}: título H1 debería llevar '— ⚠️ *Borrador*'")

    if not ast.blocks:
        errs.append(f"{base}: sin bloques tipados")
        return errs

    found_types = {b["type"] for b in ast.blocks}

    # Presencia de tipos obligatorios
    for t in MANDATORY_TYPES:
        if t not in found_types:
            errs.append(f"{base}: falta tipo obligatorio '{t}'")

    # Validar cada bloque
    for b in ast.blocks:
        t = b["type"]
        if t not in ALL_TYPES:
            errs.append(f"{base}: tipo desconocido '{t}' (¿typo?)")
        if not b["name"]:
            errs.append(f"{base}: bloque '{t}' sin nombre")
        if not b["content"]:
            errs.append(f"{base}: bloque '{t} :: {b['name']}' sin contenido")
        for tag in b.get("tags", []):
            if tag in ("obligatorio", "opcional", "recomendado", "deprecado"):
                continue
            # temáticos libres — sin restricción

    # Madurez
    if ast.status == "Definida":
        if "Comando" not in found_types:
            errs.append(f"{base}: Definida requiere ≥1 bloque 'Comando'")
        if "Estructura" not in found_types and "Diagrama" not in found_types:
            errs.append(f"{base}: Definida requiere ≥1 bloque 'Estructura' o 'Diagrama'")

    return errs


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def render_rule(ast: RuleAST) -> str:
    """AST → Markdown normalizado."""
    lines = []
    lines.append("---")
    lines.append(f"id: {ast.id}")
    lines.append(f"title: {ast.title}")
    lines.append(f"status: {ast.status}")
    lines.append(f"tags: [{', '.join(ast.tags)}]")
    lines.append("---")
    lines.append("")
    lines.append(ast.heading)
    lines.append("")

    for b in ast.blocks:
        lines.append(f"### {b['type']}: {b['name']}")
        lines.append("")
        lines.append(b["content"])
        if b.get("tags"):
            lines.append("")
            lines.append(f"tags: [{', '.join(b['tags'])}]")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# New
# ---------------------------------------------------------------------------

def create_new_rule(slug: str, title: str, log_file: str = "") -> str:
    """Genera una regla nueva desde la plantilla."""
    if (
        not slug
        or os.path.isabs(slug)
        or "/" in slug
        or "\\" in slug
        or os.path.normpath(slug) != slug
        or slug in {".", ".."}
    ):
        raise RuleCompilerError(f"slug inseguro: {slug!r}")

    num = slug.split("-")[0] if "-" in slug else slug
    dest = os.path.join(RULES_DIR, f"{slug}.md")
    if os.path.exists(dest):
        return f"La regla {slug} ya existe."

    template_content = ""
    if os.path.isfile(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, encoding="utf-8") as f:
            template_content = f.read()
    else:
        template_content = f"""---
id: {slug}
title: {title}
status: Borrador
tags: []
---

# Regla {num}: {title}

### Premisa: Descripción

> Por qué existe esta regla.

tags: [obligatorio]

### Restriccion: Prohibición

> Qué **NO** se debe hacer.

tags: [obligatorio]

### Ejemplo: Ejemplo correcto

```shell
# Ejemplo
```

tags: [obligatorio]

### Referencia: Referencias

- [Regla XX](XX-topic.md)

tags: [obligatorio]
"""

    content = template_content.replace("nn-topic", slug)
    content = content.replace(f"Regla NN", f"Regla {num}")
    content = content.replace(f"Título descriptivo", title)
    content = content.replace(f"id: nn-topic", f"id: {slug}")

    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Regla {slug} creada en {dest}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Rules Compiler — AST de reglas tipadas")
    parser.add_argument("--action", required=True,
                        choices=["parse", "validate", "render", "new"])
    parser.add_argument("rule_id", nargs="?", default=None, help="ID de regla o 'all'")
    parser.add_argument("--all", action="store_true", help="Procesar todas las reglas")
    parser.add_argument("--in-place", action="store_true", help="Render in-place")
    parser.add_argument("--slug", help="Slug para nueva regla (--action new)")
    parser.add_argument("--title", help="Título para nueva regla (--action new)")
    parser.add_argument("--log-file", help="Ruta de auditoría")
    args = parser.parse_args()

    targets = []
    if args.all:
        rules_dir = RULES_DIR
        for f in sorted(os.listdir(rules_dir)):
            if f.endswith(".md") and f[0].isdigit() and f != "00-index.md" and os.path.isfile(os.path.join(rules_dir, f)):
                targets.append(f)
    elif args.rule_id:
        targets = [args.rule_id]

    if args.action == "new":
        try:
            result = create_new_rule(args.slug or "nn-topic", args.title or "Título")
        except (OSError, RuleCompilerError) as exc:
            die(f"No se pudo crear la regla: {exc}")
        print(result)
        return

    step(1, len(targets) or 1, f"Acción: {args.action}")
    total_errors = 0
    found = False

    for rid in (targets or []):
        if not rid:
            continue
        if rid.endswith(".md"):
            filepath = os.path.join(RULES_DIR, rid)
        else:
            filepath = os.path.join(RULES_DIR, rid + ".md") if "." not in rid else None
            if filepath is None or not os.path.isfile(filepath):
                for f in os.listdir(RULES_DIR):
                    if rid in f and f.endswith(".md") and f[0].isdigit():
                        filepath = os.path.join(RULES_DIR, f)
                        break
                if filepath is None or not os.path.isfile(filepath):
                    error(f"No se encontró la regla: {rid}")
                    continue

        try:
            ast = parse_rule(filepath)
        except (OSError, UnicodeError, RuleCompilerError) as exc:
            error(f"No se pudo parsear {filepath}: {exc}")
            total_errors += 1
            continue
        if ast is None:
            error(f"No se pudo parsear: {filepath}")
            total_errors += 1
            continue
        found = True

        if args.action == "parse":
            import json
            print(json.dumps({
                "id": ast.id, "title": ast.title, "status": ast.status,
                "tags": ast.tags, "heading": ast.heading,
                "blocks": ast.blocks,
            }, indent=2, ensure_ascii=False))
        elif args.action == "validate":
            errs = validate_ast(ast)
            fatal = [e for e in errs if not e.startswith("WARNING ")]
            for e in errs:
                (warning if e.startswith("WARNING ") else error)(e)
            if fatal:
                total_errors += 1
            else:
                info(f"  {os.path.basename(filepath)}: OK")
        elif args.action == "render":
            rendered = render_rule(ast)
            if args.in_place:
                with open(filepath, "w") as f:
                    f.write(rendered)
                success(f"  {os.path.basename(filepath)}: rendered in-place")
            else:
                print(rendered)

    if not found and args.action != "new":
        error(f"No se encontraron reglas para: {args.rule_id or ''}")
        total_errors += 1

    if args.action == "validate" and total_errors > 0:
        die(f"Validación fallida: {total_errors} error(es).")
    elif args.action == "validate":
        success(f"Validación superada: {len(targets)} regla(s) OK.")


if __name__ == "__main__":
    main()

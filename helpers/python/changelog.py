#!/usr/bin/env python3
"""
Genera CHANGELOG.md a partir de Conventional Commits desde el último tag.

Se usa en release-time (just prepare-release), no en hooks.
Stdlib de Python 3.12+, sin dependencias externas.

Ejemplo de uso:
    uv run python helpers/python/changelog.py
    uv run python helpers/python/changelog.py --output CHANGELOG.md

La salida se agrupa por tipo de commit:
    feat → Added, fix → Fixed, docs → Docs, style/refactor → Changed,
    test → Tests, build/ci/chore/perf → Internal
"""

import argparse
import datetime
import re
import subprocess
import sys


def run_git_log(since_tag: str) -> str:
    """Obtiene git log desde la última etiqueta hasta HEAD."""
    cmd = ["git", "log", "--pretty=format:%s", f"{since_tag}..HEAD"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return ""


def get_latest_tag() -> str:
    """Obtiene la etiqueta más reciente, o el commit inicial si no hay."""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        # Sin tags: tomamos todos los commits desde el primero
        try:
            result = subprocess.run(
                ["git", "rev-list", "--max-parents=0", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()[:7]
        except subprocess.CalledProcessError:
            return "HEAD"


def parse_commits(log: str) -> dict[str, list[str]]:
    """Clasifica líneas de commit por tipo."""
    groups: dict[str, list[str]] = {
        "Added": [],
        "Fixed": [],
        "Docs": [],
        "Changed": [],
        "Tests": [],
        "Internal": [],
    }

    pattern = re.compile(
        r'^(feat|fix|docs|style|refactor|test|chore|build|ci|perf|revert)'
        r'(\([^)]*\))?!?:\s*(.+)'
    )

    for line in log.splitlines():
        line = line.strip()
        match = pattern.match(line)
        if not match:
            continue
        typ, _scope, desc = match.groups()
        entry = f"- {desc}"

        category = {
            "feat": "Added",
            "fix": "Fixed",
            "docs": "Docs",
            "style": "Changed",
            "refactor": "Changed",
            "test": "Tests",
            "build": "Internal",
            "ci": "Internal",
            "chore": "Internal",
            "perf": "Internal",
            "revert": "Internal",
        }.get(typ, "Internal")

        groups[category].append(entry)

    return groups


def generate_changelog(groups: dict[str, list[str]], version: str) -> str:
    """Genera el contenido de CHANGELOG.md."""
    today = datetime.date.today().isoformat()
    lines = [
        "# Changelog",
        "",
        f"## [{version}] — {today}",
        "",
    ]
    for section in ["Added", "Fixed", "Changed", "Deprecated", "Removed",
                    "Fixed", "Tests", "Docs", "Internal"]:
        if section in groups and groups[section]:
            lines.append(f"### {section}")
            lines.extend(groups[section])
            lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate CHANGELOG.md from Conventional Commits"
    )
    parser.add_argument(
        "--output", default="CHANGELOG.md", help="Output file (default: CHANGELOG.md)"
    )
    parser.add_argument(
        "--version", default=None, help="Version to tag (default: from VERSION file)"
    )
    args = parser.parse_args()

    version = args.version
    if version is None:
        try:
            with open("VERSION") as f:
                version = f.read().strip()
        except FileNotFoundError:
            version = "0.0.0"

    # Si ya existe CHANGELOG.md, preservar el contenido anterior y pre-agregar
    existing = ""
    output_path = args.output
    try:
        with open(output_path) as f:
            content = f.read()
            # Extraer todo después del primer ## header (contenido previo)
            idx = content.find("\n## ")
            if idx > 0:
                existing = content[idx + 1 :]  # sin el \n inicial
    except FileNotFoundError:
        pass

    since = get_latest_tag()
    log = run_git_log(since)
    groups = parse_commits(log)

    new_section = generate_changelog(groups, version)

    if existing:
        # Insertar la nueva entrada después del header de Changelog
        header_end = new_section.find("\n## ")
        if header_end > 0:
            result = new_section[:header_end] + "\n\n" + existing
        else:
            result = new_section + "\n" + existing
    else:
        result = new_section

    with open(output_path, "w") as f:
        f.write(result)

    print(f"CHANGELOG.md generated (version {version}, changes since {since})")


if __name__ == "__main__":
    main()

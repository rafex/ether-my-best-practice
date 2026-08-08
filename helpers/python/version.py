#!/usr/bin/env python3
"""
Lee y actualiza el archivo VERSION del proyecto.

Se usa en release-time (just prepare-release), no en hooks.
Stdlib de Python 3.12+, sin dependencias externas.

Ejemplos de uso:
    uv run python helpers/python/version.py             # leer versión actual
    uv run python helpers/python/version.py --bump patch
    uv run python helpers/python/version.py --bump minor
    uv run python helpers/python/version.py --bump major
    uv run python helpers/python/version.py --version 1.2.0  # establecer explícita
"""  # noqa: D301

import argparse
import sys

VERSION_FILE = "VERSION"


def parse_version(version_str: str) -> tuple[int, int, int]:
    parts = version_str.strip().lstrip("v").split(".")
    major = int(parts[0])
    minor = int(parts[1]) if len(parts) > 1 else 0
    patch = int(parts[2]) if len(parts) > 2 else 0
    return major, minor, patch


def read_version() -> str:
    try:
        with open(VERSION_FILE) as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.1.0"


def write_version(version_str: str) -> None:
    with open(VERSION_FILE, "w") as f:
        f.write(version_str + "\n")
    print(f"VERSION updated: {version_str}")


def bump_version(part: str) -> str:
    raw = read_version()
    major, minor, patch = parse_version(raw)
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        print(f"Unknown bump part: {part}. Expected major|minor|patch", file=sys.stderr)
        sys.exit(1)
    return f"{major}.{minor}.{patch}"


def main():
    parser = argparse.ArgumentParser(description="Manage VERSION file")
    parser.add_argument("--bump", choices=["major", "minor", "patch"], help="Bump version part")
    parser.add_argument("--version", help="Set explicit version (e.g. 1.2.0)")
    args = parser.parse_args()

    if args.version:
        new_version = args.version
    elif args.bump:
        new_version = bump_version(args.bump)
    else:
        print(read_version())
        return

    write_version(new_version)


if __name__ == "__main__":
    main()

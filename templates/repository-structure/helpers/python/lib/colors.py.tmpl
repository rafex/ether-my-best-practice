#!/usr/bin/env python3
"""
colors.py — Colores ANSI para helpers Python.

Proporciona: constantes COLOR_*, colorize(color, text),
supports_color().

Para agentes de IA: usar colores vía colorize/COLOR_* para mensajes
de UI; colors.py + messages.py = max reutilización.
"""

import sys

COLOR_RED = ""
COLOR_GREEN = ""
COLOR_YELLOW = ""
COLOR_BLUE = ""
COLOR_CYAN = ""
COLOR_MAGENTA = ""
COLOR_BOLD = ""
COLOR_RESET = ""

_COLOR_ENABLED: bool = sys.stdout.isatty() and sys.stderr.isatty()


def _init() -> None:
    global COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_BLUE
    global COLOR_CYAN, COLOR_MAGENTA, COLOR_BOLD, COLOR_RESET
    if _COLOR_ENABLED:
        COLOR_RED = "\033[0;31m"
        COLOR_GREEN = "\033[0;32m"
        COLOR_YELLOW = "\033[1;33m"
        COLOR_BLUE = "\033[0;34m"
        COLOR_CYAN = "\033[0;36m"
        COLOR_MAGENTA = "\033[0;35m"
        COLOR_BOLD = "\033[1m"
        COLOR_RESET = "\033[0m"


_init()


def supports_color() -> bool:
    """True si la terminal soporta colores ANSI."""
    return _COLOR_ENABLED


def colorize(color: str, text: str) -> str:
    """Envuelve texto en color ANSI."""
    if _COLOR_ENABLED:
        return f"{color}{text}{COLOR_RESET}"
    return text

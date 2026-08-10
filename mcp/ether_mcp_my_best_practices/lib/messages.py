#!/usr/bin/env python3
"""
messages.py — Mensajes de UI para helpers Python.

Requiere: logs.py, colors.py (deben importarse antes).
Proporciona: success, error, warning, info, step, die, header.

Para agentes de IA: usar mensajes estandarizados en vez de print()
para mantener consistencia UI y auditoría.
"""

import logging
from ether_mcp_my_best_practices.lib.colors import (
    COLOR_BLUE,
    COLOR_BOLD,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_YELLOW,
    colorize,
)
import sys


def _get_logger() -> logging.Logger:
    return logging.getLogger("messages")


def success(msg: str) -> None:
    _get_logger().info("%s %s", colorize(COLOR_GREEN, "✓"), msg)


def error(msg: str) -> None:
    _get_logger().error("%s %s", colorize(COLOR_RED, "✗"), msg)


def warning(msg: str) -> None:
    _get_logger().warning("%s %s", colorize(COLOR_YELLOW, "⚠"), msg)


def info(msg: str) -> None:
    _get_logger().info("%s %s", colorize(COLOR_CYAN, "ℹ"), msg)


def step(n: int, total: int, msg: str) -> None:
    _get_logger().info("%s [%d/%d] %s", colorize(COLOR_BLUE, "▶"), n, total, msg)


def die(msg: str, code: int = 1) -> None:
    error(msg)
    sys.exit(code)


def header(msg: str) -> None:
    line = "─" * len(msg)
    _get_logger().info("\n%s\n%s", colorize(COLOR_BOLD, msg), colorize(COLOR_BOLD, line))

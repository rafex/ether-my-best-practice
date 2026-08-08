#!/usr/bin/env python3
"""
exceptions.py — Manejo de errores para helpers Python.

Proporciona: @safe decorador + ErrorHandler context manager.
Ambos integran logging automático con exit codes.

Para agentes de IA: decorar funciones críticas con @safe
o usar 'with ErrorHandler():' para manejo controlado de excepciones.
"""

import functools
import logging
import sys
from typing import Callable


_logger = logging.getLogger("exceptions")


def safe(func: Callable) -> Callable:
    """Decorador que captura excepciones, las logea y sale con código 1."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            _logger.error("Fatal error in %s: %s", func.__name__, e)
            sys.exit(1)
    return wrapper


class ErrorHandler:
    """Context manager para manejo de errores con logging automático."""

    def __init__(self, context: str = "") -> None:
        self.context = context
        self._label = f" in {context}" if context else ""

    def __enter__(self) -> "ErrorHandler":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            _logger.error("Error%s: %s: %s", self._label, exc_type.__name__, exc_val)
            sys.exit(1)
        return False

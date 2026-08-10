#!/usr/bin/env python3
"""
logs.py — Logging con auditoría para helpers Python.

Proporciona: get_logger(name) con formato estandarizado,
RotatingFileHandler con fallback /var/log/<proyecto> → /tmp/<proyecto>.

Para agentes de IA: TODOS los helpers Python deben usar get_logger
en vez de print() para mensajes de runtime.
"""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

_PROJECT_NAME: str = os.path.basename(os.getcwd())


def _resolve_log_path(name: str) -> str:
    """Resuelve ruta del log: /var/log/<proyecto>/ → /tmp/<proyecto>/."""
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"log-{name}-{ts}.log"
    try:
        os.makedirs(f"/var/log/{_PROJECT_NAME}", exist_ok=True)
        return f"/var/log/{_PROJECT_NAME}/{filename}"
    except (PermissionError, OSError):
        os.makedirs(f"/tmp/{_PROJECT_NAME}", exist_ok=True)
        return f"/tmp/{_PROJECT_NAME}/{filename}"


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Obtiene un logger configurado con rotación y fallback."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    log_path = _resolve_log_path(name)

    handler = RotatingFileHandler(
        log_path, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    handler.setFormatter(logging.Formatter(
        "[%(levelname)s] %(asctime)s %(message)s", datefmt="%H:%M:%S"
    ))
    logger.addHandler(handler)

    # MCP stdio reserves stdout for JSON-RPC messages; diagnostics belong on stderr.
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(stream_handler)

    logger.info("Audit log: %s", log_path)
    return logger

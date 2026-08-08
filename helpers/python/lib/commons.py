#!/usr/bin/env python3
"""
commons.py — Utilidades comunes para helpers Python.

Proporciona: PROJECT_ROOT, sys.path con lib, wrapper argparse,
utilidades de rutas, ejecución de subprocesos.

Para agentes de IA: importar esta lib al inicio de cualquier helper
Python para obtener el entorno base y evitar duplicación.
"""

import argparse
import os
import subprocess
import sys

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

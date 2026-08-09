#!/usr/bin/env python3
"""
MCP Server ether-rules — expone reglas, templates y herramientas
del estándar Ether Best Practices como Resources, Tools y Prompts
para agentes de IA (Claude, opencode, Copilot).

Paquete instalable: uvx ether-mcp
Ejecutar en sitio: uv run python mcp/ether_mcp_my_best_practices/server.py
Config:   mcp-config.json → "ether-rules" server.
"""

import os
import shutil
import sys

# Reutilizar libs comunes empaquetadas (regla 15)
_lib_dir = os.path.join(os.path.dirname(__file__), "lib")
if os.path.isdir(_lib_dir):
    sys.path.insert(0, _lib_dir)
from lib.logs import get_logger
from lib.messages import success as mcp_success, error as mcp_error, info as mcp_info

from mcp.server import MCPServer
from ether_mcp_my_best_practices.config import (
    RULES_DIR,
    TEMPLATES_DIR,
    GITIGNORE_DIR,
    HELPERS_DIR,
    REPO_STRUCTURE_DIR,
    DOCS_DIR,
    list_rules_files,
    parse_frontmatter,
    list_all_templates,
    find_rule_by_id,
    templates_index,
)

log = get_logger("mcp-ether-rules")
mcp = MCPServer("ether-rules", version="1.0.0")

# ═══════════════════════════════════════════════════════════════════
# RESOURCES
# ═══════════════════════════════════════════════════════════════════

@mcp.resource("rules://index")
def resource_rules_index() -> str:
    """Índice completo de reglas con su estado y tema."""
    path = os.path.join(RULES_DIR, "00-index.md")
    if os.path.isfile(path):
        with open(path) as f:
            return f.read()
    return "Índice no encontrado."


@mcp.resource("rules://{rule_id}")
def resource_rule(rule_id: str) -> str:
    """Regla individual por ID (ej. build-tooling, 11-commitizen). Match exacto por frontmatter id, fallback a filename."""
    fname = find_rule_by_id(rule_id)
    if fname:
        with open(os.path.join(RULES_DIR, fname)) as f:
            return f.read()
    return f"No se encontró la regla '{rule_id}'."


@mcp.resource("templates://index")
def resource_templates_index() -> str:
    """Índice global de templates (repository-structure, gitignore, rule-template)."""
    return templates_index()


@mcp.resource("templates://{path:path}")
def resource_template(path: str) -> str:
    """Template por ruta relativa global (ej. repository-structure/Makefile.tmpl, gitignore/.gitignore.java.tmpl, rule-template.md.tmpl)."""
    full = os.path.join(TEMPLATES_DIR, path)
    if os.path.isfile(full):
        with open(full) as f:
            return f.read()
    return f"Template no encontrado: {path}"


@mcp.resource("gitignore://{context}")
def resource_gitignore(context: str) -> str:
    """Template de .gitignore por contexto (raiz, java, python, rust, nodejs, container, secretos, temporales, mcp)."""
    fname = f".gitignore.{context}.tmpl"
    full = os.path.join(GITIGNORE_DIR, fname)
    if os.path.isfile(full):
        with open(full) as f:
            return f.read()
    return f"Gitignore '{context}' no encontrado. Contextos: raiz, java, python, rust, nodejs, container, secretos, temporales, mcp."


@mcp.resource("helpers://{lang}/{name}")
def resource_helper(lang: str, name: str) -> str:
    """Helper específico por lenguaje y nombre (ej. shell/lint, python/changelog)."""
    for root, _dirs, files in os.walk(os.path.join(HELPERS_DIR, lang)):
        for f in files:
            if name in f or f == f"{name}.sh" or f == f"{name}.py":
                full = os.path.join(root, f)
                with open(full) as fh:
                    return fh.read()
    return f"Helper no encontrado: {lang}/{name}"


@mcp.resource("docs://{page}")
def resource_docs(page: str) -> str:
    """Página de documentación (ej. index, getting-started, contributing)."""
    fname = f"{page}.md"
    full = os.path.join(DOCS_DIR, fname)
    if os.path.isfile(full):
        with open(full) as f:
            return f.read()
    return f"Página de documentación no encontrada: {page}"


# ═══════════════════════════════════════════════════════════════════
# TOOLS
# ═══════════════════════════════════════════════════════════════════

@mcp.tool()
def list_rules() -> list[dict]:
    """Lista todas las reglas con su id, título, estado y tags (extraídos del frontmatter)."""
    result = []
    for fname in list_rules_files():
        fp = os.path.join(RULES_DIR, fname)
        fm = parse_frontmatter(fp)
        result.append({
            "file": fname,
            "id": fm.get("id", fname.replace(".md", "")),
            "title": fm.get("title", ""),
            "status": fm.get("status", "Desconocido"),
            "tags": fm.get("tags", []),
        })
    return result


@mcp.tool()
def get_rule(rule_id: str) -> str:
    """Obtiene el contenido completo de una regla por su id (ej. build-tooling, 01-build-tooling). Match exacto por frontmatter id, fallback a filename."""
    fname = find_rule_by_id(rule_id)
    if fname:
        with open(os.path.join(RULES_DIR, fname)) as f:
            return f.read()
    return f"No se encontró la regla '{rule_id}'."


@mcp.tool()
def search_rules(query: str) -> list[dict]:
    """Busca reglas cuyo contenido coincida con la query (texto simple)."""
    results = []
    for fname in list_rules_files():
        fp = os.path.join(RULES_DIR, fname)
        with open(fp) as f:
            content = f.read()
        if query.lower() in content.lower():
            fm = parse_frontmatter(fp)
            results.append({
                "file": fname,
                "id": fm.get("id", fname.replace(".md", "")),
                "title": fm.get("title", ""),
                "status": fm.get("status", ""),
                "preview": _extract_context(content, query),
            })
    return results


@mcp.tool()
def list_templates() -> list[str]:
    """Lista todos los templates disponibles (repository-structure, gitignore, rule-template). Filtra .gitkeep."""
    return list_all_templates()


@mcp.tool()
def get_template(path: str) -> str:
    """Obtiene un template por su ruta relativa global (repository-structure/..., gitignore/..., rule-template.md.tmpl)."""
    full = os.path.join(TEMPLATES_DIR, path)
    if os.path.isfile(full):
        with open(full) as f:
            return f.read()
    return f"Template no encontrado: {path}"


@mcp.tool()
def scaffold_project(slug: str, lang: str = "java", destination: str = "") -> str:
    """Genera un proyecto consumidor copiando repository-structure + gitignore según lenguaje.

    Args:
        slug: Nombre del proyecto en kebab-case (ej. patos, web).
        lang: Lenguaje principal (java, python, rust, nodejs).
        destination: Ruta destino (default: ./<slug> en workspace actual).
    """
    dest = destination or os.path.join(os.getcwd(), slug)
    if os.path.exists(dest):
        return f"El destino ya existe: {dest}. Elige otro nombre o ruta."

    log.info("Scaffolding project '%s' (lang=%s) → %s", slug, lang, dest)

    # Copiar estructura base
    shutil.copytree(REPO_STRUCTURE_DIR, dest, ignore=shutil.ignore_patterns("*.gitkeep", ".gitkeep"))

    # Copiar .gitignore raíz
    gitignore_src = os.path.join(GITIGNORE_DIR, ".gitignore.raiz.tmpl")
    if os.path.isfile(gitignore_src):
        shutil.copy(gitignore_src, os.path.join(dest, ".gitignore"))

    # Copiar .gitignore de lenguaje
    lang_gitignore = os.path.join(GITIGNORE_DIR, f".gitignore.{lang}.tmpl")
    if os.path.isfile(lang_gitignore):
        target_dir = os.path.join(dest, "source")
        if lang == "nodejs":
            target_dir = os.path.join(dest, "source", "frontend", "nodejs", slug)
        elif lang in ("java", "python", "rust"):
            target_dir = os.path.join(dest, "source", "backend", lang, slug)
        os.makedirs(target_dir, exist_ok=True)
        shutil.copy(lang_gitignore, os.path.join(target_dir, ".gitignore"))

    result = f"Proyecto '{slug}' generado en {dest}\n"
    result += f"  - Estructura base: repository-structure\n"
    result += f"  - .gitignore raíz + {lang}\n"
    result += f"  - Lenguaje principal: {lang}\n"
    result += f"  - Ejecuta 'cd {dest} && just hooks-install' para completar la instalación."
    return result


@mcp.tool()
def check_project(dir_path: str = ".") -> str:
    """Valida que un proyecto consumidor cumpla las reglas de Ether Best Practices.
    Reutiliza validate-rules.sh adaptado al proyecto en dir_path.

    Args:
        dir_path: Ruta al directorio raíz del proyecto a validar.
    """
    import subprocess

    target = os.path.abspath(dir_path)
    if not os.path.isdir(target):
        return f"Directorio no encontrado: {target}"

    # Ejecutar validate-rules.sh en el proyecto (si existe)
    validator = os.path.join(ROOT, "helpers", "shell", "validate-rules.sh")
    if not os.path.isfile(validator):
        # Si no hay validator del repo MCP, hacemos chequeos básicos
        return _basic_project_check(target)

    old_cwd = os.getcwd()
    try:
        os.chdir(target)
        result = subprocess.run(
            ["bash", validator],
            capture_output=True, text=True, timeout=30,
        )
        os.chdir(old_cwd)
        if result.returncode == 0:
            return f"Validación de reglas superada:\n{result.stdout}"
        return f"Errores de validación:\n{result.stderr or result.stdout}"
    except Exception as e:
        os.chdir(old_cwd)
        return f"Error al ejecutar validador: {e}"


@mcp.tool()
def list_helpers(lang: str = "shell") -> list[str]:
    """Lista helpers disponibles por lenguaje (shell, python)."""
    target = os.path.join(HELPERS_DIR, lang)
    if not os.path.isdir(target):
        return [f"Lenguaje no encontrado: {lang}"]
    result = []
    for root, dirs, files in os.walk(target):
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(root, f), target)
            result.append(rel)
    return result


@mcp.tool()
def get_helper(lang: str, name: str) -> str:
    """Obtiene contenido de un helper por lenguaje y nombre (ej. shell:lint, python:changelog)."""
    target = os.path.join(HELPERS_DIR, lang)
    for root, _dirs, files in os.walk(target):
        for f in files:
            if name in f or f == f"{name}.sh" or f == f"{name}.py":
                with open(os.path.join(root, f)) as fh:
                    return fh.read()
    return f"Helper no encontrado: {lang}/{name}"


# ═══════════════════════════════════════════════════════════════════
# PROMPTS
# ═══════════════════════════════════════════════════════════════════

@mcp.prompt()
def scaffold_project_prompt(slug: str, stack: str = "java+maven") -> str:
    """Guía para generar un proyecto consumidor completo.

    Args:
        slug: Nombre del proyecto en kebab-case.
        stack: Stack tecnológico (ej. java+maven, python+uv, nodejs+pnpm, rust+cargo).
    """
    return f"""Eres un agente de codificación que sigue Ether Best Practices (rules/*.md).

Vas a generar el proyecto '{slug}' con stack '{stack}'.

1. Copia la estructura base de templates/repository-structure/ a la raíz de {slug}.
2. Usa templates/gitignore/.gitignore.raiz.tmpl + el .gitignore del lenguaje correspondiente.
3. Para backend: estructura hexagonal (domain, application, infrastructure, ports) en source/backend/<lang>/<slug>/src/.
4. Para frontend: source/frontend/nodejs/<slug>/src/ con package.json.
5. Ejecuta 'just hooks-install' para activar hooks + Commitizen.
6. Configura .config/commitizen/pyproject.toml con version_files según el lenguaje.

Reglas clave a seguir:
- Regla 01 (Build Tooling): Makefile → helpers/mk/*.mk → helpers/shell/*.sh
- Regla 02 (Arquitectura): Hexagonal, domain/application/infrastructure/ports
- Regla 03 (Testing): TDD, pirámide de tests
- Regla 05 (Version Control): Conventional Commits
- Regla 08 (Stack): Java Temurin 25 LTS / Node LTS / Python 3.12+ / Podman
- Regla 09 (Repository Structure): source/<rol>/<lenguaje>/<proyecto>/
- Regla 12 (Gitignore): .gitignore por contexto
- Regla 15 (Script Reuse): helpers/lib/ logger + mensajes

Genera el cascarón paso a paso, explicando cada decisión de estructura."""


@mcp.prompt()
def implement_feature(rule_id: str, context: str = "") -> str:
    """Guía para implementar una funcionalidad siguiendo una regla específica.

    Args:
        rule_id: ID de la regla a aplicar (ej. 01-build-tooling, 11-commitizen).
        context: Descripción de lo que hay que implementar.
    """
    return f"""Eres un agente que sigue Ether Best Practices. Aplica la regla '{rule_id}'.
Contexto: {context or 'No especificado'}

1. Lee la regla '{rule_id}' completa (usa la tool get_rule).
2. Identifica las Restricciones (lo que NO se debe hacer) y los Ejemplos.
3. Implementa siguiendo exactamente los Comandos y Ejemplos de la regla.
4. Sigue Conventional Commits y arquitectura hexagonal si aplica.
5. Escribe tests antes del código (TDD)."""


@mcp.prompt()
def review_project(dir_path: str = ".") -> str:
    """Guía para revisar un proyecto contra el estándar.

    Args:
        dir_path: Ruta al proyecto a revisar.
    """
    return f"""Revisa el proyecto en '{dir_path}' contra Ether Best Practices.

1. Ejecuta la tool check_project para validar estructura de reglas.
2. Verifica: estructura hexagonal (regla 02), gitignore (regla 12), .config/ (regla 14).
3. Verifica: tests (regla 03), Conventional Commits (regla 05), CI (regla 06).
4. Reporta hallazgos agrupados por regla."""


@mcp.prompt()
def configure_tool(herramienta: str) -> str:
    """Guía para configurar una herramienta en .config/<herramienta>/ (regla 14).

    Args:
        herramienta: Nombre de la herramienta (commitizen, mkdocs, sops).
    """
    return f"""Configura '{herramienta}' según la regla 14 (Archivos de Configuración) de Ether Best Practices.

1. Crea .config/{herramienta}/ si no existe.
2. Si es commitizen: copia templates/repository-structure/.config/commitizen/pyproject.toml.tmpl.
3. Si es mkdocs: copia templates/repository-structure/.config/mkdocs/mkdocs.yml.tmpl + requirements.txt.tmpl.
4. Si es sops: copia templates/repository-structure/.config/sops/.sops.yaml.tmpl.
5. Asegura que todos los flags de las herramientas apunten a .config/<herramienta>/archivo (usa get_rule 14-config-files para los detalles)."""


@mcp.prompt()
def commit_workflow() -> str:
    """Guía para commits convencionales y release con Commitizen (regla 11)."""
    return """Flujo de commit y release según Ether Best Practices:

1. `just commit` → asistente interactivo de Commitizen (type + scope + descripción).
2. `just prepare-release` → bump version + CHANGELOG.md + tag + commit.
3. `just changelog` → genera desde Conventional Commits.
4. `just version` → lee/bumpea versión actual.

Tipos válidos: feat, fix, docs, style, refactor, test, chore, build, ci, perf, revert.
Formato: tipo[(scope)][!]: descripción
Commit de release automático: "chore(release): vX.Y.Z" """


# ═══════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _extract_context(content: str, query: str, window: int = 80) -> str:
    """Extrae snippet de contexto alrededor de la query."""
    lower = content.lower()
    idx = lower.find(query.lower())
    if idx < 0:
        return content[:200] + "..."
    start = max(0, idx - window)
    end = min(len(content), idx + len(query) + window)
    return content[start:end] + ("..." if end < len(content) else "")


def _basic_project_check(target: str) -> str:
    """Chequeo básico de estructura si no existe validate-rules.sh."""
    checks = []
    for item in [".gitignore", "Makefile", "Justfile", "helpers/", "source/"]:
        checks.append(f"  {'✓' if os.path.exists(os.path.join(target, item)) else '✗'} {item}")
    return "Chequeo básico de estructura:\n" + "\n".join(checks)


def main():
    """Entry point for the installed package (ether-mcp command)."""
    mcp_info("MCP server ether-rules v1.0.0 iniciado")
    mcp.run()


if __name__ == "__main__":
    main()

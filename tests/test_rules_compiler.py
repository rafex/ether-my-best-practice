#!/usr/bin/env python3
"""Pruebas unitarias del compilador determinista de reglas."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "helpers" / "python"))

import rules_compiler as compiler  # noqa: E402


def make_ast(
    *,
    status: str = "Borrador",
    filename: str = "01-example_draft.md",
) -> compiler.RuleAST:
    ast = compiler.RuleAST()
    ast.filepath = filename
    ast.id = "example"
    ast.title = "Example"
    ast.status = status
    ast.tags = ["example"]
    ast.heading = "# Regla 01: Example — ⚠️ *Borrador*" if status == "Borrador" else "# Regla 01: Example"
    ast.blocks = [
        {"type": "Premisa", "name": "Motivo", "content": "> Motivo.", "tags": ["obligatorio"]},
        {"type": "Restriccion", "name": "Prohibición", "content": "> No hacer esto.", "tags": ["obligatorio"]},
        {"type": "Ejemplo", "name": "Correcto", "content": "```shell\ntrue\n```", "tags": ["obligatorio"]},
        {"type": "Referencia", "name": "Documentación", "content": "- Referencia", "tags": ["obligatorio"]},
    ]
    if status == "Definida":
        ast.blocks.extend([
            {"type": "Comando", "name": "Validar", "content": "```shell\nmake validate\n```", "tags": []},
            {"type": "Estructura", "name": "Proyecto", "content": "```text\nrules/\n```", "tags": []},
        ])
    return ast


class FrontmatterAndBlocksTests(unittest.TestCase):
    def test_parse_frontmatter_and_heading(self):
        text = "---\nid: 01-example\ntitle: Ejemplo\nstatus: Borrador\ntags: [build]\n---\n\n# Regla 01: Ejemplo\n"

        frontmatter, heading = compiler.parse_frontmatter_and_heading(text)

        self.assertEqual(frontmatter["id"], "01-example")
        self.assertEqual(frontmatter["tags"], ["build"])
        self.assertEqual(heading, "# Regla 01: Ejemplo")

    def test_frontmatter_with_embedded_separator_in_value_is_supported(self):
        text = "---\nid: 01-example\ntitle: 'A --- B'\nstatus: Borrador\ntags: []\n---\n# Regla 01: Ejemplo\n"

        frontmatter, heading = compiler.parse_frontmatter_and_heading(text)

        self.assertEqual(frontmatter["title"], "A --- B")
        self.assertEqual(heading, "# Regla 01: Ejemplo")

    def test_invalid_frontmatter_raises_compiler_error(self):
        with self.assertRaises(compiler.RuleCompilerError):
            compiler.parse_frontmatter_and_heading("---\nid: [incompleto\n---\n# Regla\n")

    def test_unclosed_frontmatter_raises_compiler_error(self):
        with self.assertRaisesRegex(compiler.RuleCompilerError, "delimitador"):
            compiler.parse_frontmatter_and_heading("---\nid: example\n# Regla\n")

    def test_non_mapping_frontmatter_raises_compiler_error(self):
        with self.assertRaisesRegex(compiler.RuleCompilerError, "mapa"):
            compiler.parse_frontmatter_and_heading("---\n- item\n---\n# Regla\n")

    def test_parse_blocks_preserves_fenced_headings_and_unknown_subsections(self):
        text = """
### Premisa: Motivo
> La premisa.

### Ejemplo: Código
```shell
### Premisa: No es un bloque
echo ok
```

### TDD: Subsección documental
Texto de la subsección.

tags: [obligatorio, testing]

### Referencia: Fuente
- Documento
tags: []
"""

        blocks = compiler.parse_blocks(text)

        self.assertEqual([block["type"] for block in blocks], ["Premisa", "Ejemplo", "Referencia"])
        self.assertIn("### Premisa: No es un bloque", blocks[1]["content"])
        self.assertIn("### TDD: Subsección documental", blocks[1]["content"])
        self.assertEqual(blocks[1]["tags"], ["obligatorio", "testing"])
        self.assertEqual(blocks[2]["tags"], [])

    def test_parse_block_with_empty_name_is_reported_by_validation(self):
        ast = make_ast()
        ast.blocks[0] = {"type": "Premisa", "name": "", "content": "Texto", "tags": []}

        diagnostics = compiler.validate_ast(ast)

        self.assertTrue(any("sin nombre" in diagnostic for diagnostic in diagnostics))

    def test_parse_rule_reads_utf8_and_returns_ast(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "01-ejemplo_draft.md"
            path.write_text(
                "---\nid: 01-ejemplo\ntitle: Ñandú\nstatus: Borrador\ntags: [área]\n---\n\n"
                "# Regla 01: Ñandú — ⚠️ *Borrador*\n\n"
                "### Premisa: Motivo\n\n> Texto\n\ntags: [obligatorio]\n\n"
                "### Restriccion: Prohibición\n\n> Texto\n\ntags: [obligatorio]\n\n"
                "### Ejemplo: Correcto\n\n```shell\necho sí\n```\n\ntags: [obligatorio]\n\n"
                "### Referencia: Fuente\n\n- Documento\n\ntags: [obligatorio]\n",
                encoding="utf-8",
            )

            ast = compiler.parse_rule(str(path))

        self.assertIsNotNone(ast)
        self.assertEqual(ast.title, "Ñandú")
        self.assertEqual(ast.tags, ["área"])
        self.assertEqual(len(ast.blocks), 4)

    def test_parse_rule_returns_none_for_missing_file(self):
        self.assertIsNone(compiler.parse_rule("/tmp/no-such-rule.md"))


class ValidationAndRenderTests(unittest.TestCase):
    def test_valid_draft_has_no_diagnostics(self):
        self.assertEqual(compiler.validate_ast(make_ast()), [])

    def test_valid_defined_rule_requires_and_accepts_maturity_blocks(self):
        self.assertEqual(compiler.validate_ast(make_ast(status="Definida", filename="01-example.md")), [])

    def test_defined_rule_requires_command_and_structure_or_diagram(self):
        ast = make_ast(status="Definida", filename="01-example.md")
        ast.blocks = ast.blocks[:4]

        diagnostics = compiler.validate_ast(ast)

        self.assertTrue(any("Comando" in diagnostic for diagnostic in diagnostics))
        self.assertTrue(any("Estructura" in diagnostic or "Diagrama" in diagnostic for diagnostic in diagnostics))

    def test_validation_reports_required_frontmatter_and_heading(self):
        ast = make_ast()
        ast.id = ""
        ast.title = ""
        ast.tags = "example"
        ast.heading = ""

        diagnostics = compiler.validate_ast(ast)

        self.assertTrue(any("falta id" in diagnostic for diagnostic in diagnostics))
        self.assertTrue(any("falta title" in diagnostic for diagnostic in diagnostics))
        self.assertTrue(any("tags debe ser una lista" in diagnostic for diagnostic in diagnostics))
        self.assertTrue(any("falta título H1" in diagnostic for diagnostic in diagnostics))

    def test_validation_rejects_non_text_tags(self):
        ast = make_ast()
        ast.tags = ["testing", 42]

        diagnostics = compiler.validate_ast(ast)

        self.assertTrue(any("todos los tags deben ser texto" in diagnostic for diagnostic in diagnostics))

    def test_draft_convention_is_a_warning(self):
        ast = make_ast(filename="01-example.md")
        diagnostics = compiler.validate_ast(ast)

        self.assertTrue(diagnostics)
        self.assertTrue(all(diagnostic.startswith("WARNING ") for diagnostic in diagnostics))

    def test_render_round_trip_is_semantically_stable(self):
        ast = make_ast(status="Definida", filename="01-example.md")

        rendered = compiler.render_rule(ast)
        reparsed = compiler.RuleAST()
        reparsed.filepath = ast.filepath
        frontmatter, heading = compiler.parse_frontmatter_and_heading(rendered)
        reparsed.id = frontmatter["id"]
        reparsed.title = frontmatter["title"]
        reparsed.status = frontmatter["status"]
        reparsed.tags = frontmatter["tags"]
        reparsed.heading = heading
        reparsed.blocks = compiler.parse_blocks(rendered)

        self.assertEqual(compiler.render_rule(reparsed), rendered)
        self.assertEqual(reparsed.id, ast.id)
        self.assertEqual(reparsed.title, ast.title)
        self.assertEqual(reparsed.status, ast.status)
        self.assertEqual(reparsed.tags, ast.tags)
        self.assertEqual(reparsed.blocks, ast.blocks)

    def test_all_repository_rules_remain_valid(self):
        failures = []
        for path in sorted((ROOT / "rules").glob("[0-9][0-9]-*.md")):
            if path.name == "00-index.md":
                continue
            ast = compiler.parse_rule(str(path))
            diagnostics = compiler.validate_ast(ast)
            fatal = [diagnostic for diagnostic in diagnostics if not diagnostic.startswith("WARNING ")]
            if fatal:
                failures.append(f"{path.name}: {fatal}")

        self.assertEqual(failures, [])

    def test_create_new_rule_uses_template_and_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rules_dir = root / "rules"
            template = root / "rule-template.md.tmpl"
            template.write_text(
                "---\nid: nn-topic\ntitle: Título descriptivo\nstatus: Borrador\ntags: []\n---\n\n"
                "# Regla NN: Título\n",
                encoding="utf-8",
            )

            with patch.object(compiler, "RULES_DIR", str(rules_dir)), patch.object(compiler, "TEMPLATE_PATH", str(template)):
                result = compiler.create_new_rule("19-new-rule", "Nueva regla")
                created = rules_dir / "19-new-rule.md"
                second_result = compiler.create_new_rule("19-new-rule", "Otro título")

            self.assertIn("19-new-rule.md", result)
            self.assertIn("ya existe", second_result)
            self.assertEqual(
                created.read_text(encoding="utf-8"),
                "---\nid: 19-new-rule\ntitle: Nueva regla\nstatus: Borrador\ntags: []\n---\n\n"
                "# Regla 19: Título\n",
            )

    def test_create_new_rule_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(compiler, "RULES_DIR", str(Path(directory) / "rules")):
                with self.assertRaisesRegex(compiler.RuleCompilerError, "slug inseguro"):
                    compiler.create_new_rule("../outside", "Fuera")

            self.assertFalse((Path(directory) / "outside.md").exists())


if __name__ == "__main__":
    unittest.main()

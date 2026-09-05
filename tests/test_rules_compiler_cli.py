#!/usr/bin/env python3
"""Pruebas de contrato CLI para rules_compiler.py."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPILER = ROOT / "helpers" / "python" / "rules_compiler.py"


def rule_document(*, status="Borrador", heading="Regla 01: Ejemplo — ⚠️ *Borrador*", extra=""):
    return (
        "---\n"
        "id: 01-example\n"
        "title: Ejemplo\n"
        f"status: {status}\n"
        "tags: [testing]\n"
        "---\n\n"
        f"# {heading}\n\n"
        "### Premisa: Motivo\n\n> Motivo.\n\ntags: [obligatorio]\n\n"
        "### Restriccion: Prohibición\n\n> No hacer esto.\n\ntags: [obligatorio]\n\n"
        "### Ejemplo: Correcto\n\n```shell\necho ok\n```\n\ntags: [obligatorio]\n\n"
        "### Referencia: Fuente\n\n- Documento\n\ntags: [obligatorio]\n\n"
        f"{extra}"
    )


class CompilerCliTests(unittest.TestCase):
    def run_compiler(self, *arguments, rules_dir, templates_dir=None):
        environment = os.environ.copy()
        environment["RULES_DIR"] = str(rules_dir)
        environment["TEMPLATES_DIR"] = str(templates_dir or ROOT / "templates")
        return subprocess.run(
            [sys.executable, str(COMPILER), *arguments],
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_parse_emits_json_on_stdout_and_logs_on_stderr(self):
        with tempfile.TemporaryDirectory() as directory:
            rules_dir = Path(directory) / "rules"
            rules_dir.mkdir()
            (rules_dir / "01-example_draft.md").write_text(rule_document(), encoding="utf-8")

            result = self.run_compiler("--action", "parse", "01-example_draft", rules_dir=rules_dir)

        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed["id"], "01-example")
        self.assertEqual(parsed["blocks"][0]["type"], "Premisa")
        self.assertNotIn("Audit log:", result.stdout)

    def test_validate_returns_zero_for_valid_draft_and_warnings_are_nonfatal(self):
        with tempfile.TemporaryDirectory() as directory:
            rules_dir = Path(directory) / "rules"
            rules_dir.mkdir()
            (rules_dir / "01-example.md").write_text(
                rule_document(heading="Regla 01: Ejemplo"), encoding="utf-8"
            )

            result = self.run_compiler("--action", "validate", "01-example", rules_dir=rules_dir)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("WARNING", result.stderr)
        self.assertNotIn("✗", result.stderr)

    def test_validate_returns_nonzero_for_malformed_yaml_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            rules_dir = Path(directory) / "rules"
            rules_dir.mkdir()
            (rules_dir / "01-example.md").write_text(
                "---\nid: [incompleto\n---\n# Regla 01: Ejemplo\n", encoding="utf-8"
            )

            result = self.run_compiler("--action", "validate", "01-example", rules_dir=rules_dir)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("YAML inválido", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_validate_all_processes_rule_files(self):
        with tempfile.TemporaryDirectory() as directory:
            rules_dir = Path(directory) / "rules"
            rules_dir.mkdir()
            (rules_dir / "00-index.md").write_text("# Índice\n", encoding="utf-8")
            (rules_dir / "01-example_draft.md").write_text(rule_document(), encoding="utf-8")

            result = self.run_compiler("--action", "validate", "--all", rules_dir=rules_dir)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("✗", result.stderr)

    def test_render_in_place_is_the_only_render_mode_that_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            rules_dir = Path(directory) / "rules"
            rules_dir.mkdir()
            path = rules_dir / "01-example_draft.md"
            original = rule_document()
            path.write_text(original, encoding="utf-8")

            stdout_result = self.run_compiler("--action", "render", "01-example_draft", rules_dir=rules_dir)
            self.assertEqual(stdout_result.returncode, 0, stdout_result.stderr)
            self.assertEqual(path.read_text(encoding="utf-8"), original)
            self.assertTrue(stdout_result.stdout.startswith("---\n"))

            inplace_result = self.run_compiler(
                "--action", "render", "01-example_draft", "--in-place", rules_dir=rules_dir
            )
            rendered_content = path.read_text(encoding="utf-8")

        self.assertEqual(inplace_result.returncode, 0, inplace_result.stderr)
        self.assertNotEqual(rendered_content, original)

    def test_new_uses_configured_template(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rules_dir = root / "rules"
            templates_dir = root / "templates"
            templates_dir.mkdir()
            (templates_dir / "rule-template.md.tmpl").write_text(
                "---\nid: nn-topic\ntitle: Título descriptivo\nstatus: Borrador\ntags: []\n---\n\n"
                "# Regla NN: Título\n",
                encoding="utf-8",
            )

            result = self.run_compiler(
                "--action", "new", "--slug", "19-new-rule", "--title", "Nueva regla",
                rules_dir=rules_dir, templates_dir=templates_dir,
            )

            created = rules_dir / "19-new-rule.md"
            created_content = created.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("id: 19-new-rule", created_content)
        self.assertIn("Regla 19", created_content)

    def test_new_rejects_unsafe_slug_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            rules_dir = Path(directory) / "rules"

            result = self.run_compiler(
                "--action", "new", "--slug", "../outside", "--title", "Fuera",
                rules_dir=rules_dir,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("slug inseguro", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()

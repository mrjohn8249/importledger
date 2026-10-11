import tempfile
import unittest
from pathlib import Path

from importledger.cli import check


class CheckTests(unittest.TestCase):
    def test_reports_only_missing_third_party_imports(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "pyproject.toml").write_text(
                '[project]\ndependencies = ["requests>=2", "Pillow>=10"]\n'
                '[tool.importledger.module-map]\nPIL = "Pillow"\n', encoding="utf-8"
            )
            (root / "app.py").write_text(
                "import json\nimport requests\nfrom PIL import Image\nimport missing_pkg\n",
                encoding="utf-8",
            )
            self.assertEqual(list(check(root)), ["missing_pkg"])

    def test_optional_and_relative_imports(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "pyproject.toml").write_text(
                '[project]\ndependencies = []\n[project.optional-dependencies]\n'
                'dev = ["pytest>=8"]\n', encoding="utf-8"
            )
            package = root / "src" / "example"
            package.mkdir(parents=True)
            (package / "__init__.py").write_text("from .core import run\n", encoding="utf-8")
            (package / "core.py").write_text("import pytest\nimport example\n", encoding="utf-8")
            self.assertEqual(list(check(root)), ["pytest"])
            self.assertEqual(check(root, include_optional=True), {})


if __name__ == "__main__":
    unittest.main()

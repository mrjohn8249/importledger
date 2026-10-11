# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — 2026-10-11

### Added

- Static analysis of Python source files using `ast` — no import side-effects.
- PEP 621 (`[project].dependencies`) dependency parsing.
- Poetry (`[tool.poetry.dependencies]`) dependency parsing.
- Optional dependency support (`--include-optional` flag).
- Configurable import-to-package name mapping via `[tool.importledger.module-map]` in the project's `pyproject.toml` (e.g. `PIL = "Pillow"`).
- JSON output mode (`--json`) for machine-readable results.
- Meaningful exit codes: `0` = clean, `1` = undeclared imports found, `2` = error.
- Detection of local modules (packages under `src/`, `lib/`, and top-level) so they are not reported as missing.
- Skips generated and environment directories (`.git`, `.venv`, `venv`, `__pycache__`, `build`, `dist`, `.tox`).
- Unit tests using Python's standard `unittest` module.
- GitHub Actions CI workflow covering Python 3.11, 3.12, and 3.13.
- MIT license.

[Unreleased]: https://github.com/mrjohn8249/importledger/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/mrjohn8249/importledger/releases/tag/v0.1.0

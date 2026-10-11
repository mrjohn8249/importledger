# Contributing to importledger

Thank you for taking the time to contribute. This document explains how to get started.

## Code of conduct

Be respectful and constructive. Harassment of any kind is not tolerated.

## Reporting bugs

Open a [GitHub Issue](https://github.com/mrjohn8249/importledger/issues) using the **Bug report** template. Include:

- Your Python version and OS.
- A minimal `pyproject.toml` and Python file that demonstrates the problem.
- The exact output you received and what you expected.

## Suggesting features

Open an issue using the **Feature request** template. Describe the problem you are trying to solve rather than a specific solution, so the design can be discussed before code is written.

## Making changes

1. Fork the repository and create a branch from `main`.
2. Install the package in editable mode:

   ```console
   python -m pip install -e .
   ```

3. Make your change with a focused scope — one logical change per pull request.
4. Add or update tests in `tests/` for any new behaviour. The test suite uses only Python's standard `unittest` module; no additional test framework is needed.
5. Run the tests locally:

   ```console
   PYTHONPATH=src python -m unittest discover -s tests -v
   ```

   All tests must pass on Python 3.11, 3.12, and 3.13.

6. Run the tool against its own repository to confirm it does not report a false positive:

   ```console
   PYTHONPATH=src python -m importledger .
   ```

7. Open a pull request against `main`. Describe what the change does and why.

## Import-to-package mapping

A common request is to add a new built-in mapping (for example, `cv2 → opencv-python`). These mappings belong in the project being checked via `[tool.importledger.module-map]`, not in the tool itself, so that each project can declare exactly the mappings it needs. Please read the README for details before opening an issue about missing mappings.

## Style

- Format code with standard Python style (PEP 8).
- Keep the runtime dependency count at zero — the tool must work with only the standard library.
- Prefer clarity over cleverness. The implementation is meant to be easy to audit.

## License

By contributing you agree that your contributions will be licensed under the [MIT License](LICENSE).

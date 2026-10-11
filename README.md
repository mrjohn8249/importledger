# importledger

`importledger` checks a Python project's imports against its declared `pyproject.toml` dependencies. It helps catch the common mistake where code works on a developer's machine but fails in a clean environment because a package was never declared.

## Requirements

Python 3.11 or newer. The tool has no runtime dependencies.

## Install and run

```console
python -m pip install .
importledger path/to/project
```

Run without installation from this checkout:

```console
PYTHONPATH=src python -m importledger path/to/project
```

Exit code 0 means no missing imports were found; 1 means possible missing dependencies; 2 means the project could not be checked. Use `--json` for scripts and `--include-optional` to count optional dependencies.

Some distribution names differ from their import names. Add explicit mappings to the project being checked:

```toml
[tool.importledger.module-map]
PIL = "Pillow"
yaml = "PyYAML"
cv2 = "opencv-python"
```

## Scope

This is a static check. It reads `import` statements from Python files and supports PEP 621 and Poetry dependency declarations. It cannot see dynamic imports, infer every import-to-distribution mapping, or tell whether an import is used only in a test. Review the reported locations before changing dependencies. It skips common generated and environment directories.

## Contributing

Issues and focused pull requests are welcome. Please include a small example project or test case for new detection behavior. Run the tests with:

```console
PYTHONPATH=src python -m unittest discover -s tests -v
```

## License

MIT. See [LICENSE](LICENSE).

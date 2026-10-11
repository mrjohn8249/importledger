"""Command line entry point for importledger."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import tomllib
from pathlib import Path

REQUIREMENT_NAME = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)")
IGNORED_DIRS = {".git", ".venv", "venv", "__pycache__", "build", "dist", ".tox"}


def normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def declared_dependencies(config: dict, include_optional: bool) -> set[str]:
    project = config.get("project", {})
    requirements = list(project.get("dependencies", []))
    if include_optional:
        for group in project.get("optional-dependencies", {}).values():
            requirements.extend(group)
    poetry = config.get("tool", {}).get("poetry", {}).get("dependencies", {})
    requirements.extend(name for name in poetry if name.lower() != "python")
    names = set()
    for requirement in requirements:
        match = REQUIREMENT_NAME.match(requirement)
        if match:
            names.add(normalize(match.group(1)))
    return names


def source_files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*.py")
        if not any(part in IGNORED_DIRS or part.startswith(".") for part in path.relative_to(root).parts)
    )


def local_modules(root: Path, files: list[Path]) -> set[str]:
    modules = set()
    for file in files:
        relative = file.relative_to(root)
        parts = relative.parts
        if len(parts) == 1:
            modules.add(file.stem)
        elif parts[0] in {"src", "lib"} and len(parts) > 1:
            modules.add(parts[1].removesuffix(".py"))
        else:
            modules.add(parts[0])
    modules.discard("__init__")
    return modules


def imported_modules(files: list[Path]) -> dict[str, list[str]]:
    imports: dict[str, list[str]] = {}
    for file in files:
        try:
            tree = ast.parse(file.read_text(encoding="utf-8-sig"), filename=str(file))
        except (SyntaxError, UnicodeError) as error:
            raise ValueError(f"Cannot parse {file}: {error}") from error
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names = [node.module.split(".")[0]]
            else:
                continue
            for name in names:
                imports.setdefault(name, [])
                location = f"{file}:{node.lineno}"
                if location not in imports[name]:
                    imports[name].append(location)
    return imports


def check(root: Path, include_optional: bool = False) -> dict[str, list[str]]:
    config_path = root / "pyproject.toml"
    if not config_path.is_file():
        raise ValueError(f"No pyproject.toml found in {root}")
    try:
        config = tomllib.loads(config_path.read_text(encoding="utf-8-sig"))
    except (tomllib.TOMLDecodeError, UnicodeError) as error:
        raise ValueError(f"Cannot read {config_path}: {error}") from error
    declared = declared_dependencies(config, include_optional)
    mapping = config.get("tool", {}).get("importledger", {}).get("module-map", {})
    if not isinstance(mapping, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in mapping.items()):
        raise ValueError("[tool.importledger.module-map] must map import names to package names")
    files = source_files(root)
    local = local_modules(root, files)
    imports = imported_modules(files)
    return {
        name: locations
        for name, locations in sorted(imports.items())
        if name not in sys.stdlib_module_names
        and name not in sys.builtin_module_names
        and name not in local
        and normalize(mapping.get(name, name)) not in declared
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", help="project directory (default: current directory)")
    parser.add_argument("--include-optional", action="store_true", help="count optional dependencies as declared")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args(argv)
    try:
        missing = check(Path(args.path).resolve(), args.include_optional)
    except (ValueError, OSError) as error:
        parser.exit(2, f"importledger: {error}\n")
    if args.json:
        print(json.dumps({"missing": missing}, indent=2))
    elif missing:
        for name, locations in missing.items():
            print(f"{name}: not declared (found at {', '.join(locations)})")
    else:
        print("No undeclared third-party imports found.")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())

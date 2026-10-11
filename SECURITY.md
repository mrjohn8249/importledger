# Security Policy

## Supported versions

Only the latest release is actively maintained.

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅ Yes    |

## Scope

`importledger` is a static analysis tool that reads Python source files and `pyproject.toml` configuration files. It does not execute user code, make network requests, or write to disk beyond its own output.

The main security-relevant code path is the parsing of Python source files via `ast.parse`. Malformed files are rejected with an error message; they are never executed.

## Reporting a vulnerability

If you believe you have found a security vulnerability, **do not open a public issue**. Instead, please report it privately:

- **Email:** open a [GitHub private security advisory](https://github.com/mrjohn8249/importledger/security/advisories/new) (preferred), or contact the maintainer through the GitHub profile.
- Include a description of the vulnerability, steps to reproduce it, and the potential impact.

You can expect an acknowledgement within 7 days and a resolution or status update within 30 days.

## Public disclosure

Once a fix is ready, the vulnerability will be disclosed publicly in a GitHub Security Advisory and in the [CHANGELOG](CHANGELOG.md).

#!/usr/bin/env python3
"""Lint every YAML snippet in docs/ (P1-02): confirm each ```yaml fenced
block actually parses as valid YAML.

Unlike PHP snippets (which distinguish a complete, file-level example from a
bare method excerpt), a YAML fragment is valid YAML on its own even when
it's just one config key — so every ```yaml block is checked, not a subset.
This proves **syntactic validity**, not that the keys/values shown are
correct Symfony 8.0 configuration options — that would require a schema
validator against Symfony's actual Config tree, which is not built here (see
specs/RemediationLog.md P1-02 for the honest scope of what this does and
does not check).

Exit non-zero on any real parse failure. Run: python tools/lint_yaml.py
"""
from __future__ import annotations
import glob, re, os, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK = re.compile(r"```yaml\n(.*?)```", re.DOTALL)

# Symfony's own YAML component recognizes custom tags (!service_locator,
# !tagged_iterator, !tagged, !service, !iterator, ...) that plain PyYAML does
# not know about out of the box - that is real, valid Symfony DI config
# syntax, not a YAML error. Register them as passthrough constructors so
# this linter checks generic YAML syntax validity without false-flagging
# legitimate Symfony-specific tags as failures.
class _SymfonyYamlLoader(yaml.SafeLoader):
    pass


def _passthrough(loader, tag_suffix, node):
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    return None


_SymfonyYamlLoader.add_multi_constructor("!", _passthrough)


def main() -> int:
    linted = 0
    fails = []
    for f in glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True):
        if "/_meta/" in f:
            continue
        text = open(f, encoding="utf-8").read()
        for m in BLOCK.finditer(text):
            code = m.group(1)
            if not code.strip():
                continue
            linted += 1
            try:
                yaml.load(code, Loader=_SymfonyYamlLoader)
            except yaml.YAMLError as e:
                msg = str(e).splitlines()[0]
                fails.append((os.path.relpath(f, ROOT), msg))
    print(f"linted {linted} YAML snippets (syntax only); {len(fails)} failure(s)")
    for rel, msg in fails:
        print(f"  FAIL {rel}: {msg}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Documentation-only CI checks. No app, secrets or network required."""
from __future__ import annotations
import re
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
errors: list[str] = []

def check_links(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"```[\s\S]*?```", "", raw)
    raw = re.sub(r"`[^`\n]*`", "", raw)
    for match in re.finditer(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", raw):
        target = match.group(1).strip().split("#", 1)[0].split("?", 1)[0]
        if not target or target.startswith(("https://", "http://", "mailto:", "#")):
            continue
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        resolved = (path.parent / target).resolve()
        if not resolved.is_relative_to(ROOT):
            errors.append(f"{path.relative_to(ROOT)}: link escapes repo: {target}")
        elif not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken link: {target}")

def check_openapi() -> None:
    path = DOCS / "08-operations" / "OpenAPI.yaml"
    api = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(api, dict) or api.get("openapi") != "3.1.0":
        errors.append("OpenAPI.yaml is not an OpenAPI 3.1 document")
        return
    paths = api.get("paths", {})
    schemas = api.get("components", {})
    if not isinstance(paths, dict) or not isinstance(schemas, dict):
        errors.append("OpenAPI.yaml lacks paths or components")
        return
    refs: set[str] = set()
    def walk(node: object) -> None:
        if isinstance(node, dict):
            if "$ref" in node:
                refs.add(node["$ref"])
            for val in node.values():
                walk(val)
        elif isinstance(node, list):
            for val in node:
                walk(val)
    walk(api)
    for ref in sorted(refs):
        if not isinstance(ref, str) or not ref.startswith("#/"):
            errors.append(f"Unsupported or invalid OpenAPI reference: {ref}")
            continue
        item: object = api
        for part in ref[2:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            if not isinstance(item, dict) or part not in item:
                errors.append(f"Unresolved OpenAPI reference: {ref}")
                break
            item = item[part]
    seen: set[str] = set()
    for route, methods in paths.items():
        if not isinstance(methods, dict):
            errors.append(f"Invalid OpenAPI path item: {route}")
            continue
        for verb, op in methods.items():
            if verb not in {"get", "post", "put", "patch", "delete", "options", "head", "trace"}:
                continue
            opid = op.get("operationId")
            if not opid or opid in seen:
                errors.append(f"Missing/duplicate operationId: {verb} {route}")
            seen.add(opid)

def main() -> int:
    for path in [ROOT / "README.md", ROOT / "AGENTS.md", *DOCS.rglob("*.md")]:
        check_links(path)
    check_openapi()
    if errors:
        print("\n".join("ERROR: " + error for error in errors))
        return 1
    print("Documentation relative links and OpenAPI references: OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())

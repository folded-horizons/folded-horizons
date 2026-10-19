#!/usr/bin/env python3
"""Validate the FTB Quests SNBT files in overrides/.

Checks:
  1. every .snbt file parses (SNBT subset: comments // and #, quoted
     strings with escapes, unquoted keys, nested compounds/lists)
  2. every quest has an id, a title, and a tasks object
  3. quest ids are unique across chapters
  4. every dependency points at an existing quest id
  5. every item id referenced by a task/icon uses a namespace that is
     actually in the pack (catches `gregtech:` vs `gtceu:` mistakes)

Run from the repo root:  python3 scripts/validate_quests.py
Exit code 0 = clean, 1 = problems found.
"""

from __future__ import annotations

import json
import pathlib
import sys

QUESTS_DIR = pathlib.Path("overrides/ftbquests/quests")
LOCKFILE = pathlib.Path("pakku-lock.json")

# Project slug -> in-game mod namespace. The lockfile records slugs and
# file names, never the namespace, so this map is maintained by hand. Add
# an entry whenever the pack gains a mod that quests reference.
#
# Keys may be a CurseForge slug, a Modrinth slug, or (for GitHub-hosted
# projects such as GTCEu) the "owner/repo" string written there as
# "owner\nrepo" in the lockfile's slug map — see slug_keys().
SLUG_NAMESPACES: dict[str, str] = {
    "applied-energistics-2": "ae2",
    "applied-flux": "appflux",
    "architectury-api": "architectury",
    "bonsai-trees": "bonsaitrees4",
    "emi": "emi",
    "expanded-delight": "expandeddelight",
    "farmers-delight": "farmersdelight",
    "ftb-chunks-forge": "ftbchunks",
    "ftb-essentials": "ftbessentials",
    "ftb-library-forge": "ftblibrary",
    "ftb-quests-forge": "ftbquests",
    "ftb-teams-forge": "ftbteams",
    "functional-storage": "functionalstorage",
    # GTCEu is tracked from its GitHub release because the CurseForge build
    # cannot start a dedicated server (upstream #4155). The lockfile records
    # the project as slug.github = "GregTechCEu/GregTech-Modern".
    "GregTechCEu/GregTech-Modern": "gtceu",
}

# Namespaces that ship with the pack but not from a CurseForge project.
BUILTIN_NAMESPACES = {"minecraft", "foldedhorizons"}


# --------------------------------------------------------------------------
# SNBT parsing (subset sufficient for FTB Quests files)
# --------------------------------------------------------------------------

def tokenize(text: str):
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c in " \t\r\n":
            i += 1
            continue
        if c == "#" or (c == "/" and i + 1 < n and text[i + 1] == "/"):
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c in "{}[]:,":
            yield (c, c)
            i += 1
            continue
        if c == '"':
            j = i + 1
            buf = []
            while j < n:
                if text[j] == "\\":
                    buf.append(text[j + 1])
                    j += 2
                    continue
                if text[j] == '"':
                    yield ("str", "".join(buf))
                    i = j + 1
                    break
                buf.append(text[j])
                j += 1
            else:
                raise ValueError("unterminated string")
            continue
        j = i
        while j < n and text[j] not in ' \t\r\n{}[]:,"#':
            j += 1
        yield ("word", text[i:j])
        i = j


def parse(tokens):
    tok = list(tokens)
    pos = 0

    def peek():
        return tok[pos] if pos < len(tok) else (None, None)

    def take():
        nonlocal pos
        t = tok[pos]
        pos += 1
        return t

    def value():
        kind, _ = peek()
        if kind == "{":
            take()
            out = {}
            while peek()[0] in ("str", "word"):
                _, key = take()
                if peek()[0] != ":":
                    raise ValueError(f"expected ':' after key {key!r}")
                take()
                out[key] = value()
                if peek()[0] == ",":
                    take()
            if take()[0] != "}":
                raise ValueError("expected '}'")
            return out
        if kind == "[":
            take()
            arr = []
            while peek()[0] != "]":
                arr.append(value())
                if peek()[0] == ",":
                    take()
            take()
            return arr
        _, v = take()
        return v

    result = value()
    if pos != len(tok):
        raise ValueError(f"trailing tokens at {pos}: {tok[pos:pos + 3]}")
    return result


def load(path: pathlib.Path):
    return parse(tokenize(path.read_text(encoding="utf-8")))


# --------------------------------------------------------------------------
# Pack namespaces (so we can catch wrong mod ids)
# --------------------------------------------------------------------------

def slug_keys(project: dict) -> list[str]:
    """Every slug a lockfile project is known by, across all platforms."""
    slugs = project.get("slug") or {}
    keys = []
    for value in slugs.values():
        if not value:
            continue
        if isinstance(value, dict):  # github: {owner, repo}
            owner, repo = value.get("owner"), value.get("repo")
            if owner and repo:
                keys.append(f"{owner}/{repo}")
        else:
            keys.append(str(value))
    return keys


def pack_namespaces() -> set[str]:
    """Namespaces the pack can actually resolve.

    Derived by mapping each project in the Pakku lockfile through
    SLUG_NAMESPACES, so a mod removed from the pack makes its namespace
    disappear here too and any quest still referencing it is flagged.
    """
    ns = set(BUILTIN_NAMESPACES)
    if not LOCKFILE.exists():
        return ns
    try:
        data = json.loads(LOCKFILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ns
    for project in data.get("projects", []):
        if not isinstance(project, dict):
            continue
        for slug in slug_keys(project):
            if slug in SLUG_NAMESPACES:
                ns.add(SLUG_NAMESPACES[slug])
    return ns


def main() -> int:
    problems: list[str] = []

    if not QUESTS_DIR.is_dir():
        print(f"missing {QUESTS_DIR}", file=sys.stderr)
        return 1

    files = sorted(QUESTS_DIR.rglob("*.snbt"))
    parsed: dict[pathlib.Path, object] = {}
    for f in files:
        try:
            parsed[f] = load(f)
        except Exception as exc:  # noqa: BLE001 - report every failure
            problems.append(f"parse error in {f}: {exc}")
    print(f"parsed {len(parsed)}/{len(files)} SNBT files")

    quest_ids: dict[str, pathlib.Path] = {}
    dependencies: list[tuple[pathlib.Path, str, str]] = []
    total = 0

    for f, doc in parsed.items():
        if not (isinstance(doc, dict) and "quests" in doc):
            continue
        for q in doc["quests"]:
            total += 1
            qid = q.get("id")
            if not qid:
                problems.append(f"{f}: quest without id: {q.get('title', '?')}")
                continue
            if qid in quest_ids:
                problems.append(
                    f"duplicate quest id {qid} in {f} and {quest_ids[qid]}")
            quest_ids[qid] = f
            if not q.get("title"):
                problems.append(f"{f}: quest {qid} has no title")
            if "tasks" not in q:
                problems.append(f"{f}: quest {qid} has no tasks")
            for dep in q.get("dependencies", []):
                dependencies.append((f, qid, dep))

    for f, qid, dep in dependencies:
        if dep not in quest_ids:
            problems.append(f"{f}: quest {qid} depends on unknown id {dep}")

    # Namespace sanity on item references.
    known = pack_namespaces()
    print(f"known namespaces: {', '.join(sorted(known))}")
    for f, doc in parsed.items():
        if not isinstance(doc, dict):
            continue
        for q in doc.get("quests", []):
            refs = []
            if isinstance(q.get("icon"), str):
                refs.append(q["icon"])
            for task in (q.get("tasks") or {}).values():
                if isinstance(task, dict) and isinstance(task.get("item"), str):
                    refs.append(task["item"])
            for ref in refs:
                if ":" not in ref:
                    problems.append(f"{f}: quest {q['id']} bad item id {ref!r}")
                    continue
                namespace = ref.split(":", 1)[0]
                if namespace not in known:
                    problems.append(
                        f"{f}: quest {q['id']} references namespace "
                        f"{namespace!r} not in pakku-lock.json ({ref})")

    print(f"{total} quests, {len(quest_ids)} unique ids, "
          f"{len(dependencies)} dependencies")
    if problems:
        print(f"\n{len(problems)} problem(s):", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    print("no problems found")
    return 0


if __name__ == "__main__":
    sys.exit(main())

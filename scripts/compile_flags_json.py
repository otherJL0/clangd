#!/usr/bin/env python
import json
import sys
from pathlib import Path
from typing import TypedDict

EXTS = (
    ".c",
    ".C",
    ".cpp",
    ".cc",
    ".cxx",
    ".m",
    ".mm",
    ".h",
    ".H",
    ".hpp",
    ".hh",
    ".hxx",
)


class CompileCommand(TypedDict):
    directory: str
    file: str
    arguments: list[str]


compile_flags: Path = Path.cwd() / (
    sys.argv[1] if len(sys.argv) > 1 else "compile_flags.txt"
)
compiler = sys.argv[2] if len(sys.argv) > 2 else "clang"
with compile_flags.open("r") as f:
    flags = [line.strip() for line in f.readlines()]

project_dir: Path = compile_flags.parent

compile_commands: list[CompileCommand] = []

for item in project_dir.glob("**/*"):
    if not item.is_file() and item.suffix not in EXTS:
        continue

    compile_commands.append(
        {
            "directory": str(project_dir),
            "file": str(item.absolute),
            "arguments": [compiler] + flags + [str(item.absolute)],
        }
    )

with (project_dir / "compile_commands.json").open("w") as file:
    json.dump(compile_commands, file, indent=2)

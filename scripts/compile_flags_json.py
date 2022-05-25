#!/usr/bin/env python
import json
import sys
from pathlib import Path
from typing import List, TypedDict

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
    arguments: List[str]


compile_flags = Path(sys.argv[1] if len(sys.argv) > 1 else "compile_flags.txt")
compiler = sys.argv[2] if len(sys.argv) > 2 else "clang"
with compile_flags.open("r") as f:
    flags = [line.strip() for line in f.readlines()]

project_dir: Path = compile_flags.parent

compile_commands: List[CompileCommand] = [
    {
        "directory": str(project_dir.absolute()),
        "file": str(file_path.absolute()),
        "arguments": [compiler] + flags + [str(file_path.absolute)],
    }
    for file_path in project_dir.glob("**/*")
    if file_path.is_file() and file_path.suffix in EXTS
]


with (project_dir / "compile_commands.json").open("w") as file:
    json.dump(compile_commands, file, indent=2)

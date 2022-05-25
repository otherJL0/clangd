#!/usr/bin/env python
import json
import os
import sys

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

compile_flags = sys.argv[1] if len(sys.argv) > 1 else "compile_flags.txt"
compiler = sys.argv[2] if len(sys.argv) > 2 else "clang"
with open(compile_flags) as f:
    flags = [line.strip() for line in f]

project_dir = os.path.dirname(os.path.abspath(compile_flags))

compile_commands = []

for root, dirs, files in os.walk(project_dir):
    for file in files:
        ext = os.path.splitext(file)[1]
        if ext in EXTS:
            compile_commands.append(
                {
                    "directory": project_dir,
                    "file": os.path.join(project_dir, file),
                    "arguments": [compiler] + flags + [os.path.join(project_dir, file)],
                }
            )

with open(os.path.join(project_dir, "compile_commands.json"), "w") as file:
    json.dump(compile_commands, file, indent=2)

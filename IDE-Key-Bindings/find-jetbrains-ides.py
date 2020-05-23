#!/usr/bin/env python3

from pathlib import Path
import re
from re import Pattern
from typing import Optional, Iterable
import sys
from collections import defaultdict
import difflib
import subprocess


MAC_SETTINGS_DIRS = [
    Path("~/Library/Preferences"),
    Path("~/Library/Application Support"),
    Path("~/Library/Application Support/JetBrains"),
]

EDITORS = [
    "PyCharm",
    "GoLand"
]


class IDEMatch:
    path: Path
    ide_name: str
    ide_name_suffix: str
    year: int
    version: str

    def __init__(self, path, ide_name, ide_name_suffix, year, version):
        self.path = path
        self.ide_name = ide_name
        self.ide_name_suffix = ide_name_suffix
        self.year = year
        self.version = version
        
    @staticmethod
    def jetbrains_dir_pattern() -> Pattern:
        opts = "(" + "|".join(EDITORS) + ")([a-zA-Z]*?)"
        return re.compile(
            opts + 
            r"(\d+)\.(\d+)")
        # return re.compile(opts + r"\d+\.\d+")

    @classmethod
    def from_jetbrains_dir(cls, path: Path) -> Optional["IDEMatch"]:
        match = cls.jetbrains_dir_pattern().match(path.name)
        if match is None:
            return None
        ide_name, ide_name_suffix, year, version = match.groups()
        return IDEMatch(
            path=path,
            ide_name=ide_name,
            ide_name_suffix=ide_name_suffix,
            year=int(year),
            version=int(version)
        )
    
    def __str__(self):
        return str(f"<IDE: {self.path}>")


def jetbrains_dirs() -> Iterable[IDEMatch]:
    """
    All JetBrains directories located in macOS settings locations. Filtered to only those
    that match dirname expectations.
    """
    for settings_dir in MAC_SETTINGS_DIRS:
        for editor in EDITORS:
            for jetbrains_dir in settings_dir.expanduser().glob(f"{editor}*"):
                if not jetbrains_dir.is_dir():
                    continue
                ide = IDEMatch.from_jetbrains_dir(jetbrains_dir)
                if ide is not None:
                    yield ide
                else:
                    print(f"IGNORE: {jetbrains_dir}")


def current_jetbrains_dirs() -> Iterable[IDEMatch]:
    """All current JetBrains directories; i.e., the latest version of each JetBrains IDE."""
    by_editor = defaultdict(lambda: [])
    for editor in jetbrains_dirs():
        by_editor[editor.ide_name].append(editor)
    for editors in by_editor.values():
        editors.sort(key=lambda editor: (editor.year, editor.version))
        for editor in editors[:-1]:
            print(f"IGNORE: {editor.path}")
        yield editors[-1]


def git_keymap_for(ide_name: str) -> Path:
    """Error if keymap not found."""
    keymap_path = Path(".") / f"MattJW-{ide_name}.xml"
    if not keymap_path.is_file():
        raise Exception(f"git keymap file {keymap_path} does not exist or is not a file")
    return keymap_path


def jetbrains_keymap_for(editor_dir: Path, keymap_filename: str) -> Path:
    """Path to where keymap is expected (it may not exist)."""
    return editor_dir / "keymaps" / keymap_filename


def main():
    editors = list(current_jetbrains_dirs())
    print()
    for editor in editors:
        print(f"\n==== {editor.ide_name} ====\n")
        print(f"JetBrains settings dir:  {editor.path}\n")
        git_keymap_file = git_keymap_for(ide_name=editor.ide_name)
        jetbrains_keymap_file = jetbrains_keymap_for(editor_dir=editor.path, keymap_filename=git_keymap_file.name)

        print(f"git keymap file:         {git_keymap_file}")
        print(f"JetBrains keymap file:   {jetbrains_keymap_file}")

        git_contents = git_keymap_file.read_text()

        if not jetbrains_keymap_file.is_file():
            print("\nJetBrains keymap file does not exist")
            jetbrains_contents = ""
        else:
            jetbrains_contents = jetbrains_keymap_file.read_text()

        print("\nDiff: Edits required to transform GIT KEYMAP to JETBRAINS KEYMAP...\n")
        print(
            "\n".join(
                difflib.unified_diff(
                    git_contents.split("\n"),
                    jetbrains_contents.split("\n"),
                    fromfile=f"{git_keymap_file}",
                    tofile=f"{jetbrains_keymap_file}",
                )
            )
        )

        print()
        print("Open in VS Code...")
        args = [
            'code',
            '-n',
            '-d',
            f"{git_keymap_file}",
            f"{jetbrains_keymap_file}",
        ]
        print(" ".join(args))
        if jetbrains_keymap_file.exists():
            subprocess.run(arg.strip('"') for arg in args)


if __name__ == "__main__":
    main()

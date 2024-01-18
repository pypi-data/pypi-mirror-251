from __future__ import annotations
import os
from pathlib import Path
from typing import Literal, Union
from uuid import uuid4
from dataclasses import dataclass
import json

from .constants import PLUGIN_MANIFEST

PYTHON = Literal['Python']
PYTHON_V2 = Literal['Python_v2']
CSHARP = Literal['CSharp']
FSHARP = Literal['FSharp']
EXECUTABLE = Literal['Executable']
EXECUTABLE_V2 = Literal['Executable_V2']
TYPESCRIPT = Literal['TypeScript']
TYPESCRIPT_V2 = Literal['TypeScript_V2']
JAVASCRIPT = Literal['JavaScript']
JAVASCRIPT_V2 = Literal['JavaScript_V2']


LANGUAGES = Literal[
    PYTHON,
    PYTHON_V2,
    CSHARP,
    FSHARP,
    EXECUTABLE,
    EXECUTABLE_V2,
    TYPESCRIPT,
    TYPESCRIPT_V2,
    JAVASCRIPT,
    JAVASCRIPT_V2
]

DEFAULT_PLUGIN_PATH = Path().cwd().joinpath(PLUGIN_MANIFEST)


def generate_uuid() -> str:
    return str(uuid4())


@dataclass
class PluginManifest:
    ID: str
    ActionKeyword: str
    Name: str
    Description: str
    Author: str
    Version: str
    Language: Union[LANGUAGES, str]
    Website: str
    IcoPath: str
    ExecuteFileName: str

    @staticmethod
    def from_path(path: Path = Path.cwd()) -> PluginManifest:
        full_path = Path(path).joinpath(PLUGIN_MANIFEST)
        return PluginManifest.from_file(full_path)

    @staticmethod
    def from_file(path: Path = DEFAULT_PLUGIN_PATH) -> PluginManifest:
        with open(path, "r", encoding='UTF-8') as f:
            return PluginManifest(**json.load(f))


def create_manifest(path: str = '.') -> None:
    id = generate_uuid()
    print(f"Generated ID: {id}")
    manifest = PluginManifest(
        ID=id,
        ActionKeyword=input("ActionKeyword: ") or "",
        Name=input("Name: "),
        Description=input("Description: "),
        Author=input(f"Author [{os.getlogin()}]: ") or os.getlogin(),
        Version=input("Version [0.0.0]: ") or "0.0.0",
        Language=input("Language [Python]: ") or "Python",
        Website=input("Website: "),
        IcoPath=input("IcoPath: "),
        ExecuteFileName=input("ExecuteFileName: "),
    )
    with open(Path(path).joinpath(PLUGIN_MANIFEST), "w", encoding='UTF-8') as f:
        json.dump(manifest.__dict__, f, indent=4)
    print(f"Created manifest at {Path(path).joinpath(PLUGIN_MANIFEST)}")

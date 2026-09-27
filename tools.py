"""Small policy-checked tools exposed to the coding agent."""
from __future__ import annotations
import subprocess
from pathlib import Path
from typing import Any

class Workspace:
    def __init__(self, root: str | Path): self.root = Path(root).resolve()
    def path(self, relative: str) -> Path:
        target = (self.root / relative).resolve()
        if target != self.root and self.root not in target.parents: raise ValueError("Path escapes workspace")
        return target
    def read_file(self, path: str) -> str: return self.path(path).read_text()
    def write_file(self, path: str, content: str) -> str:
        target = self.path(path); target.parent.mkdir(parents=True, exist_ok=True); target.write_text(content); return f"wrote {path}"
    def run_tests(self) -> str:
        result = subprocess.run(["python", "-m", "pytest", "-q"], cwd=self.root, capture_output=True, text=True, timeout=60)
        return (result.stdout + result.stderr)[-4000:]

def definitions() -> list[dict[str, Any]]:
    return [{"type":"function","function":{"name":"read_file","description":"Read a UTF-8 file in the workspace","parameters":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}}},
            {"type":"function","function":{"name":"write_file","description":"Write a UTF-8 file in the workspace","parameters":{"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"}},"required":["path","content"]}}},
            {"type":"function","function":{"name":"run_tests","description":"Run the repository test suite","parameters":{"type":"object","properties":{}}}}]

def execute(ws: Workspace, name: str, args: dict[str, Any]) -> str:
    if name == "read_file": return ws.read_file(args["path"])
    if name == "write_file": return ws.write_file(args["path"], args["content"])
    if name == "run_tests": return ws.run_tests()
    raise ValueError(f"Unknown tool: {name}")

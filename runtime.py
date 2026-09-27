from __future__ import annotations
import json, importlib, time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

@dataclass
class PluginContext:
    root: Path
    session: dict[str, Any]

class PluginRuntime:
    def __init__(self, root: str | Path = "."):
        self.root=Path(root).resolve(); self.plugins={}; self.session={"started_at":time.time(),"events":[]}
    def register(self, name: str, plugin: Any):
        if not hasattr(plugin, "run"): raise TypeError(f"Plugin {name} must expose run(context, input)")
        self.plugins[name]=plugin
    def load_from_config(self, config_path: str | Path):
        config=json.loads(Path(config_path).read_text())
        for item in config["plugins"]:
            module=importlib.import_module(item["module"]); self.register(item["name"], module)
    def run(self, name: str, request: str) -> dict:
        if name not in self.plugins: raise KeyError(name)
        started=time.time(); result=self.plugins[name].run(PluginContext(self.root,self.session),request)
        event={"plugin":name,"request":request,"result":result,"elapsed_s":round(time.time()-started,4)}
        self.session["events"].append(event); return event

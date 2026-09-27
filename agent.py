"""The complete harness loop: model -> tool policy -> observation -> model."""
from __future__ import annotations
import json, time
from pathlib import Path
from .provider import MockProvider, OpenRouterProvider
from .tools import Workspace, definitions, execute

class CodingHarness:
    def __init__(self, workspace: str | Path, live: bool = False, trace_path: str | Path = "artifacts/part_a_trace.jsonl"):
        self.ws = Workspace(workspace); self.provider = OpenRouterProvider() if live else MockProvider(); self.trace_path = Path(trace_path)
        self.trace_path.parent.mkdir(parents=True, exist_ok=True)
    def run(self, task: str, max_steps: int = 8) -> dict:
        messages = [{"role":"system","content":"You are a careful coding agent. Use tools only inside the workspace, explain actions, and stop when the task is complete."},{"role":"user","content":task}]
        events = []
        for step in range(max_steps):
            start = time.time(); answer = self.provider.complete(messages, definitions())
            events.append({"step":step,"type":"assistant","content":answer.content,"tool_calls":answer.tool_calls})
            messages.append({"role":"assistant","content":answer.content})
            if not answer.tool_calls: break
            for call in answer.tool_calls:
                try: result = execute(self.ws, call["name"], call["arguments"])
                except Exception as exc: result = f"TOOL_ERROR: {exc}"
                events.append({"step":step,"type":"tool","name":call["name"],"result":result,"elapsed_s":round(time.time()-start,4)})
                messages.append({"role":"tool","content":result})
        with self.trace_path.open("w") as f:
            for event in events: f.write(json.dumps(event) + "\n")
        return {"task":task,"steps":len(events),"trace":str(self.trace_path),"events":events}

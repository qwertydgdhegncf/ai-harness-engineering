"""Original plugin #2: create a compact project decision record."""
import json
from pathlib import Path
def run(ctx, request):
    path=ctx.root/"artifacts"/"project_memory.json"; path.parent.mkdir(exist_ok=True)
    data=json.loads(path.read_text()) if path.exists() else {"decisions":[]}
    data["decisions"].append({"decision":request,"status":"open","source":"creator-mode"}); path.write_text(json.dumps(data,indent=2))
    return {"saved":True,"decision_count":len(data["decisions"]),"storage":str(path)}

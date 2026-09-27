"""Original plugin #1: turn notes into searchable, tagged memory cards."""
import json, re
from pathlib import Path
def run(ctx, request):
    path=ctx.root/"artifacts"/"second_brain.json"; path.parent.mkdir(exist_ok=True)
    cards=json.loads(path.read_text()) if path.exists() else []
    tags=re.findall(r"#([a-zA-Z0-9_-]+)",request); clean=re.sub(r"#[a-zA-Z0-9_-]+","",request).strip()
    card={"id":len(cards)+1,"note":clean,"tags":sorted(set(tags))}; cards.append(card); path.write_text(json.dumps(cards,indent=2))
    return {"created":card,"total_cards":len(cards),"storage":str(path)}

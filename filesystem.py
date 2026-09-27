from pathlib import Path
def run(ctx, request):
    files=[str(p.relative_to(ctx.root)) for p in ctx.root.rglob("*") if p.is_file() and ".git" not in p.parts]
    return {"request":request,"files":files[:100],"count":len(files)}

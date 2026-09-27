import subprocess
def run(ctx, request):
    allowed={"pwd","ls","find"}; command=request.strip().split()[0] if request.strip() else ""
    if command not in allowed: return {"error":"Only read-only commands pwd, ls, and find are allowed"}
    result=subprocess.run(request, shell=True, cwd=ctx.root, capture_output=True, text=True, timeout=10)
    return {"command":request,"stdout":result.stdout[-2000:],"stderr":result.stderr[-1000:],"returncode":result.returncode}

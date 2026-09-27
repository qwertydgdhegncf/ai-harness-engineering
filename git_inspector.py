import subprocess
def run(ctx, request):
    result=subprocess.run(["git","status","--short","--branch"],cwd=ctx.root,capture_output=True,text=True)
    return {"status":result.stdout,"request":request}

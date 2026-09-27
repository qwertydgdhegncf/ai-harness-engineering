import subprocess
def run(ctx, request):
    result=subprocess.run(["python","-m","pytest","-q"],cwd=ctx.root,capture_output=True,text=True,timeout=60)
    return {"passed":result.returncode==0,"output":(result.stdout+result.stderr)[-4000:]}

from pathlib import Path
from .runtime import PluginRuntime
def main():
    runtime=PluginRuntime("."); runtime.load_from_config(Path(__file__).with_name("dsh.config.json"))
    requests={"filesystem":"show repository files","git_inspector":"inspect git status","second_brain":"Study plugin contracts #harness #learning","project_memory":"Use deterministic seeds for reproducibility","test_runner":"run tests"}
    for name,request in requests.items(): print(name, runtime.run(name,request))
    Path("artifacts").mkdir(exist_ok=True); Path("artifacts/part_b_session.json").write_text(__import__("json").dumps(runtime.session,indent=2,default=str))
if __name__ == "__main__": main()

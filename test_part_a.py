from pathlib import Path
from part_a.agent import CodingHarness
from part_a.tools import Workspace

def test_mock_harness_writes_inside_workspace(tmp_path):
    result=CodingHarness(tmp_path, trace_path=tmp_path/"trace.jsonl").run("Create hello.txt containing Hello harness")
    assert (tmp_path/"hello.txt").read_text()=="Hello harness\n"
    assert result["trace"]

def test_workspace_blocks_escape(tmp_path):
    try: Workspace(tmp_path).read_file("../outside.txt")
    except ValueError as exc: assert "escapes" in str(exc)
    else: raise AssertionError("escape should be blocked")

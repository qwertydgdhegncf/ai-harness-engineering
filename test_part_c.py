from part_c.autoresearch import run
def test_autoresearch_produces_evidence(tmp_path):
    result=run(3,tmp_path/"results.csv")
    assert result["iterations"]==3 and 0 <= result["best_accuracy"] <= 1
    assert (tmp_path/"results.csv").exists()

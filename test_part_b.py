from part_b.runtime import PluginRuntime
def test_creator_mode_loads_seven_plugins():
    r=PluginRuntime("."); r.load_from_config("part_b/dsh.config.json")
    assert len(r.plugins)==7
    result=r.run("second_brain","Remember reproducibility #ml")
    assert result["result"]["created"]["tags"]==["ml"]

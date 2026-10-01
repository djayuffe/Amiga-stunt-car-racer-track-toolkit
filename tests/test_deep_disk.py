import json,pathlib
r=json.loads((pathlib.Path(__file__).parents[1]/"adf_deep_report.json").read_text())
assert r["bytes"]==901120 and r["sectors"]==1760
assert r["unique_sectors"]==874
assert any("Rob Northen Computing" in x["text"] for x in r["strings"])
print("protected-disk static evidence: PASS")

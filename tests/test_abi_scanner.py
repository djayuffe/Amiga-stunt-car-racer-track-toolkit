import json,pathlib
r=pathlib.Path(__file__).parent
c=json.loads((r/"abi_candidates.json").read_text())
assert any(x["face_base"]==128 and x["face_count"]>=4 for x in c)
o=(r/"abi_scanned.obj").read_text()
assert len([x for x in o.splitlines() if x.startswith("v ")])==5
assert len([x for x in o.splitlines() if x.startswith("f ")])>=4
print("ABI scan/export: PASS")

import pathlib,sys
root=pathlib.Path(__file__).parents[1];sys.path.insert(0,str(root/"tools"))
from infer_disk_transform import infer,apply
from infer_renderer_abi import infer as ai
r=bytes(range(64));d=bytes(x^165 for x in r);q=infer(r,d);assert apply(d,q["transform"],True)==r
t=[{"kind":"MEMR","pc":0x1234,"address":0x10000+i*6,"size":2,"value":0} for i in range(12)]
assert ai(t)["candidates"][0]["stride"]==6
print("missing-logic inference: PASS")

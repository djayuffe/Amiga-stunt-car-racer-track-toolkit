import pathlib,sys,tempfile,json,subprocess,os
root=pathlib.Path(__file__).parents[1];sys.path.insert(0,str(root))
from scrtool.track import *
t=Track(2,0,[0]*100,[0]*100,[0]*100,[0]*100,[0]*100,[0]*100,0,0);t.xz[:2]=[0x12,0x13]
d=editor_dict(t);d["pieces"][1]["x"]=9;d["pieces"][1]["config"]=0x26
assert d["pieces"][0]["x"]==2 and d["pieces"][0]["z"]==1
q=from_editor_dict(d);assert q.xz[1]==0x19 and q.config[1]==0x26
try:
 d["pieces"][0]["index"]=1;from_editor_dict(d);assert False
except ValidationError:pass
print("release 1.1 editor import: PASS")

import os,sys,random,json
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","tools"))
from track804_codec_verified import *
from editor_interchange import *
random.seed(42)
t=Track804(3,1,[0]*100,[0]*100,[0]*100,[0]*100,[0]*100,[0]*100,4,9)
t.road_xz[:3]=[pack_xz(1,2),pack_xz(1,3),pack_xz(2,3)]
t.angle_template[:3]=[0x10,0x21,0x36]
raw=encode(t); d=export_editor(raw)
assert import_editor(d)==raw
d["pieces"][1]["grid_x"]=7
raw2=import_editor(d); t2=decode(raw2)
assert unpack_xz(t2.road_xz[1])==(7,3)
assert raw2[0]==raw[0] and len(raw2)==804
print("editor native-field round-trip/edit: PASS")

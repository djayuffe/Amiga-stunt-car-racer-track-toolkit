import pathlib,sys
r=pathlib.Path(__file__).parents[1];sys.path.insert(0,str(r))
from scrtool.track import *
from scrtool.recover import scan,score_track
t=Track(4,0,[0]*100,[0]*100,[0]*100,[0]*100,[0]*100,[0]*100,2,3)
t.xz[:4]=[0x12,0x13,0x23,0x22];t.config[:4]=[0,1,3,4];t.left_height[:4]=[0,10,20,30]
b=b"noise!"+encode(t)+b"tail";q=scan(b,1,60)
assert any(x["offset"]==6 for x in q)
assert score_track(b,6)["score"]>=60
print("release 1.3 recovery scan: PASS")
